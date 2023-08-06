import os
import mne
import numpy as np
import tkinter as tk
import json
import pyedflib 
import math
import time
from datetime import datetime, timezone, timedelta

from ..base import *

'''
    [QL]eeg信号处理及使用接口
'''
class Recorder(object):
    def __init__(self):   
        # 根目录
        self._eeg_path = None
        self._edf_path = None
        # 记录最早开始时间
        self._start_time = None
        # 记录最晚结束时间
        self._end_time = None
        # 全部文件基本信息
        self._raw_list = []

    def export_edf(self, eeg_path=None, start_time=None, end_time=None, channels=None, edf_path=None, force=False, deepth=0):
        if not eeg_path:
            root = tk.Tk()
            root.withdraw()
            eeg_path = tk.filedialog.askdirectory()

        # 导默认保存到eeg文件相同目录
        print("eeg path is {}".format(eeg_path))
        if edf_path:
            print("edf path is {}".format(edf_path))

        eeg_files = get_file_list(eeg_path, "eeg")
        if len(eeg_files) == 0:
            print("No found eeg file in path {}".format(eeg_path))
            return
            
        last_eeg_file = eeg_files[-1] 
        if start_time or end_time:
            eeg_files = _eeg_file_filter(eeg_files, start_time, end_time)
        print('eeg file list: {}'.format(eeg_files))
        for eeg_file in eeg_files:
            # 最后一个文件覆盖已转换的edf文件
            if (eeg_file == last_eeg_file):                
                eeg_to_edf(eeg_file, edf_path, force=True)
            else:
                eeg_to_edf(eeg_file, edf_path, force=force)

    def _open(self, path=None):
        # 初始化示例变量
        self._eeg_path = self._edf_path = path
        self._raw_list = []
        self._start_time = None
        self._end_time = None

        # 手动选择文件夹
        if not self._eeg_path:
            root = tk.Tk()
            root.withdraw()
            self._eeg_path = self._edf_path = tk.filedialog.askdirectory()

        return self

    def _preload(self, start_time, end_time, extension='edf'):
            
        # 先导出为edf
        self.export_edf(self._eeg_path, start_time, end_time)

        # 读取edf/bdf文件
        self.file_list = get_file_list(self._eeg_path, extension)

        # 读取文件信息
        self._read_header()

        return self

    # 读取文件头信息
    def _read_header(self):
        if not self.file_list:
            raise Exception('File not found in path {}'.format(self._edf_path))

        print(self.file_list)
        for file in self.file_list:
            raw = mne.io.read_raw_edf(file, preload=False, verbose=False)

            # 当前文件记录开始时间和结束时间
            raw.start_time = raw.annotations.orig_time
            raw.end_time = raw.start_time + timedelta(seconds=raw.times[-1])

            if self._start_time is None or self._start_time > raw.start_time:
                self._start_time = raw.start_time

            if self._end_time is None or self._end_time < raw.end_time:
                self._end_time = raw.end_time

            self._raw_list.append(raw)

        if not self._raw_list:
            raise Exception('No data in in path {}'.format(self._edf_path))

        if self._start_time is None or self._end_time is None:
            raise Exception('Record time parse error.')

        print("Records from {} to {}, but may not be continuous.".format(
            self._start_time, self._end_time))

    # 时间对齐
    def _time_align(self, start_time=None, end_time=None):
        if start_time is None and end_time is None:
            end_time = self._end_time
            start_time = end_time + timedelta(days=-1)

        if start_time is None:
            start_time = end_time + timedelta(days=-1)

        if end_time is None:
            end_time = start_time + timedelta(days=1)

        # 时间区间内没有数据文件
        if start_time > self._end_time or end_time < self._start_time:
            raise Exception('No data between {} and {}'.format(
                start_time, end_time))

        return start_time, end_time

    # 获取指定时间区间的文件信息
    def get_raw_list(self, start_time, end_time):
        if len(self._raw_list) == 0:
            return []

        raw_list = []
        for idx_raw, raw in enumerate(self._raw_list):
            if raw.end_time >= start_time and raw.start_time <= end_time:
                raw_list.append(raw)

        return raw_list

    # 读取数据
    # trim 是否去掉记录实际开始前和结束后的无效时间区间
    def get_data_within(self,
                        start_time=None,
                        end_time=None,
                        channel=None,
                        sf=None,
                        resampling=False,
                        ref_channels=None,
                        path=None,
                        extension="edf", 
                        trim=True):

        # 读取文件列表
        self._open(path)._preload(start_time, end_time, extension)

        # 时间对齐
        start_time, end_time = self._time_align(start_time, end_time)
        print("Read data expect from {} to {}".format(start_time, end_time))

        # 只读取指定时间区间内的文件
        raw_list = self.get_raw_list(start_time, end_time)
        print(raw_list)

        # 去掉记录实际开始前和结束后的无效时间区间
        if trim:
            real_start_time = min(raw.start_time for raw in raw_list)
            if real_start_time > start_time:
                start_time = real_start_time
            real_end_time = max(raw.end_time for raw in raw_list)
            if real_end_time < end_time:
                end_time = real_end_time
            print("Read data from {} to {}".format(start_time, end_time))

        # 使用设置的采样率（未设置时取全部文件中的最小采样率）
        if sf is None:
            sf = min(raw.info['sfreq'] for raw in raw_list)

        # 按指定采样率重采样处理，未设置时按最低采样率处理
        if resampling:
            for idx_raw, raw in enumerate(raw_list):
                if not raw.info['sfreq'] == sf:
                    raw_list[idx_raw] = raw.copy().resample(sf)
        else:
            raw_list = [raw for raw in raw_list if raw.info['sfreq'] == sf]

        if not channel:
            channel = range(min(len(raw.ch_names) for raw in raw_list) - 1)
            print(channel)

        # 初始化数据数组
        data = np.empty(
            (len(channel),
             int(sf * (end_time - start_time).total_seconds()) + 1))
        data[:] = np.nan
        # print(data)

        # 读取数据
        for raw in raw_list:
            if all(isinstance(item, str) for item in channel):
                idx_chan = [raw.ch_names.index(item) for item in channel]
            elif all(isinstance(item, int) for item in channel):
                idx_chan = list(channel)
                ch_names = [raw.ch_names[i] for i in idx_chan]

            if 'idx_whole_start' not in locals():
                start_time_file = raw.annotations.orig_time
                idx_whole_start = int(
                    (start_time_file - start_time).total_seconds() * sf)
            else:
                idx_whole_start += data_len

            data_len = raw.n_times
            if idx_whole_start + data_len < 0:
                continue

            flag_overlap = (0 <= np.arange(idx_whole_start, idx_whole_start + data_len, 1)) \
                        & (np.arange(idx_whole_start, idx_whole_start + data_len, 1) < data.shape[1])

            data[:, max(0, idx_whole_start):min(idx_whole_start + data_len, data.shape[1])] = \
                mne.io.read_raw_edf(raw.filenames[0], verbose=False).get_data()[idx_chan][:, flag_overlap]

        # print(data[::5])
        info = mne.create_info(ch_names=ch_names,
                               sfreq=sf,
                               ch_types='eeg',
                               verbose=False)
        raw = mne.io.RawArray(data, info, verbose=False)

        # 设置重参考
        if ref_channels:
            raw.set_eeg_reference(ref_channels)
        return raw, path
    

