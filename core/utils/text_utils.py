# bible-analysis/core/utils/text_utils.py

""" text utils """

import json


def ensure_json_format(text):
    """ensure_json_format"""
    if isinstance(text, str):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"text": text, "context": None}
    return text
