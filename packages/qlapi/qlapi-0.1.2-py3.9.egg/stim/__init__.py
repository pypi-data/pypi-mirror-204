from ctypes import *
import json
from .nrsdk import nr_sdk as sdk

class Stimulator:
    # 直流刺激
    DC_STIM = 0
    # 交流刺激
    AC_STIM = 1

    def __init__(self, ip='127.0.0.1'):    
        # load sdk    
        self.api = sdk()
        #login
        self.login_handle = c_void_p(None)
        server_ip = c_char_p(ip.encode('utf-8'))
        res = self.api.QLNR_Login(server_ip, pointer(self.login_handle))

        #log
        msg = "success" if res == 0 else "fail"
        print("server[" + ip + "] connect " + msg)
        # print(self.login_handle)
        
    def __del__(self):
        #logout
        print("logout")
        # print(self.login_handle)
        self.api.QLNR_Logout(self.login_handle)
        #destory
        # print("destory")
        # print(self.login_handle)
        # self.api.QLNR_Destory()

        
    # 开始刺激
    def stim_start(self, param):
        print("stim start with paradigm")
        # 字符串格式统一为dict
        if isinstance(param, str):
            param = json.loads(param)

        s = json.dumps(param, indent=4)
        # print(s)

        param_2 = c_char_p(s.encode('utf-8'))
        resp = c_char_p(None)
        res = self.api.QLNR_StartStimulation(self.login_handle, param_2, pointer(resp))
        print("result:{}".format(res))
        # print("value:{}".format(resp.value))
    
        if res == 0:
            return 1
        return 0

    # 刺激
    def __stim_start(self, channels_p, channels_n, current, duration, waveform, frequency=0, phase_pos=0, ramp_up=0, ramp_down=0):
        ch_num = len(channels_p) + len(channels_n)
        if ch_num == 0:
            print("请至少指定一个刺激通道！")
            return 0

        # 参数转换为范式格式，统一参数
        jsonParam = {}
        jsonParam["channels"] =  [{}] * ch_num
        jsonParam["params"] = [{}]
        jsonParam["params"][0]["channels"] = [{}] * ch_num
        i = 0
        for ch in channels_p:
            jsonParam["channels"][i] = {}
            jsonParam["channels"][i]["channel_id"] = int(ch)
            jsonParam["params"][0]["channels"][i] = {}
            jsonParam["params"][0]["channels"][i]["waveform"] = waveform
            jsonParam["params"][0]["channels"][i]["current"] = current
            jsonParam["params"][0]["channels"][i]["frequecy"] = int(frequency)
            jsonParam["params"][0]["channels"][i]["duration"] = int(duration)
            jsonParam["params"][0]["channels"][i]["ramp_up"] = int(ramp_up)
            jsonParam["params"][0]["channels"][i]["ramp_down"] = int(ramp_down)
            jsonParam["params"][0]["channels"][i]["phase_position"] = int(phase_pos)
            jsonParam["params"][0]["channels"][i]["channel_id"] = int(ch)
            i += 1
        
        for ch in channels_n:
            jsonParam["channels"][i] = {}
            jsonParam["channels"][i]["channel_id"] = int(ch)
            jsonParam["params"][0]["channels"][i] = {}
            jsonParam["params"][0]["channels"][i]["waveform"] = waveform
            jsonParam["params"][0]["channels"][i]["current"] = -current
            jsonParam["params"][0]["channels"][i]["frequecy"] = int(frequency)
            jsonParam["params"][0]["channels"][i]["duration"] = int(duration)
            jsonParam["params"][0]["channels"][i]["ramp_up"] = int(ramp_up)
            jsonParam["params"][0]["channels"][i]["ramp_down"] = int(ramp_down)
            jsonParam["params"][0]["channels"][i]["phase_position"] = int(phase_pos)
            jsonParam["params"][0]["channels"][i]["channel_id"] = int(ch)
            i += 1
            
        return self.stim_start(jsonParam)

    # 直流电刺激
    def dc_start(self, channels_p, channels_n, current, duration, ramp_up=0, ramp_down=0):
        print("dc stim start")

        return self.__stim_start(channels_p, channels_n, current, duration, Stimulator.DC_STIM, 0, 0, ramp_up, ramp_down)

    # 交流电刺激
    def ac_start(self, channels_p, channels_n, current, duration, frequency, phase_pos=0, ramp_up=0, ramp_down=0):
        print("ac stim start")
        if frequency <= 0:
            print("交流电刺激必须指定频率值(频率单位Hz，值为正整数)")
            return 0;

        return self.__stim_start(channels_p, channels_n, current, duration, Stimulator.AC_STIM, frequency, phase_pos, ramp_up, ramp_down)

    # 停止刺激
    def stim_stop(self):
        print("sti_stop")
        resp = c_char_p(None)
        res = None
        try:
            res = self.api.QLNR_StopStimulation(self.login_handle, pointer(resp))
        except Exception as e:
            print(e)
        print(res)
        if res != 0:
            print("get unexcept result {}".format(res))
        else:
            print(resp.value)
        return res

    # 获取通道参数
    def get_param(self, ch):
        resp = c_char(1)
        print(resp)
        res = self.api.QLNR_GetStimulationChParam(self.login_handle, ch, resp)
        print(res)
        print(resp.value)

    # 获取全局参数
    def get_global_param(self):
        resp = c_wchar_p(None)
        res = self.api.QLNR_StopStimulation(self.login_handle, resp)
        print(res)
        print(resp.value)