import functools


def message_handler(message_code: str):
    """ Decorator for message handler """
    def wrapper(func):
        func.__kmx_message_code__ = message_code

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapped

    return wrapper
