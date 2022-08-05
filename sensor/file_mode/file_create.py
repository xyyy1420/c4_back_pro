from cmath import log
import os


def create_new_path(base_path, sensor_id):
    finall_path = os.path.join(base_path, sensor_id)
    log_path = os.path.join(finall_path, 'log')
    rule_path = os.path.join(finall_path, 'rules')
    csv_path = os.path.join(finall_path, 'csvs')

    os.makedirs(finall_path)
    os.makedirs(log_path)
    os.makedirs(rule_path)
    os.makedirs(csv_path)

    return {
        "sensor_path": finall_path,
        "log_path": log_path,
        "rule_path": rule_path,
        "csv_path": csv_path
    }
