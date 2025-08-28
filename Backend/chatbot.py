from nlp_parser import parse_user_input
from math_engine import route_problem
from user_history import save_user_query
d

def chatbot_response(user_input):
    """
    Processes user input and returns the AI tutor's response.

    Parameters:
    -----------
    user_input : str
        The raw question entered by the user (e.g., "Solve 2x^2 + 3x + 1 = 0").

    Returns:
    --------
    str
        The chatbot's answer.
    """

    parsed = parse_user_input(user_input)

    save_user_query(user_input, parsed)

    result = route_problem(parsed)

    return result

if __name__ == "__main__":
    print("🤖 AI Math Tutor is ready! Type 'quit' to exit.")
    while True:
        user_question = input("You: ")
        if user_question.lower() in ["quit", "exit"]:
            print("AI Tutor: Goodbye! Keep learning 📚")
            break

        answer = chatbot_response(user_question)
        print(f"AI Tutor: {answer}")