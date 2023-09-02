import json
import subprocess

from quiz import Quiz_Creator
from video import Slide

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def main():
    """MAIN"""
    # QUIZ

    quiz = open_quiz("Sports")
    # quiz = Quiz_Creator.prompt_create_quiz()
    # quizzes = Quiz_Creator.create_quizzes(amount=2, length=3)

    # VIDEO

    Slide("title", "cubes.mp4").add_title(quiz["name"])
    slide = Slide("q1", "cubes.mp4")

    q_1 = quiz["questions_json"][0]
    slide.add_question(q_1["question"], q_1["incorrect_answers"], q_1["correct_answer"])

    open_video("slides/title")
    open_video("slides/q1")


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
