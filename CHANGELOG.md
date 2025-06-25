# Changelog

All notable changes to **Mind** are documented in this file.

## [2025-06-25] - Latest
### Added
- `SECURITY.md` with initial security policy guidance.

### Changed
- Merge conflicts resolved in `validate_thoughts.py` combining fallback YAML/JSON validation.
- Updated `start_all.sh` and new `start_voice_server.sh` to remove old Wirklichkeits API and use virtual environment.
- `token_registry.py` refactored for environment generation.
- `.github/workflows/ci.yml` ensures compilation and validation on CI.

### Removed
- Legacy `start_voice_server.sh` replaced and Wirklichkeits API start removed from scripts.

## [2025-06-24]
### Added
- Voice pipeline modules (`voice_pipeline/`) integrating HumeAI emotion detection and ElevenLabs TTS.
- Continuous integration workflow and thought validation schema.
- `mind_bootstrap.py` and `mind_bus_api.py` startup sequence with `start_mind.sh`.
- Central secrets management with `.env` generation and helper tests.

### Changed
- Environment handling simplified via `token_registry.generate_env_files`.
- README updated with voice pipeline setup and usage.

### Removed
- Old agent code such as `gpt_agent.py` and templates under `init/anchors/gpt_Narion`.

## Earlier
- Initial repository structure cleanup and addition of Wirklichkeits API server (now deprecated).
- Various minor fixes and repository hygiene updates.
