from nlp_parser import parse_user_input
from math_solver import solve_expression
from user_history import UserHistory
from question_generator import generate_question

def chatbot():
    print("🧠 MathBot: Ask me any math question (e.g. 'solve x² + 5 = 10')")
    print("Type 'quit' to exit.\n")

    history = UserHistory()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit']:
            print("👋 MathBot: Goodbye!")
            break

        # Step 1: Parse input (detect subject, expression, step-by-step mode)
        parsed = parse_user_input(user_input)

        # Step 2: Solve the math question using the correct subject solver
        result = solve_expression(parsed)

        # Step 3: Show the result to the user
        print(f"\n🧠 MathBot:\n{result}\n")

        # Step 4: Add this interaction to the user's history
        history.add(parsed)

        # Step 5: Check if quiz should be suggested based on subject repetition
        subject_to_quiz = history.should_suggest_quiz()
        if subject_to_quiz:
            print(f"📚 You've asked a lot of {subject_to_quiz} questions.")
            print("Would you like to try a quick quiz on that topic? (yes/no)")

            answer = input("> ").strip().lower()
            if answer in ["yes", "y"]:
                quiz_q = generate_question(subject_to_quiz)
                print(f"\n🎯 Quiz time!\n{quiz_q['question']}")
                user_ans = input("Your answer: ").strip()

                if user_ans == quiz_q['answer']:
                    print("✅ Correct!\n")
                else:
                    print(f"❌ Nope. The correct answer is: {quiz_q['answer']}\n")

if __name__ == "__main__":
    chatbot()
