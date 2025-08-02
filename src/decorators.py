import functools
import traceback
import sys
from typing import Callable, Optional, Tuple, Dict, Any

def log(filename: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name: str = func.__name__
            message_start: str = f"{func_name} started."
            if filename:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(message_start + '\n')
            else:
                print(message_start)
            try:
                result: Any = func(*args, **kwargs)
                message_ok: str = f"{func_name} ok"
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message_ok + '\n')
                else:
                    print(message_ok)
                return result
            except Exception as e:
                error_type: str = type(e).__name__
                inputs: Tuple[Tuple[Any, ...], Dict[str, Any]] = (args, kwargs)
                message_error: str = (f"{func_name} error: {error_type}. "
                                      f"Inputs: {inputs}")
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message_error + '\n')
                else:
                    print(message_error)
                # Передаем вывод стек-трейса в stdout
                traceback.print_exc(file=sys.stdout)
                raise
        return wrapper
    return decorator
