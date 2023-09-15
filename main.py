import json
import os
import subprocess
from pprint import pprint

from quiz import Quiz, Quiz_Creator
from video import Slide

INCLUDE_TITLE_SLIDE = False
CREATE_QUESTION_SLIDE = True
BOOLEAN_QUESTIONS = False
CREATE_NEW_QUIZ = True
DEBUG = False


def main():
    """creates quizzes and slides, then adds the questions and answers
    for the quiz to each slide"""

    # CONFIG ##############################################
    create_new_quiz = True if input("Create new quiz? (y/n):") == "y" else False

    # QUIZ ################################################
    if create_new_quiz:
        new_quiz: Quiz = Quiz_Creator.prompt_create_quiz()
    else:
        new_quiz: Quiz = open_quiz(input("Select quiz to open: "))

    # quizzes = Quiz_Creator.create_quizzes(amount=2, length=3)

    if DEBUG:
        pprint(new_quiz)

    # IMAGE ###############################################
    scale_img("img/leopard.jpg", "img/cubes.jpg")

    # VIDEO ###############################################

    # create title slide
    if INCLUDE_TITLE_SLIDE:
        Slide("title", "img/cubes.jpg").add_title(new_quiz.name)

    # create question slides: (question_slide, answer_slide)
    quiz_questions = zip(
        new_quiz.get_prompts(),
        new_quiz.get_guesses(),
        new_quiz.get_answers(),
    )
    question_slides = (
        add_question_slides(quiz_questions) if CREATE_QUESTION_SLIDE else ""
    )
    if not question_slides:
        print("No questions found")
        return

    clean_slides(question_slides)
    create_videos()


def create_videos():
    subprocess.run(["./make_video.sh"])


def add_question_slides(questions):
    question_slides, answer_slides = [], []
    for index, (prompt, guesses, answer) in enumerate(questions):
        question_name = chr(ord("`") + index + 2)  # int -> char

        # create question slide
        question_slide = Slide(question_name + "_a", "img/cubes.jpg")
        if not BOOLEAN_QUESTIONS and len(guesses) <= 3:
            question_slide.delete()
            continue
        question_slide.add_guesses(prompt, guesses)
        question_slides.append(question_slide)

        # create answer slide
        answer_slide = Slide(question_name + "_b", "img/cubes.jpg")
        answer_slide.add_answer(answer)
        answer_slides.append(answer_slide)

    return list(zip(question_slides, answer_slides))


def clean_slides(slides):
    """remove empty slides and print status"""
    print("\n", str(len(slides)), "questions created: \n")
    for q_slide, a_slide in slides:
        if os.path.isfile(q_slide.path) and os.path.isfile(a_slide.path):
            if (
                os.path.getsize("slides/" + q_slide.name + ".jpg") > 0
                and os.path.getsize("slides/" + a_slide.name + ".jpg") > 0
            ):
                print(q_slide.name + " and " + a_slide.name)
                continue

        q_slide.delete()
        a_slide.delete()


def open_quiz(name) -> Quiz:
    """OPEN QUIZ from json"""
    quiz_d = {}
    with open("quizzes/" + name + ".json", "r", encoding="UTF") as file:
        quiz_d = json.loads(file.read())
    quiz = Quiz(quiz_d["name"], quiz_d["length"], quiz_d["category"])
    quiz.add_questions(quiz_d["questions"])
    return quiz


def scale_img(input_path, output_path):
    subprocess.run(["ffmpeg", "-i", input_path, "-vf", "scale=1920:1080", output_path])


if __name__ == "__main__":
    main()