'''
    <单文件处理>
    读取eeg文件的header、events、data
    导出eeg文件内容到edf格式的文件
'''
class QlEEG(object):

    def __init__(self, fname, exclude=(), infer_types=None, preload=False, include=None,
                 units=None, encoding='utf8', *, verbose=None):  
        self._init(fname, preload)
        self._load()

    def _init(self, fname, preload = False): 
        self._header = None
        self._events = None
        self._data = None 
        self._fname = fname
        self._preload = preload 

    def _load(self): 
        self._header = _read_eeg_header(self._fname)
        if self._preload:
            _read_eeg_data(self._fname, self._header)

    @property
    def data(self):
        if self._preload or self._data:
            return self._data
        
        return _read_eeg_data(self._fname, self._header)

    @property
    def header(self):
        return self._header

    @property
    def events(self):
        if self._events:
            return self._events
        return _read_eeg_events(self._fname, self._header)

    def export_edf(self, edf_path=None, force=False):
        def get_edf_fname():
            eeg_fname = self._fname.lower ()
            export_type = (".edf" if pbytes == 2 else ".bdf")
            if edf_path is None:
                edf_fname = eeg_fname.split('.eeg')[0] + export_type;
            else:
                # 创建目录
                if not os.path.exists(edf_path):
                    os.makedirs(edf_path)
                edf_fname = eeg_fname.replace("/", "\\").split('\\')[-1]
                edf_fname = edf_path + "\\" + edf_fname.split('.eeg')[0] + export_type;

            return edf_fname

        header = self.header
        nchan = header['channel_count']
        pbytes = header['point_bytes']

        edf_fname = get_edf_fname()
        # 文件存在则不导出，否则导出为edf/bdf
        # eeg 导出为 edf/bdf 存在两个场景：1、目标地址已存在导出的文件（不重复导出） 2、目标地址不存在文件，但文件已导出且处理过（和具体业务相关，暂不处理)
        if (not force) and os.path.exists(edf_fname):
            print("file {} had already exists.".format(edf_fname))
            return edf_fname

        t0 = time.time()
        file_type = pyedflib.FILETYPE_EDFPLUS if pbytes == 2 else pyedflib.FILETYPE_BDFPLUS
        print('edf file is {}'.format(edf_fname))
        f = pyedflib.EdfWriter(edf_fname,
                            nchan,
                            file_type=file_type)

        # edf/bdf header                    
        edf_header = self._get_edf_header()
        f.setSignalHeaders(edf_header)
        f.setStartdatetime(header['start_time'])
        f.setEquipment(DEVICE_MAPPING.get(header['device_type']))
        f.writeSamples(self.data,  digital = True)
        f.writeAnnotation(0, -1, "Recording starts")
        end_event = (header['packet_count'] * header['sample_count']) / header['sample_rate']
        f.writeAnnotation(end_event, -1, "Recording ends")

        # triggers
        events = self.events
        for event in events:
            f.writeAnnotation(event['offset'] / header['sample_rate'], -1, TRIGGER_MAPPING.get(event['id']))

        f.close()
        del f 

        t1 = time.time()            
        print("file {} export to {} success. cost {:.2f} seconds".format(self._fname, edf_fname, (t1 - t0)))

        return edf_fname

    def _get_edf_header(self):
        point_bytes = self._header['point_bytes']
        dmax = (1 << (point_bytes * 8 - 1)) - 1
        dmin = -1 - dmax
        pmax = int(dmax * 0.195)
        pmin = int(dmin * 0.195)
        channel_info = []
        for ch_name in self._header['channel_names']:
            ch_info = {
                'label': ch_name,
                'dimension': 'uV', # 固定
                'sample_rate': self._header['sample_rate'],
                'physical_max': pmax,
                'physical_min': pmin,
                'digital_max': dmax,
                'digital_min': dmin,
                'transducer': '',
                'prefilter': ''
            }
            channel_info.append(ch_info)
        return channel_info    


