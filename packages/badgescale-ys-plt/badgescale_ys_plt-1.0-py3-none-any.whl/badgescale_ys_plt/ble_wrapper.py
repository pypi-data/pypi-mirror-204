"""这是一个封装BLE客户端接口的模块。
它依赖软件包 bleak。
"""
class BLEWrapper(object):
    """note
    """
    def __init__(self):
        self._local_path = ''
        self._wf = None

