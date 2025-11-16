import re
import random

PLACEHOLDER_RE = re.compile(r"{([a-zA-Z0-9_]+)}")

SAMPLE_WORDS = {
    "name": ["Alex", "Sam", "Priya", "Ravi"],
    "animal": ["lion", "tiger", "elephant", "monkey"],
    "adjective": ["funny", "bright", "brave", "tall"],
    "adverb": ["quickly", "slowly", "beautifully"],
    "verb": ["dance", "jump", "run", "sing"],
    "verb_past": ["danced", "jumped", "ran", "sang"],
    "place": ["park", "space", "zoo", "school"],
    "color": ["blue", "red", "purple"],
    "job": ["doctor", "chef", "teacher"],
}

def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_placeholders(template):
    return list(dict.fromkeys(PLACEHOLDER_RE.findall(template)))

def random_fill_value(key):
    key = key.lower()
    if key in SAMPLE_WORDS:
        return random.choice(SAMPLE_WORDS[key])
    for k in SAMPLE_WORDS:
        if key.startswith(k):
            return random.choice(SAMPLE_WORDS[k])
    return "something"

def render_story(template, inputs):
    def replace(match):
        key = match.group(1)
        value = inputs.get(key, "")
        return value if value else f"<{key}>"
    return PLACEHOLDER_RE.sub(replace, template)