# eeg 单文件导出为 edf/bdf
def eeg_to_edf(eeg_file, edf_path=None, force=True):
    if eeg_file is None:
        print("no file!")

    qleeg = QlEEG(eeg_file)
    return qleeg.export_edf(edf_path=edf_path, force=force)

def _read_eeg_header(fname):     
    header = {'events': []}
    header['file_name'] = fname

    with open(fname, 'rb') as fid:
        header['magic'] = fid.read(4).decode("latin-1").rstrip()[:3]
        header['version'] = bytes_to_number(fid.read(4))
        header['length'] = bytes_to_number(fid.read(4))
        header['file_index'] = bytes_to_number(fid.read(4))
        header['device_type'] = bytes_to_number(fid.read(4))
        header['packet_count'] = bytes_to_number(fid.read(4))
        header['point_bytes'] = bytes_to_number(fid.read(1))
        header['origin_rate'] = bytes_to_number(fid.read(4))
        header['sample_rate'] = bytes_to_number(fid.read(4))
        header['ref_volt'] = bytes_to_number(fid.read(4))
        header['start_time'] = bytes_to_datetime(fid.read(10))
        header['end_time'] = bytes_to_datetime(fid.read(10))
        header['sample_count'] = bytes_to_number(fid.read(4))
        header['trigger_en'] = bytes_to_number(fid.read(1))
        extend_len = header['length'] - 62
        # eeg header extend info
        extend = json.loads(fid.read(extend_len).decode("latin-1").rstrip())
        header['channel_ids'] = []
        header['channel_names'] = []
        header['channel_count'] = len(extend['channels'])
        for channel in extend['channels']:
            header['channel_ids'].append(channel['channel_id']);
            ch_name = channel['channel_name'] if len(channel['channel_name']) > 0 else ("channel " + channel['channel_id'])
            header['channel_names'].append(ch_name);

        fid.seek(0,2)
        fbytes = fid.tell()
        header['fbytes'] = fbytes
        # packet总数量
        if header['packet_count'] == 0:
            header['packet_count'] = math.ceil((fbytes - header['length']) / (12 + (4 + header['channel_count'] * header['point_bytes']) * header['sample_count']))

        # 读取trigger信息
        # header['events'] = read_eeg_trigger()

    return header
  
