import json
import os
import subprocess
import sys
from pprint import pprint

from quiz import Quiz, QuizCreator
from video import Slide

AUDIO_FILE = "../audio/break1.mp3"
BOOLEAN_QUESTIONS = False
CREATE_NEW_QUIZ = True
DEBUG = False


def main():
    """creates a quiz video"""

    new_quiz = get_quiz()
    quiz_data = new_quiz.get_slide_data()

    if DEBUG:
        pprint(quiz_data)

    background = convert_to_png(
        scale_img("img/" + input("Select background: ") + ".jpg")
    )

    if input("\nCreate title slide?(y/n): ") == "y":
        Slide("title", background).add_title(new_quiz.name)

    question_slides = add_question_slides(quiz_data, background)
    clean_slides(question_slides)
    create_video(new_quiz.name)


def get_quiz():
    new_quiz = (
        QuizCreator.prompt_create_quiz()
        if input("Create new quiz? (y/n): ") == "y"
        else open_quiz_from_json(
            input(list_saved_quizzes() + "\n" + "Select quiz to open: ")
        )
    )
    return new_quiz


def add_question_slides(questions, background):
    question_slides, answer_slides = [], []
    for index, (prompt, guesses, answer) in enumerate(questions):
        question_name = chr(ord("`") + index + 2)  # int -> char

        # create question slide
        question_slide = Slide(question_name + "_a", background)
        if not BOOLEAN_QUESTIONS and len(guesses) <= 3:
            question_slide.delete()
            continue
        question_slide.add_guesses(prompt, guesses)
        question_slides.append(question_slide)

        # create answer slide
        answer_slide = Slide(question_name + "_b", background)
        answer_slide.add_answer(answer)
        answer_slides.append(answer_slide)

    return list(zip(question_slides, answer_slides))


def clean_slides(slides):
    """remove empty slides and print status"""
    print("\n", str(len(slides)), "questions created: \n")
    for q_slide, a_slide in slides:
        if os.path.isfile(q_slide.path) and os.path.isfile(a_slide.path):
            if (
                os.path.getsize("slides/" + q_slide.name + ".png") > 0
                and os.path.getsize("slides/" + a_slide.name + ".png") > 0
            ):
                print(q_slide.name + " and " + a_slide.name)
                continue

        q_slide.delete()
        a_slide.delete()


def create_video(title):
    """execute make_video.sh"""
    subprocess.run(["./make_video.sh", title, AUDIO_FILE])


def open_quiz_from_json(name) -> Quiz:
    """create Quiz object from a json file in the quizzes directory"""
    quiz_d = {}
    with open("quizzes/" + name + ".json", "r", encoding="UTF") as file:
        quiz_d = json.loads(file.read())
    quiz = Quiz(quiz_d["name"], quiz_d["length"], quiz_d["category"])
    quiz.add_questions(quiz_d["questions"])
    return quiz


def list_saved_quizzes() -> str:
    """  returns list a of quizzes as a string """
    names: str = ""
    print("\nQuizzes:")
    for index, (_, _, filenames) in enumerate(os.walk("quizzes/")):
        for filename in filenames:
            names += str(index + 1) + ". " + filename.split(".")[0] + "\n"
    return names


def list_saved_images() -> str:
    return ""


def scale_img(input_path):
    output_path = input_path.split(".")[:-1][0] + "_1080.jpg"
    subprocess.run(
        ["ffmpeg", "-i", input_path, "-vf", "scale=1920:1080", "-y", output_path]
    )
    return output_path


def convert_to_png(input_path):
    file = input_path.split(".")[:-1][0] + ".png"
    subprocess.run(["ffmpeg", "-i", input_path, "-y", file])
    return file


if __name__ == "__main__":
    if len(sys.argv) == 3:  # main.py name background
        Slide("title", sys.argv[2]).add_title(sys.argv[1])
        args = "ffmpeg -y -loop 1 -i slides/title.png -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 3 -c:v libx264 -t 3 -pix_fmt yuv420p -vf scale=1920:1080 -y output/title.mpeg"
        subprocess.run(args.split(" "))
    else:
        main()
