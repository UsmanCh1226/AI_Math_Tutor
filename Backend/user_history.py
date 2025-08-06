from collections import defaultdict

class UserHistory:
    def __init__(self):
        self.history = []

    def add(self, parsed_input):
         self.history.append(parsed_input)

    def most_frequent_subject(self):
        counter = defaultdict(int)

        for item in self.history:
            subject = item.get("subject", 'Unknown')
            counter[subject] += 1

            if not counter:
                return None

            # Get the subject with the highest frequency
            most_common = max(counter.items(), key=lambda x: x[1])[0]
            return most_common

        def should_suggest_quiz(self):
            """
            Determines whether a quiz should be suggested based on repeated subject use.

            Returns:
                str or None: The subject that should be quizzed (if seen 3+ times), or None.
            """
            subject = self.most_frequent_subject()
            if not subject:
                return None

            count = sum(1 for item in self.history if item.get("subject") == subject)
            if count >= 3:
                return subject
            return None

