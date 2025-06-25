import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

import pytest


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def request(method, url, data=None, headers=None):
    if data is not None:
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    if headers:
        for k,v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


@pytest.fixture(autouse=True)
def start_api(tmp_path):
    port = get_free_port()
    env = os.environ.copy()
    env['API_PORT'] = str(port)
    env['SECRET_STORE'] = str(tmp_path / 'store.json')
    proc = subprocess.Popen([sys.executable, 'mind_bus_api.py'], env=env)
    time.sleep(1.0)
    yield port
    proc.terminate()
    proc.wait()


def test_secret_crud_flow(start_api):
    port = start_api
    h = {'X-Role':'secrets.edit'}
    code, _ = request('POST', f'http://localhost:{port}/secrets/upload',
                      {'key':'OPENAI_API_KEY','value':'sk-test'}, h)
    assert code == 200
    code, body = request('GET', f'http://localhost:{port}/secrets', headers=h)
    assert code == 200
    secrets = json.loads(body)
    assert any(s['key']=='OPENAI_API_KEY' for s in secrets)
    code, _ = request('PATCH', f'http://localhost:{port}/secrets/OPENAI_API_KEY',
                      {'value':'sk-new'}, h)
    assert code == 200
    code, _ = request('DELETE', f'http://localhost:{port}/secrets/OPENAI_API_KEY',
                      headers=h)
    assert code == 200
    code, body = request('GET', f'http://localhost:{port}/secrets', headers=h)
    secrets = json.loads(body)
    assert not any(s['key']=='OPENAI_API_KEY' for s in secrets)
