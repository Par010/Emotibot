def get_time_difference_from_now(message_time, current_time):
    time_diff = current_time - message_time
    return time_diff.total_seconds() / 60
