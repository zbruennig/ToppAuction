from functools import wraps

from app import get_session


def insert_result():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            inserts = f(*args, **kwargs)
            if isinstance(inserts, list):
                get_session().bulk_save_objects(inserts)
            else:
                get_session().add(inserts)
            get_session().commit()

        return decorated
    return decorator
