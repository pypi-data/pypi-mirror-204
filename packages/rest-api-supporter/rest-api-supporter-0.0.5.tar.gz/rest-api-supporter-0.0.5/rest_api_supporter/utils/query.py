import requests

def query(url, json=None, data=None, headers=None, timeout=60):
    response = requests.post(url, json=json, data=data, headers=headers, timeout=timeout)
    outputs = response.json()
    return outputs
