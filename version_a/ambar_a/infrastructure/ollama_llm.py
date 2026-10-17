"""Local language model served by Ollama. No cloud API involved."""
from __future__ import annotations

import json
import urllib.request


class OllamaLlm:
    def __init__(self, url: str, model: str, timeout: float = 60.0):
        self._url, self._model, self._timeout = url, model, timeout

    def generate(self, prompt: str) -> str:
        body = json.dumps({"model": self._model, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(self._url, body, {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self._timeout) as resp:
            return json.loads(resp.read())["response"]
