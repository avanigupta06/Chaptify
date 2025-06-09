from datetime import timedelta

def parse_timestamp(ts):
    h, m, s = map(int, ts.split(':'))
    return h * 3600 + m * 60 + s

def seconds_to_timestamp(seconds):
    return str(timedelta(seconds=seconds))

def format_timestamp_properly(ts):
    parts = ts.split(":")
    return f"{int(parts[0]):02d}:{int(parts[1]):02d}:{int(parts[2]):02d}"
