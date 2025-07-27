
from nlp_parser import extract_expression, parse_user_input
from math_solver import solve_expression

def chatbot():
    print("🧠 MathBot: Ask me a math question! (Type 'quit' to exit)")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit']:
            print("MathBot: Goodbye!")
            break

        parsed = parse_user_input(user_input)

        result = solve_expression(parsed)

        print(f"MathBot: {result}")
