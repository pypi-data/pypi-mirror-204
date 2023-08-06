import functools


def rpc(name: str):
    """ Decorator for API functions """
    def wrapper(func):
        func.__kmx_rpc_function__ = name

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapped

    return wrapper
