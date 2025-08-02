import re
from collections import defaultdict


KEYWORDS = {
    "calculus": [
        "derivative", "differentiate", "find the derivative", "take the derivative",
        "rate of change", "integrate", "antiderivative"
    ],
    "algebra": [
        "solve", "simplify", "expand", "factor", "equation", "expression"
    ],
    "geometry": [
        "area", "perimeter", "volume", "triangle", "circle", "rectangle"
    ],
    "trigonometry": [
        "sin", "cos", "tan", "cot", "trig", "sine", "cosine", "tangent"
    ],
    "linear_algebra": [
        "matrix", "matrices", "determinant", "inverse", "eigen", "eigenvalue"
    ],
    "statistics": [
        "mean", "median", "mode", "probability", "variance", "standard deviation"
    ]
}


WORD_TO_SYMBOL = {
    "plus": "+", "minus": "-", "times": "*", "multiplied by": "*",
    "divided by": "/", "over": "/", "equals": "=", "equal to": "=",
    "is equal to": "=", "is": "=", "to the power of": "**"
}


FRACTIONS = {
    "one half": 0.5,
    "one third": 1/3,
    "one fourth": 0.25,
    "three fourths": 0.75,
    "two thirds": 2/3
}


NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90
}



def word_to_number(text):
    """
    Converts written-out numbers and fractions into numeric digits.
    Example: "twenty one" -> "21", "one half" -> "0.5"
    """

    def parse_compound_number(match):
        words = match.group(0).split()
        total = 0
        for word in words:
            if word in NUMBER_WORDS:
                total += NUMBER_WORDS[word]
        return str(total)

    # Replace compound numbers like "twenty one"
    text = re.sub(
        r'\b(' + '|'.join(NUMBER_WORDS.keys()) + r')(\s+(' + '|'.join(NUMBER_WORDS.keys()) + r'))?\b',
        parse_compound_number,
        text
    )

    # Replace fraction phrases like "one half"
    for phrase, value in FRACTIONS.items():
        text = re.sub(rf'\b{re.escape(phrase)}\b', str(value), text)

    # Handle negatives like "negative five"
    text = re.sub(r'\bnegative (\d+(\.\d+)?)', r'-\1', text)

    return text



def normalize_language(text):
    """
    Removes filler words and noise from natural language questions.
    Example: "Can you solve the equation" → "solve equation"
    """
    filler_words = [
        "the", "this", "that", "a", "an", "my", "your", "his", "her",
        "please", "could you", "would you", "can you", "tell me", "show me"
    ]
    for word in filler_words:
        text = re.sub(r'\b' + re.escape(word) + r'\b', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_expression(user_input):
    """
    Converts user input into a clean, math-friendly expression.
    Handles powers, multiplication, equality, and numeric conversions.
    """
    cleaned = normalize_language(user_input.lower())         # Step 1: Remove noise
    cleaned = word_to_number(cleaned)                        # Step 2: Convert numbers

    cleaned = re.sub(r"(\b\w+)\s+squared", r"\1**2", cleaned)  # Handle "x squared"
    cleaned = re.sub(r"(\b\w+)\s+cubed", r"\1**3", cleaned)    # Handle "x cubed"

    # Step 3: Replace words with operators
    for phrase, symbol in sorted(WORD_TO_SYMBOL.items(), key=lambda x: -len(x[0])):
        cleaned = re.sub(r'\b' + re.escape(phrase) + r'\b', f' {symbol} ', cleaned)

    # Step 4: Remove common math verbs
    cleaned = re.sub(
        r"^(differentiate|integrate|solve|simplify|calculate|find|evaluate|what is|show)",
        '', cleaned
    ).strip()

    # Step 5: Handle implicit multiplication (e.g., 2x → 2*x)
    cleaned = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', cleaned)
    cleaned = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', cleaned)
    cleaned = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', cleaned)
    cleaned = re.sub(r'(\d|\w)\s*\(', r'\1*(', cleaned)

    return re.sub(r'\s+', ' ', cleaned).strip()



def classify_subject(user_input):
    """
    Determines the math subject most relevant to the input based on keyword matches.
    """
    input_lower = user_input.lower()
    subject_scores = defaultdict(int)

    for subject, keywords in KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', input_lower):
                subject_scores[subject] += 1

    if not subject_scores:
        return "Unknown"

    return max(subject_scores.items(), key=lambda x: x[1])[0]



def parse_user_input(user_input):
    """
    Orchestrates classification, expression extraction, and step-by-step detection.

    Returns:
        dict with:
            - subject: str
            - expression: str
            - step_by_step: bool
    """
    subject = classify_subject(user_input)
    expression = extract_expression(user_input)

    step_mode = any(
        kw in user_input.lower()
        for kw in ["explain", "steps", "step by step", "show work", "show the steps"]
    )

    return {
        "subject": subject,
        "expression": expression,
        "step_by_step": step_mode
    }



if __name__ == "__main__":
    example_input = "Can you please solve x squared plus five equals ten and show the steps?"

    result = parse_user_input(example_input)

    print("User Input:", example_input)
    print("Subject:", result["subject"])
    print("Expression:", result["expression"])
    print("Step-by-step requested?", result["step_by_step"])
