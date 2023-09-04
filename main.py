import json
import subprocess

from quiz import Quiz_Creator
from video import Slide

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def main():
    """MAIN"""
    # QUIZ

    prompt = True

    quiz_questions = None
    if prompt:
        quiz = Quiz_Creator.prompt_create_quiz()  # obj
        quiz_questions = quiz.get_questions()  # obj -> json
    else:
        quiz_questions = open_quiz("Sports")  # json

    # quizzes = Quiz_Creator.create_quizzes(amount=2, length=3)

    # VIDEO
    # Slide("title", "cubes.mp4").add_title(quiz["name"])

    for index, question in enumerate(quiz["questions_json"]):
        curr_slide = Slide("q" + str(index + 1), "cubes.mp4")
        if question["type"] == "multiple":
            curr_slide.add_question(
                question["question"],
                question["incorrect_answers"],
                question["correct_answer"],
            )
        else:
            curr_slide.delete()

    # open_video("slides/title")
    # open_video("slides/q1")
    # open_video("slides/q1")


def open_quiz(name):
    """OPEN QUIZ"""
    quiz = None
    with open("quizzes/" + name + ".json", "r", encoding="UTF") as file:
        quiz = json.loads(file.read())
    return quiz


def open_video(path):
    """OPEN WITH VLC"""
    subprocess.run(["vlc", path + ".mp4"])


if __name__ == "__main__":
    main()
