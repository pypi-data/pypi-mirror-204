from ctypes import cdll
import os

def nr_sdk():    
    cur_path = os.path.dirname(__file__)
    dll_path = cur_path + "/lib/QLNRSdk.dll"
    api = cdll.LoadLibrary(dll_path)
    
    # init
    api.QLNR_Init()
    return api
    