import re
from collections import defaultdict



KEYWORDS = {
    "calculus": [
        "derivative", "differentiate", "find the derivative",
        "take the derivative", "rate of change", "integrate", "antiderivative"
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


def classify_subject(user_input):
    """
    Detects the most likely math subject based on keyword matches.

    Args:
        user_input (str): The raw question from the user.

    Returns:
        str: One of the keys from KEYWORDS, or 'Unknown' if no match.
    """
    input_lower = user_input.lower()
    subject_scores = defaultdict(int)

    for subject, keywords in KEYWORDS.items():
        for keyword in keywords:
            # Check for whole-word match (e.g., "mean", not "meaning")
            if re.search(r"\b" + re.escape(keyword) + r"\b", input_lower):
                subject_scores[subject] += 1

    if not subject_scores:
        return "Unknown"

    # Return the subject with the most matched keywords
    return max(subject_scores.items(), key=lambda x: x[1])[0]


def word_to_number(text):

    number_words = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
        "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
        "eighteen": "18", "nineteen": "19", "twenty": "20",
        "thirty": "30", "forty": "40", "fifty": "50", "sixty": "60",
        "seventy": "70", "eighty": "80", "ninety": "90",
        "hundred": "100", "thousand": "1000",
        "one half": "0.5", "one third": "1/3", "one fourth": "0.25"
    }

    # Replace longer phrases (e.g. "one half") first
    for word_phrase in sorted(number_words, key=lambda x: -len(x)):
        pattern = r'\b' + re.escape(word_phrase) + r'\b'
        text = re.sub(pattern, number_words[word_phrase], text)

    return text


def extract_expression(user_input):
    """
    Converts verbal math into symbolic math (e.g., "plus" → "+").
    Handles things like "x squared", "three times x", etc.

    Args:
        user_input (str): Raw question from user

    Returns:
        str: Cleaned, math-friendly expression
    """

    cleaned = user_input.lower()
    cleaned = word_to_number(cleaned)

    cleaned = re.sub(r"(\b\w+)\s+squared", r"\1**2", cleaned)
    cleaned = re.sub(r"(\b\w+)\s+cubed", r"\1**3", cleaned)

    cleaned = cleaned.replace("^", "**")

    word_to_symbol = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied by": "*",
        "divided by": "/",
        "over": "/",
        "equals": "=",
        "equal to": "=",
        "is": "=",
        "to the power of": "**"
    }

    # Sort by length so multi-word phrases like "multiplied by" are replaced first
    for word, symbol in sorted(word_to_symbol.items(), key=lambda x: -len(x[0])):
        cleaned = re.sub(r"\b" + re.escape(word) + r"\b", f" {symbol} ", cleaned)

    # Step 4: Remove common leading words
    cleaned = re.sub(r"^(differentiate|integrate|solve|simplify|calculate|find|what is|evaluate|show)\b", '', cleaned).strip()

    cleaned = re.sub(r"\s+", " ", cleaned)

    #Implicit Multiplication
    cleaned = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', cleaned)
    cleaned = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', cleaned)

    # Rule: variable next to variable → xy → x*y (optional, toggle if needed)
    cleaned = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', cleaned)

    # Rule: digit or variable before parenthesis → 2(x+1) or x(x+1) → 2*(x+1)
    cleaned = re.sub(r'(\d|\w)\s*\(', r'\1*(', cleaned)

    return cleaned.strip()

    return cleaned.strip()





def parse_user_input(user_input):
    """
    Orchestrates the full parsing pipeline:
    1. Detect subject (e.g., 'calculus')
    2. Extract expression (e.g., 'x**2')
    3. Detect whether step-by-step explanation is requested

    Args:
        user_input (str): The raw user message.

    Returns:
        dict: {
            "subject": str,
            "expression": str,
            "step_by_step": bool
        }
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
