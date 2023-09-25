import html
import json
import os
import subprocess

from quiz import Quiz, QuizCreator
from video import Slide

# from youtube_upload.client import YoutubeUploader


AUDIO_FILE = "../audio/break1.mp3"
BOOLEAN_QUESTIONS = False
CREATE_NEW_QUIZ = True
DEBUG = False


def main():
    """Menu"""

    new_quiz = get_quiz()
    video_from_quiz_data(new_quiz)


def video_from_quiz_data(quiz: Quiz):
    """creates a quiz video"""
    slide_data = quiz.get_slide_data()
    background = get_background_image()

    if input("\nCreate title slide? (y/n): ") == "y":
        Slide("title", background).add_title(quiz.name)

    question_slides = create_question_slides(slide_data, background)
    clean_slides(question_slides)
    print("\nCreating question slides:\n")
    create_video(quiz.name)

    if input("Upload new video? (y/n): ") == "y":
        upload(quiz.name)


def get_quiz():
    new_quiz = (
        QuizCreator.prompt_create_quiz()
        if input("Create new quiz? (y/n): ") == "y"
        else open_quiz_from_json(
            input(list_saved_quizzes() + "\nSelect quiz to open: ")
        )
    )
    print("")
    return new_quiz


def create_question_slides(questions, background):
    question_slides, answer_slides = [], []
    for index, (prompt, guesses, answer) in enumerate(questions):
        question_name = chr(ord("`") + index + 2)  # int -> char

        prompt = html.unescape(prompt)
        for guess in guesses:
            guess = html.unescape(guess)
        answer = html.unescape(answer)

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
    print("\n", str(len(slides) / 2), "questions created: \n")
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
    return list_files("quizzes/", "Quizzes", False)


def list_saved_images() -> str:
    return list_files("img/", "Images", True)


def list_files(path, title, show_ext):
    files: str = ""
    print("\n%s:" % title)
    for _, _, filenames in os.walk(path):
        for index, filename in enumerate(filenames):
            files += (
                str(index + 1)
                + " - "
                + (filename if show_ext else filename.split(".")[0])
                + "\n"
            )
    return files


def get_background_image():
    print(list_saved_images())
    # return convert_to_png(scale_img("img/" + input("Select background: ") + ".jpg"))
    return "img/" + input("Select background: ")


def scale_img(input_path):
    output_path = input_path.split(".")[0] + "_1080.jpg"
    subprocess.run(
        ["ffmpeg", "-i", input_path, "-vf", "scale=1920:1080", "-y", output_path]
    )
    return output_path


def convert_to_png(input_path):
    file = input_path.split(".")[0] + ".png"
    subprocess.run(["ffmpeg", "-i", input_path, "-y", file])
    return file


def upload(name: str):
    subprocess.run(["./upload.sh", name])


if __name__ == "__main__":
    main()
