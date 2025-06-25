import json
import os
import socket
import subprocess
import sys
import time
import urllib.request


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def req(method, url, data=None):
    if data is not None:
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), resp.read().decode()


def test_register_anchor_e2e():
    port = get_free_port()
    env = os.environ.copy()
    env['API_PORT'] = str(port)
    env['DATABASE_URL'] = 'sqlite:///./e2e.db'
    proc = subprocess.Popen([sys.executable, 'mind_bus_api.py'], env=env)
    try:
        time.sleep(1.5)
        payload = {'identity': 'E2E', 'model': 'gpt-4o', 'version': '1.0.0'}
        code, _ = req('PUT', f'http://localhost:{port}/anchors/e2e', payload)
        assert code == 200
        code, html = req('GET', f'http://localhost:{port}/dashboard')
        assert code == 200
        assert '<!DOCTYPE html>' in html
        code, anchors = req('GET', f'http://localhost:{port}/anchors')
        anchors = json.loads(anchors)
        assert any(a['gpt_id'] == 'e2e' for a in anchors)
    finally:
        proc.terminate()
        proc.wait()
