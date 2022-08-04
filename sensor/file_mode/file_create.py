from cmath import log
import os


def create_new_path(base_path, sensor_id):
    finall_path = os.path.join(base_path, sensor_id)
    log_path = os.path.join(finall_path, 'log')
    rule_path = os.path.join(finall_path, 'rules')

    os.makedirs(finall_path.decode('utf-8'))
    os.makedirs(log_path.decode('utf-8'))
    os.makedirs(rule_path.decode('utf-8'))

    return {
        "sensor_path": finall_path,
        "log_path": log_path,
        "rule_path": rule_path
    }
