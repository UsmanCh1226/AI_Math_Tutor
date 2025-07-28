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
        Tries to detect what kind of math question the user is asking.
        It checks if any known keywords are in the input, like "integrate" or "area".

        :param user_input: The user's full text question (e.g. "Differentiate x squared")
        :return: A string like "calculus", "algebra", etc., or "unknown" if it can't tell.
        """
    input_lower = user_input.lower()
    subject_scores = defaultdict(int)


    for subject, keywords in KEYWORDS.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", input_lower):
                subject_scores[subject] += 1

    if not subject_scores:
        return "Unknown"

    return max(subject_scores.items(), key=lambda x: x[1])[0]


def extract_expression(user_input):
    """
        Tries to pull out the math expression from the user's sentence.
        For example, "Differentiate x squared" → "x**2"

        :param user_input: The user's full question
        :return: Just the math part as a string (e.g., "x**2" or "2*x + 1")
        """
    cleaned = user_input.lower()

    cleaned = cleaned.replace("^", "**")

    cleaned = re.sub(r"(\b\w+)\s+squared", r"\1**2", cleaned)
    cleaned = re.sub(r"(\b\w+)\s+cubed", r"\1**3", cleaned)

    match = re.search(r"(?:of|:)?\s*(.+)", cleaned)
    if match:
        return match.group(1).strip()
    else:
        return ""

def parse_user_input(user_input):
    """
        Parses the user input to identify the subject and extract the math expression.

        :param user_input: The user's full question (e.g. "Differentiate x squared")
        :return: A dictionary like {"subject": "calculus", "expression": "x**2"}
        """

    subject = classify_subject(user_input)
    expression = extract_expression(user_input)

    step_mode = any(kw in user_input.lower() for kw in ["explain", "steps", "step by step", "show work"])

    return {
        "subject": subject,
        "expression": expression,
        "step_by_step": step_mode
    }