def _read_eeg_events(fname, header):       
    events = [] 
    offset = header['channel_count'] * header['point_bytes']
    with open(fname, 'rb') as fid:
        # 跳过文件头
        fid.seek(header['length'], 0)
        packet_offset = 0
        while True:
            # 跳过包头
            fid.seek(12, 1)
            cur_bytes = fid.tell()
            #文件遍历完成
            if cur_bytes >= header['fbytes']:
                break

            for idx in range(header['sample_count']):
                event_id = bytes_to_number(fid.read(4), signed=False)
                if (event_id > 0): 
                    event = {}
                    event['id'] = event_id
                    event['offset'] = packet_offset
                    events.append(event)
                packet_offset += 1

                fid.seek(offset, 1)

    return events

def _read_eeg_data(fname, header=None):   
    if header is None:
        header = _read_eeg_header(fname)

    nchan = header['channel_count']
    nbytes = header['point_bytes']
    sample_count = header['sample_count']
    packet_count = header['packet_count']
    
    last_packet = -1
    if (packet_count == 0):
        fsize = os.path.getsize(header['file_name'])
        packet_count = math.ceil((fsize - header['length']) / (12 + (4 + nchan * 3) * sample_count))

    data =  np.empty((nchan, packet_count * sample_count), dtype=np.int16)
    offset = 0    
    with open(fname, 'rb') as fid:
        # 跳过header区
        fid.seek(header['length'], 0)   
        while(True):  
            fid.seek(3, 1)     
            group_count = bytes_to_number(fid.read(4), signed=False)
            if (group_count < 1):
                break

            # packet info
            packet_id = bytes_to_number(fid.read(4), signed=False)
            # print("group count is {}, packet id is {}".format(group_count, packet_id))
            if last_packet >=0 and packet_id - last_packet > 1:
                print("packet not continuous, current {}, last {}".format(packet_id, last_packet))
            # print(packet_id)
            last_packet = packet_id 
            fid.seek(1, 1)     
            for idx in range(group_count):
                event = bytes_to_number(fid.read(4), signed=False)                
                for idx_ch in range(nchan):
                    data[idx_ch][offset + idx] = bytes_to_number(fid.read(nbytes))

            offset += group_count

    print('file {} read data finished.'.format(fname))

    return data

def _eeg_file_filter(eeg_files, start_time=None, end_time=None):    
    if start_time is None and end_time is None:
        return eeg_files

    rst = []
    for eeg_file in eeg_files:
        eeg_header = _read_eeg_header(eeg_file)
        accept = True
        print('start:{}, end:{}, estart:{}, eend:{}'.format(start_time, end_time, eeg_header['start_time'], eeg_header['end_time']))
        if start_time:
            accept = accept and eeg_header['end_time'] >= start_time
        if end_time:
            accept = accept and eeg_header['start_time'] <= end_time
        if accept:
            rst.append(eeg_file)

    print('filter:{}'.format(rst))
    return rst