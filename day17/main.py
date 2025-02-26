from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

question_bank =[]


for data in question_data:
    question_bank.append(Question(data["text"], data["answer"]))

quiz_brain = QuizBrain(question_bank)

while quiz_brain.still_has_question():
    quiz_brain.next_question()

print("You've completed the quiz")
quiz_brain.print_score()