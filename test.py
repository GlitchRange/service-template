import os
import time
import subprocess

def start_service():
    os.system("cd ./service && docker compose up --build -d")

def stop_service():
    os.system("cd ./service && docker compose down")

def run_glitch_checks():
    from checker import checker
    flag_id = os.urandom(16).hex()
    flag = f"flag{{{flag_id}}}"
    private = ''
    resp = checker.check('127.0.0.1')
    assert len(resp) == 3   # Ensure valid check response
    assert resp[2]          # Ensure 'check' check passed
    print("CHECK passed")

    resp = checker.put('127.0.0.1', flag, flag_id)
    assert len(resp) == 3 or len(resp) == 4   # Ensure valid put response
    assert resp[2]          # Ensure 'put' check passed
    if len(resp) == 4:
        flag_id = resp[3]
    print("PUT passed")

    resp = checker.get('127.0.0.1', flag, flag_id, resp[1])
    assert len(resp) == 3   # Ensure valid get response
    assert resp[2]          # Ensure 'get' check passed
    print("GET passed")
    print("All checks passed")

def run_forcad_checks():
    flag_id = os.urandom(16).hex()
    flag = f"flag{{{flag_id}}}"
    private = ''
    return_code = 0
    try:
        result = subprocess.check_output(["python3", "checker/checker.py", "check", "127.0.0.1"], timeout=30, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        result = e.stdout
    result = result.decode('latin-1')
    if len(result.split('\n')) > 1:
        private = result.split('\n')[0]
        public = result.split('\n')[1]
        debug = ', '.join(result.split('\n')[2:])
        print("CHECK:")
        print(f"  Private: {private}")
        print(f"  Public: {public}")
        print(f"  Debug: {debug}")
        print(f"  Return code: {return_code}")
    assert return_code == 101
    print("  CHECK passed")

    return_code = 0
    try:
        result = subprocess.check_output(["python3", "checker/checker.py", "put", "127.0.0.1", flag_id, flag, "1"], timeout=30, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        result = e.stdout
    result = result.decode('latin-1')
    if len(result.split('\n')) > 1:
        private = result.split('\n')[0]
        public = result.split('\n')[1]
        debug = ', '.join(result.split('\n')[2:])
        print("PUT:")
        print(f"  Private: {private}")
        print(f"  Public: {public}")
        print(f"  Debug: {debug}")
        print(f"  Return code: {return_code}")
    assert return_code == 101
    print("  PUT passed")

    return_code = 0
    try:
        result = subprocess.check_output(["python3", "checker/checker.py",  "get", "127.0.0.1", private, flag, "1"], timeout=30, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        result = e.stdout
    result = result.decode('latin-1')
    if len(result.split('\n')) > 1:
        private = result.split('\n')[0]
        public = result.split('\n')[1]
        debug = ', '.join(result.split('\n')[2:])
        print("GET:")
        print(f"  Private: {private}")
        print(f"  Public: {public}")
        print(f"  Debug: {debug}")
        print(f"  Return code: {return_code}")
    assert return_code == 101
    print("GET passed")
    print("All checks passed")

def cleanup_checks():
    os.system("rm -rf ./__pycache__")
    os.system("rm -rf ./checker/__pycache__")

if __name__ == "__main__":
    # Check type of service template
    if not os.path.exists("./checker/.template"):
        print("No service template found; set it in ./checker/.template")
        exit(1)
    with open("./checker/.template", "r") as f:
        template = f.read().strip()
    templates = {
        "glitch": run_glitch_checks,
        "forcad": run_forcad_checks,
    }
    if template not in templates:
        print(f"Unknown service template: {template}.  Must be one of {list(templates.keys())}")
        exit(1)
    start_service()
    print("Waiting for the service to start...")
    time.sleep(10) # Wait for the service to start
    print("Running checks...")
    templates[template]()
    cleanup_checks()
    stop_service()

