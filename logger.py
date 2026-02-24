audit_log = []

def log_event(event: str):
    audit_log.append(event)

def get_logs():
    return audit_log