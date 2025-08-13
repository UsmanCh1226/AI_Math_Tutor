import re

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}

FRACTIONS = {
    "one half": 0.5, "one third": 1/3, "two thirds": 2/3,
    "one fourth": 0.25, "three fourths": 0.75,
}

WORD_TO_SYMBOL = {
    "plus": "+", "minus": "-", "times": "*", "multiplied by": "*",
    "divided by": "/", "over": "/", "equals": "=", "equal to": "=",
    "is equal to": "=", "to the power of": "**", "power of": "**",
}

POWER_WORDS = {
    "squared": "**2", "cubed": "**3",
}

FILLER = [
    "please", "can you", "could you", "would you", "show me", "tell me",
    "calculate", "compute", "evaluate", "find", "solve", "determine",
]


def _replace_number_words(text: str) -> str:
    """Convert simple number words + common two-word fractions to digits."""
    # fractions first (to avoid splitting their words)
    for phrase, val in FRACTIONS.items():
        text = re.sub(rf"\b{re.escape(phrase)}\b", str(val), text, flags=re.IGNORECASE)

    # compound numbers like "twenty one"
    def repl(match):
        words = match.group(0).split()
        total = 0
        for w in words:
            if w in NUMBER_WORDS:
                total += NUMBER_WORDS[w]
        return str(total)

    pattern = r"\b(" + "|".join(NUMBER_WORDS.keys()) + r")(?:\s+(" + "|".join(NUMBER_WORDS.keys()) + r"))?\b"
    return re.sub(pattern, lambda m: repl(m).lower(), text, flags=re.IGNORECASE)


def _replace_power_words(text: str) -> str:
    """x squared → x**2 ; y cubed → y**3"""
    text = re.sub(r"\b([a-zA-Z])\s+squared\b", r"\1**2", text)
    text = re.sub(r"\b([a-zA-Z])\s+cubed\b", r"\1**3", text)
    return text


def _replace_word_symbols(text: str) -> str:
    """Map word operators to symbols (plus→+, divided by→/ …)."""
    # longest phrases first to avoid partial matches
    for phrase, sym in sorted(WORD_TO_SYMBOL.items(), key=lambda kv: -len(kv[0])):
        text = re.sub(rf"\b{re.escape(phrase)}\b", f" {sym} ", text, flags=re.IGNORECASE)
    return text


def _strip_fillers(text: str) -> str:
    for w in FILLER:
        text = re.sub(rf"\b{re.escape(w)}\b", " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def _insert_implicit_multiplication(text: str) -> str:
    """
    2x → 2*x ; xy → x*y ; 3(x+1) → 3*(x+1) ; x(…)-> x*(…)
    """
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'(\d|\w)\s*\(', r'\1*(', text)
    return text


def normalize_math_text(user_input: str) -> str:
    """Full normalization pipeline."""
    s = user_input.strip()
    s = _strip_fillers(s)
    s = _replace_number_words(s)
    s = _replace_power_words(s)
    s = _replace_word_symbols(s)
    s = _insert_implicit_multiplication(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def detect_variables(expression: str) -> list:
    """Return sorted unique variable names (single letters)."""
    vars_found = sorted(set(re.findall(r"[a-zA-Z]", expression)))
    return vars_found


def split_multi_steps(user_input: str) -> list:

    # normalize connectors to '||'
    tmp = re.sub(r"\b(and then|then|after that|next)\b", "||", user_input, flags=re.IGNORECASE)
    steps = [s.strip(" ,.") for s in tmp.split("||") if s.strip(" ,.")]
    return steps
