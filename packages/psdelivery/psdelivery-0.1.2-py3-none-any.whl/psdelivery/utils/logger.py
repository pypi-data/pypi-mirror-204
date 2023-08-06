class LogStatus:
    PROGRESS = 'progress'
    SUCCESS = 'success'
    FAILED = 'failed'

def print_log(logging: bool, msg: str):
    if logging:
        print(msg)

def print_status(logging: bool, log_type: str | None, msg: str):
    if log_type:
        msg = f'[{log_type}] {msg}'
    print_log(logging, msg)
