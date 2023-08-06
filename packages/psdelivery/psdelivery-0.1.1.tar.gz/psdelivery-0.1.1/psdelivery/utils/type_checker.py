from typing import Type, List, Callable, Any
from types import UnionType


def must_be_type(arg_name: str, arg_type: Type | UnionType):
    """
    함수의 파라미터 타입이 맞는지 확인
    쉬프트연산이 들어간 UnionType은 지원 안하니까 쓰지 마셈
    args 체크 안하니까 이거 쓸때 arg_name=arg_val 형태로 쓰셈
    """
    def _decorator(func: Callable):
        def _wrapper(*args, **kwargs):
            valid_types: List[Type] = []
            if isinstance(arg_type, Type):
                valid_types = [arg_type]
            elif isinstance(arg_type, UnionType):
                valid_types = list(arg_type.__args__)

            if arg_name not in kwargs:
                raise ValueError(f'Argment {arg_name} is not exists.')
            arg_val: Any = kwargs[arg_name]

            is_valid = any([isinstance(arg_val, vt) for vt in valid_types])
            if not is_valid:
                raise ValueError('This type of argument is not valid')
            
            return func(*args, **kwargs)
        return _wrapper
    return _decorator