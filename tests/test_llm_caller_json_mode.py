import unittest
from unittest.mock import patch

from core.llm_caller import ask_llm_json


class _FakeResponse:
    def __init__(self, response_text):
        self._response_text = response_text

    def raise_for_status(self):
        return None

    def json(self):
        return {"response": self._response_text}


class AskLlmJsonTests(unittest.TestCase):
    def test_enables_ollama_json_mode_and_strips_wrappers(self):
        captured = {}

        def fake_post(url, json, timeout):
            captured["payload"] = json
            return _FakeResponse(
                "<think>I should return strict JSON.</think>\n"
                "```json\n"
                "{\"entities\": [], \"relationships\": []}\n"
                "```"
            )

        with patch("core.llm_caller.requests.post", side_effect=fake_post):
            result = ask_llm_json("extract graph")

        self.assertEqual(result, {"entities": [], "relationships": []})
        self.assertEqual(captured["payload"]["format"], "json")

    def test_recovers_python_style_dict_when_model_drifts(self):
        def fake_post(url, json, timeout):
            return _FakeResponse(
                "Here is the result you asked for:\n"
                "{'entities': [{'name': 'RBI'}], 'relationships': [],}\n"
                "Done."
            )

        with patch("core.llm_caller.requests.post", side_effect=fake_post):
            result = ask_llm_json("extract graph")

        self.assertEqual(result["entities"][0]["name"], "RBI")
        self.assertEqual(result["relationships"], [])


if __name__ == "__main__":
    unittest.main()
