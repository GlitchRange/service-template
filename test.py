import os
import time
from checker import checker

def start_service():
    os.system("cd ./service && docker compose up --build -d")

def stop_service():
    os.system("cd ./service && docker compose down")

def run_checks():
    flag_id = os.urandom(16).hex()
    flag = f"flag{{{flag_id}}}"
    private = ''
    resp = checker.check('127.0.0.1')
    assert len(resp) == 3   # Ensure valid check response
    assert resp[2]          # Ensure 'check' check passed
    print("Check passed")

    resp = checker.put('127.0.0.1', flag, flag_id)
    assert len(resp) == 3   # Ensure valid put response
    assert resp[2]          # Ensure 'put' check passed
    print("Put passed")

    checker.get('127.0.0.1', flag, flag_id, resp[1])
    assert len(resp) == 3   # Ensure valid get response
    assert resp[2]          # Ensure 'get' check passed
    print("Get passed")
    print("All checks passed")

def cleanup_checks():
    os.system("rm -rf ./checker/__pycache__")

if __name__ == "__main__":
    start_service()
    print("Waiting for the service to start...")
    time.sleep(10) # Wait for the service to start
    print("Running checks...")
    run_checks()
    cleanup_checks()
    stop_service()

