# qlapi



## Getting started

> export eeg to edf file
```python
from device import Rsa

def test_export():
    path = r'E:\\eeg' #eeg file path
    Rsa().export_edf(eeg_path=path)
```

> get signals from eeg file(or edf file)
```python
from device import Rsa

def get_all_signals():
    path = r'E:\\eeg' #eeg file path
    Rsa().get_data_within(path=path)

def get_signals(start_time, end_time):
    path = r'E:\\edf' #edf file path
    Rsa().get_data_within(path=path, start_time=start_time, end_time=end_time)

def get_signals_from_bdf(start_time, end_time):
    path = r'E:\\edf' #edf file path
    Rsa().get_data_within(path=path, start_time=start_time, end_time=end_time, extension='bdf')
```

> send stim signals to device

```python
from device import Rsa

def test_stim():
    paradigm = {
    "params": [{
        "channels": [ #刺激通道：所选通道列表，从通道号从0开始  
            {
                "waveform": 1,        #波形类型：0-直流，1-交流  -必填
                "frequency": 500,        #频率(Hz) -- 交流刺激必填
                "current": 1,    #电流强度(mA)  -必填
                "ramp_up": 5,    #上升时间(s) -- 默认0
                "ramp_down": 5,    #下降时间(s) -- 默认0
                "duration": 30,    #平稳阶段持续时间(s)  -必填
                "phase_position": 0,    #相位 -- 默认0
                "channel_id": 1,        #通道号 -- 必填
                "channel_position": "Fp2",
                "duration_delay": "0",
                "duration_startdown": "5",
                "ramp_up_rate": "",
                "ramp_down_rate": "",
                "smooth_rate": ""
            },
            {
                "waveform": 1,        #波形类型：0-直流，1-交流  -必填
                "frequency": 500,        #频率(Hz) -- 交流刺激必填
                "current": 1,    #电流强度(mA)  -必填
                "ramp_up": 5,    #上升时间(s) -- 默认0
                "ramp_down": 5,    #下降时间(s) -- 默认0
                "duration": 30,    #平稳阶段持续时间(s)  -必填
                "phase_position": 0,    #相位 -- 默认0
                "channel_id": 2,        #通道号 -- 必填
                "channel_position": "Fp2",
                "duration_delay": "0",
                "duration_startdown": "5",
                "ramp_up_rate": "",
                "ramp_down_rate": "",
                "smooth_rate": ""
            }
        ]
    }]

    Rsa().connect(r'10.80.101.185').stim_start(paradigm)
}
```

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
