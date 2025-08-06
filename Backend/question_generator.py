import random
from sympy import symbols, simplify, diff, integrate

x = symbols('x')


def generate_question(subject):
    """
    Generates a math question and its answer based on the given subject.

    Returns:
        dict: { "question": str, "answer": str }
    """

    if subject == "algebra":
        templates = [
            lambda: {
                "question": "Solve: 2x + 5 = 13",
                "answer": "4"
            },
            lambda: {
                "question": "What is x if 3x = 12?",
                "answer": "4"
            },
            lambda: {
                "question": "Factor: x² - 9",
                "answer": "(x - 3)(x + 3)"
            },
            lambda: {
                "question": "Simplify: (x + 2)(x - 2)",
                "answer": simplify((x + 2) * (x - 2)).__str__()
            }
        ]

    elif subject == "calculus":
        templates = [
            lambda: {
                "question": "Differentiate: x²",
                "answer": diff(x ** 2, x).__str__()
            },
            lambda: {
                "question": "What is the derivative of sin(x)?",
                "answer": "cos(x)"
            },
            lambda: {
                "question": "Integrate: x",
                "answer": integrate(x, x).__str__() + " + C"
            },
            lambda: {
                "question": "Find the antiderivative of x²",
                "answer": integrate(x ** 2, x).__str__() + " + C"
            }
        ]

    else:
        # fallback if no subject match
        return {
            "question": "Sorry, I don't have questions for that subject yet.",
            "answer": ""
        }

    return random.choice(templates)()
