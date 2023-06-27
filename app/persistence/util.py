from functools import wraps

from app import db_manager as db


def insert_result():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            inserts = f(*args, **kwargs)
            if isinstance(inserts, list):
                db.session.bulk_save_objects(inserts)
            else:
                db.session.add(inserts)
            db.session.commit()

        return decorated
    return decorator
