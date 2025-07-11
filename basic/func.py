class AccessLogger:
    def __init__(self, obj):
        self._obj = obj

    def __getattribute__(self, name):
        # 注意：访问 self._obj 需要特殊处理
        if name == "_obj":
            return object.__getattribute__(self, name)

        print(f"Accessing __getattribute__: {name}")
        return getattr(object.__getattribute__(self, "_obj"), name)

    def __getattr__(self, item):
        return f"return from __getattr__({item})"

# 使用示例
import datetime

logged_date = AccessLogger(datetime.datetime.now())
print(logged_date.day)  # 输出访问日志
print(logged_date.asda)  # 输出访问日志


print(globals())