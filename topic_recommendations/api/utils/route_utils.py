def ensure_authentication(f):
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper
