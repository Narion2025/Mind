import os
from pathlib import Path
import unittest

from token_registry import generate_env_files

class TestEnvGeneration(unittest.TestCase):
    def setUp(self):
        self._orig_env = os.environ.copy()
        os.environ['MINDSWARM_GITHUB_TOKEN'] = 'gh'
        os.environ['OPENAI_API_KEY'] = 'openai'
        os.environ['HUMEAI_API_KEY'] = 'hume'
        os.environ['ELEVENLABS_API_KEY'] = 'eleven'

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._orig_env)
        for name in ['imerion', 'claudius']:
            path = Path(f'.env.{name}')
            if path.exists():
                path.unlink()

    def test_generate_env_files(self):
        generate_env_files(['imerion', 'claudius'])
        for name in ['imerion', 'claudius']:
            path = Path(f'.env.{name}')
            self.assertTrue(path.exists())
            content = path.read_text().splitlines()
            self.assertEqual(content, [
                'MINDSWARM_GITHUB_TOKEN=gh',
                'OPENAI_API_KEY=openai',
                'HUMEAI_API_KEY=hume',
                'ELEVENLABS_API_KEY=eleven',
            ])

if __name__ == '__main__':
    unittest.main()
