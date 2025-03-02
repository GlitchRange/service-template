import requests

PORT = 1234
TIMEOUT = 10

OK = ('', '', True)

# Returns (public, private, success)
def check(host: str) -> tuple[str, str, bool]:
    response = requests.get(f'http://{host}:{PORT}', timeout=TIMEOUT)
    if response.status_code != 200:
        return ('unexpected status code ' + str(response.status_code), '', False)
    return OK

# Returns (public, private, success) or (public, private, success, flagid)
def put(host: str, flag: str, flag_id: str) -> tuple[str, str, bool] | tuple[str, str, bool, str]:
    response = requests.post(f'http://{host}:{PORT}/items/{flag_id}/{flag}', timeout=TIMEOUT)
    if response.status_code != 200:
        return ('unexpected status code ' + str(response.status_code), '', False)
    return OK

# Returns (public, private, success)
def get(host: str, flag: str, flag_id: str, private: str) -> tuple[str, str, bool]:
    response = requests.get(f'http://{host}:{PORT}/items/{flag_id}', timeout=TIMEOUT)
    if response.status_code != 200:
        return ('unexpected status code ' + str(response.status_code), '', False)
    if response.json()['item'] != flag:
        return ('flag does not match', '', False)
    return OK

