import re

KEYWORDS = {
"calculus": ["derivative", "differentiate", "integrate", "antiderivative", "rate of change"],
    "algebra": ["solve", "simplify", "expand", "factor"],
    "geometry": ["area", "perimeter", "volume", "triangle", "circle"],
    "trigonometry": ["sin", "cos", "tan", "cot", "trig"],
    "linear_algebra": ["matrix", "determinant", "inverse", "eigen"],
    "statistics": ["mean", "median", "mode", "probability", "variance"]
}

def classify_subject(user_input):
    """
        Tries to detect what kind of math question the user is asking.
        It checks if any known keywords are in the input, like "integrate" or "area".

        :param user_input: The user's full text question (e.g. "Differentiate x squared")
        :return: A string like "calculus", "algebra", etc., or "unknown" if it can't tell.
        """
    input_lower = user_input.lower()

    for subject, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in input_lower:
                return subject

    return "Unknown"

def extract_expression(user_input):
    """
        Tries to pull out the math expression from the user's sentence.
        For example, "Differentiate x squared" → "x**2"

        :param user_input: The user's full question
        :return: Just the math part as a string (e.g., "x**2" or "2*x + 1")
        """
    cleaned = user_input.lower()

    cleaned = cleaned.replace("squared", "x**2").replace("cubed", "x**3")

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

    return {
        "subject": subject,
        "expression": expression
    }

