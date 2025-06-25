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


@pytest.fixture(autouse=True)
def start_api():
    port = get_free_port()
    env = os.environ.copy()
    env['API_PORT'] = str(port)
    env['DATABASE_URL'] = 'sqlite:///./test.db'
    proc = subprocess.Popen([sys.executable, 'mind_bus_api.py'], env=env)
    time.sleep(1.0)
    yield port
    proc.terminate()
    proc.wait()


def request(method, url, data=None):
    if data is not None:
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def test_put_anchor_valid(start_api):
    port = start_api
    payload = {"identity": "Test", "model": "gpt-4o", "version": "1.0.0"}
    code, body = request('PUT', f'http://localhost:{port}/anchors/test1', payload)
    assert code == 200
    data = json.loads(body)
    assert data['gpt_id'] == 'test1'
    assert 'created_at' in data


def test_bad_id(start_api):
    port = start_api
    payload = {"identity": "Test", "model": "gpt-4o", "version": "1.0.0"}
    code, _ = request('PUT', f'http://localhost:{port}/anchors/BAD!', payload)
    assert code == 400


def test_schema_error(start_api):
    port = start_api
    payload = {"identity": "Test", "model": "wrong", "version": "1"}
    code, _ = request('PUT', f'http://localhost:{port}/anchors/test2', payload)
    assert code == 422


def test_state_and_list(start_api):
    port = start_api
    payload = {"identity": "Test", "model": "gpt-4o", "version": "1.0.0"}
    request('PUT', f'http://localhost:{port}/anchors/test3', payload)
    code, body = request('GET', f'http://localhost:{port}/anchors')
    assert code == 200
    anchors = json.loads(body)
    assert any(a['gpt_id'] == 'test3' for a in anchors)
    code, body = request('GET', f'http://localhost:{port}/state?gpt_id=test3')
    assert code == 200
    assert body == 'online'


def test_capabilities_and_actions(start_api):
    port = start_api
    code, body = request('GET', f'http://localhost:{port}/capabilities')
    assert code == 200
    caps = json.loads(body)
    assert 'gpt-4o' in caps
    payload = {"identity": "A", "model": "gpt-4o", "version": "1.0.0"}
    request('PUT', f'http://localhost:{port}/anchors/act', payload)
    code, _ = request('POST', f'http://localhost:{port}/agents/act/action', {"op": "pause"})
    assert code == 200
    code, body = request('GET', f'http://localhost:{port}/state?gpt_id=act')
    assert body == 'offline'


def test_update_settings(start_api):
    port = start_api
    code, _ = request('PATCH', f'http://localhost:{port}/settings/ui', {"dark": "1"})
    assert code == 200

