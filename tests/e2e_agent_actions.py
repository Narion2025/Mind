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


def test_agent_action_e2e():
    port = get_free_port()
    env = os.environ.copy()
    env['API_PORT'] = str(port)
    proc = subprocess.Popen([sys.executable, 'mind_bus_api.py'], env=env)
    try:
        time.sleep(1.5)
        if proc.poll() is not None:
            raise RuntimeError("API server failed to start")
        code, _ = req('POST', f'http://localhost:{port}/agents/e2e/action', {
            'op': 'connect', 'model': 'gpt-4o', 'identity': 'E2E', 'params': {}
        })
        assert code == 200
        code, anchors = req('GET', f'http://localhost:{port}/anchors')
        anchors = json.loads(anchors)
        assert any(a['gpt_id'] == 'e2e' for a in anchors)
        code, _ = req('POST', f'http://localhost:{port}/agents/e2e/action', {'op':'pause'})
        assert code == 200
        code, anchors = req('GET', f'http://localhost:{port}/anchors')
        anchors = json.loads(anchors)
        a = next(a for a in anchors if a['gpt_id']=='e2e')
        assert a['online'] is False
        code, _ = req('POST', f'http://localhost:{port}/agents/e2e/action', {'op':'delete'})
        assert code == 200
        code, anchors = req('GET', f'http://localhost:{port}/anchors')
        anchors = json.loads(anchors)
        assert not any(a['gpt_id']=='e2e' for a in anchors)
    finally:
        proc.terminate()
        proc.wait()
