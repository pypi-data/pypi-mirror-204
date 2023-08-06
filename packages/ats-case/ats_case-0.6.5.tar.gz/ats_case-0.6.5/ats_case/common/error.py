class APIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "APIError - API服务接口[{}], 连接失败.".format(repr(self.value))


class MeterOperationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "MeterOperationError - 电表操作错误, {}".format(repr(self.value))


class ClientError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ClientReturnError - 客户端返回结果为空. {}".format(repr(self.value))


