import builtins
from voice_pipeline import pipeline_orchestrator

class DummyHume:
    def __init__(self, agent):
        pass
    def analyze(self, audio):
        return {"emotion": "happy"}

class DummyTTS:
    def __init__(self, agent):
        pass
    def synthesize(self, text, voice_id):
        assert voice_id
        return b"AUDIO"

def test_run_pipeline(monkeypatch):
    monkeypatch.setattr(pipeline_orchestrator, "HumeClient", DummyHume)
    monkeypatch.setattr(pipeline_orchestrator, "ElevenLabsTTS", DummyTTS)
    result = pipeline_orchestrator.run_pipeline("imerion", "Hallo")
    assert result["emotion"] == "happy"
    assert result["prompt"].startswith("[HAPPY]")
    assert result["audio"] == b"AUDIO"
