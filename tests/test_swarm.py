import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import yaml
import urllib.request


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def request(method, url, data=None):
    if data is not None:
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), resp.read().decode()


def start_api():
    port = get_free_port()
    env = os.environ.copy()
    env['API_PORT'] = str(port)
    proc = subprocess.Popen([sys.executable, 'mind_bus_api.py'], env=env)
    time.sleep(1.0)
    if proc.poll() is not None:
        raise RuntimeError('API server failed to start')
    return proc, port


def test_yaml_integritaet(tmp_path):
    base = Path('mind_root/schwarm/minds')
    base.mkdir(parents=True, exist_ok=True)
    (base / 'dummy.yaml').write_text('name: dummy')
    for f in base.glob('*.yaml'):
        yaml.safe_load(f.read_text())


def test_gui_funktion_neuer_agent():
    proc, port = start_api()
    try:
        payload = {
            'name': 'tester',
            'farbe': 'blau',
            'fokus': 'tests',
            'beschreibung': 'ein test'
        }
        code, _ = request('POST', f'http://localhost:{port}/agents', payload)
        assert code == 200
        yaml_path = Path('mind_root/schwarm/minds/tester.yaml')
        assert yaml_path.exists()
        data = yaml.safe_load(yaml_path.read_text())
        assert data['name'] == 'tester'
        for d in ['wiki', 'sort', 'narrative', 'lineage']:
            assert (Path('mind_root/schwarm/tester') / d).is_dir()
    finally:
        proc.terminate()
        proc.wait()


