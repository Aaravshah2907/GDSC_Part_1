import random
import json
import csv
import os
import datetime


class Question:
    # Initializing variables used in this class
    def __init__(self, text, answer):
        self.text = text
        # Accepting the first letter of the response only to make it more user-friendly.
        self.answer = answer[0].lower()

    def is_correct(self, user_answer):
        # Converting user's response from boolean to True / False
        if user_answer[0] == "0":
            user_answer == 'False'
        elif user_answer[0] == "1":
            user_answer == 'True'
        # Returning if the answer provided by the user is correct or not.
        return self.answer == user_answer.lower()


class Quiz:
    # Initializing Variables used in this class
    def __init__(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.score = 0

    # Going to next Question
    def next_question(self):
        # Checking if the we have completed the list of questions or not.
        if self.current_question_index >= len(self.questions):
            return None

        #  If not, we will go to next question in the list and update the index number of the question for next loop
        current_question = self.questions[self.current_question_index]
        self.current_question_index += 1

        return current_question

    def check_answer(self, user_answer):
        '''
        We will check if the answer provided to us by the user is correct or not.
        NOTE: We use self.current_question_index - 1 as we have updated the index number in the next_question.
        '''
        current_question = self.questions[self.current_question_index - 1]

        # Let's prevent the user from skipping the question or providing us with Arbitary or random answer.
        if len(user_answer) > 0:
            if user_answer.lower()[0] != 't' and user_answer.lower()[0] != 'f' and user_answer[0] != '1' and user_answer[0] != '0':
                self.current_question_index -= 1

            # Updating User's Score
            elif current_question.is_correct(user_answer):
                self.score += 2
            else:
                self.score -= 1
        else:
            self.current_question_index -= 1

    def do_questions_remain(self):
        # Checking if questions are remaining
        return self.current_question_index < len(self.questions)

    def get_score(self):
        # Returning User's Score for the final
        return self.score


# Load the questions from the questions.py file provided by the Admin
with open("questions.py", "r") as file:
    question_data = json.load(file)

# Create a list of Question objects from the data acquired from questions.py file
questions = []
for question in question_data:
    questions.append(Question(question["text"], question["answer"]))

# Randomizes the list of questions provided
random.shuffle(questions)

# Create a Quiz object
quiz = Quiz(questions)

# Gives a set of rules for the user to stick to -
print("""Here are the set of rules the user has to stick to:
      1. Correct Answer can be marked via - 't', 'T', '1'.
      2. Wrong Answer can be marked via - 'f', 'F', '0'.
      3. No other response will be accepted.
      4. You can't skip any questions, all questions are compulsory to attend. Without attempting the current question, you may not proceed further.
      5. Your name shall be collected and your total score stored in the 'Leaderboard.csv' file. 
      """)

name = input("Enter Your Name for the database: ")

# Start the quiz
while quiz.do_questions_remain():
    # Get the next question
    current_question = quiz.next_question()

    # Print the question
    print(current_question.text)

    # Get the user's answer
    user_answer = input("True or False? ")

    # Check the answer
    quiz.check_answer(user_answer)

# Display the final score
print(f"Your final score is: {quiz.get_score()}")

today = datetime.datetime.now()
today_date = today.strftime("%b-%d-%Y")

now_time = today.strftime("%H:%M:%S")

path = r'\Leaderboard.csv'
if os.path.exists(path):
    pass
else:
    with open('Leaderboard.csv', 'w', newline='') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=[
                                'date', 'time', 'name', 'score'])
        writer.writerow({'date': 'Date', 'time': "Time",
                        "name": 'Name', 'score': 'Score'})

with open('Leaderboard.csv', 'a+', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'time', 'name', 'score'])
    writer.writerow({'date': today_date, 'time': now_time, "name": name,
                    'score': quiz.get_score()})
