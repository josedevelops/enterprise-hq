import os 
import subprocess


def is_reachable(host):
    """
    Standard 'test' check.
    Uses a system 'ping' to confirm the Management IP is responding.
    """
    command = ["ping", "-c", "1", "-W", "1", host]

    # using subprocess to run the system ping and capture the return code 
    # Return code 0 means success
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0
