from functools import wraps
from inspect import signature


def _resolve_annotation(annotation, func_globals):
    if isinstance(annotation, str):
        annotation = eval(annotation, func_globals)
    return annotation


def check_input_types(args_to_check: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create dictionary of arg name: provided arg
            # https://stackoverflow.com/q/68847925
            sig = signature(func)
            provided_arg_dict = sig.bind_partial(*args, **kwargs).arguments

            # Only check specified arguments
            for arg_name in args_to_check:
                provided_arg = provided_arg_dict[arg_name]
                raw = sig.parameters[arg_name].annotation
                expected_arg_type = _resolve_annotation(raw, func.__globals__)
                if not isinstance(provided_arg, expected_arg_type):
                    raise ValueError(f"{arg_name} must be of type {expected_arg_type}!")
            return func(*args, **kwargs)

        return wrapper

    return decorator
