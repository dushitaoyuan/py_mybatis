from py_mybatis import PyFunction, PY_PARAM_FUNCTION
import time


def fun1(name: str):
    print("hello---" + name)


PY_PARAM_FUNCTION.register_func('print', print)
PY_PARAM_FUNCTION.register_func('fun1', fun1)
PY_PARAM_FUNCTION.call_func('print', 'name1', 'name2')

PY_PARAM_FUNCTION.call_func('fun1', 'name1')

print(PY_PARAM_FUNCTION.call_func('like', 'name'))

print(PY_PARAM_FUNCTION.call_func('time_format', time.localtime(), '%Y-%m-%d %H:%M:%S'))

print('fun1fun1(111)'.replace('fun1', 'fun', 1))


def add3(a, b):
    s = 'a+b'
    c = compile(s, '<expression string>', 'eval')

    print(locals())
    return eval(c, locals())


def add4(context):
    s = 'a+b'
    ccc = compile(s, '<expression string>', 'eval')

    return eval(ccc, locals())


print(add4({'a':1,'b':1}))
