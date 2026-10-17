# Ambar: software design analysis

Ambar is a personal, local, Jarvis-style assistant: it joins the user's devices in their
own network, talks with the user through a local language model, and acts on devices
(for example a motor) while the conversation continues. No external API is required.
CO2 and temperature are only the first test case used to validate and bound the system.

This repository supports the activity "Analysis and improvement of software design".

## Layout

| Path | Contents |
| --- | --- |
| `baseline/` | Original design: one class, `AmbarAssistant`, with ten responsibilities |
| `version_a/` | Improved design A: layered architecture with ports (domain, application, infrastructure, interface) |
| `version_b/` | Improved design B: event bus core with pluggable skills and adapters |
| `docs/VERSIONS.md` | What each version does differently and why |

## Run the tests

```bash
pip install pytest ruff
ruff check .
python -m pytest version_a/tests -q
python -m pytest version_b/tests -q
```

The tests need no broker, no ESP32 and no language model: ports and adapters are replaced by fakes.

## Branches

- `main`: baseline, CI and documentation, plus merged versions
- `feature/version-a-layered`: version A
- `feature/version-b-events`: version B

Author: Jonathan Israel Gonzalez Ruiz.
