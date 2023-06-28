import logging

from functools import wraps
from json import dumps

logger = logging.getLogger(__name__)


def post_response(message=None, code=201):
    return {
        "message": message
    }, code


def captures_fails():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            fails = f(*args, **kwargs)
            if fails:
                return post_response(f"Could not insert the following records: {dumps(fails)}", 200)
            return post_response("All records successfully added")

        return decorated
    return decorator


def process_items(items: list, process_function) -> (list, list):
    '''
    Creates two lists, first is successful returns, if the function returns
    Second is failures, inputs for which an exception was thrown
    Iterates through items and runs the function on each
    :param items:
    :param process_function:
    :return:
    '''
    successes = []
    failures = []
    for item in items:
        try:
            processed = process_function(item)
            if processed is not None:
                successes.append(processed)
        except Exception:
            logger.warning(f"Could not process item: {dumps(item)}")
            failures.append(item)
    return successes, failures
