from ctypes import *
import os
import json

def nr_sdk():    
    cur_path = os.path.dirname(__file__)
    dll_path = cur_path + "/lib/QLNRSdk.dll"
    api = cdll.LoadLibrary(dll_path)
    
    # init
    api.QLNR_Init()
    return api

_api = nr_sdk()

class NRSDK(object):
    def __init__(self) :
        self.ip = r'127.0.0.1'
        self.login_handle = c_void_p(None)
        self.connected = False

    def connect(self, ip=None):
        if ip:
            self.ip = ip
        #login
        server_ip = c_char_p(self.ip.encode('utf-8'))
        res = _api.QLNR_Login(server_ip, pointer(self.login_handle))
        self.connected = (res == 0)

        #log
        print("connect to app server[{}] {}.".format(self.ip, "success" if self.connect else "fail"))

        return self
        
    def close(self):
        print("logout from app server[{}]".format(self.ip))
        _api.QLNR_Logout(self.login_handle)
        self.connected = False
    
    # 未连接时，自动连接一次
    def _assert_connected(self):
        if self.connected:
            return
        
        self.connect()

    # 开始刺激
    def _start_stimulation(self, param):
        self._assert_connected()

        # 字符串格式统一为dict
        if isinstance(param, str):
            param = json.loads(param)

        s = json.dumps(param, indent=4)
        # print(s)

        param_2 = c_char_p(s.encode('utf-8'))
        resp = c_char_p(None)
        try:
            res = _api.QLNR_StartStimulation(self.login_handle, param_2, pointer(resp))
            print("start stimulation {}".format(resp_result(res)))
        except Exception as e:
            print(e)
    
        return _SUCCESS if res == _RESP_SUCCESS else _FAIL
        
    def _stop_stimulation(self):
        self._assert_connected()

        resp = c_char_p(None)
        try:
            res = _api.QLNR_StopStimulation(self.login_handle, pointer(resp))
            print("stop stimulation {}".format(resp_result(res)))
        except Exception as e:
            print(e)
        
        return _SUCCESS if res == _RESP_SUCCESS else _FAIL

_RESP_SUCCESS = 0
_SUCCESS = 1
_FAIL = 0

def resp_result(res):
    return 'success' if res == 0 else 'fail'

def show_result(res):
    return 'success' if res == 1 else 'fail'