import os


def get_time_difference_from_now(message_time, current_time):
    """Get the time difference between message_time and current_time, both are in UTC format"""
    time_diff = current_time - message_time
    return time_diff.total_seconds() / 60


def get_env_variable(var_name, default=None):
    """Check if the var_name is in virtual environment or pass a default"""
    if var_name not in os.environ:
        os.environ[var_name] = default
    return os.environ[var_name]