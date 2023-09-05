import json
import subprocess
from pprint import pprint

from quiz import Quiz_Creator
from video import Slide

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def main():
    """MAIN"""
    # QUIZ

    include_title_slide = False
    debug = False
    new_quiz = True

    quiz_questions = {}
    if new_quiz:
        new_quiz = Quiz_Creator.prompt_create_quiz()
        quiz_questions: dict = new_quiz.get_questions()
        new_quiz_name = new_quiz.name
    else:
        new_quiz = open_quiz_dict(input("Select quiz to open: "))
        quiz_questions = new_quiz["questions"]
        new_quiz_name = new_quiz["name"]

    # quizzes = Quiz_Creator.create_quizzes(amount=2, length=3)

    # VIDEO
    if include_title_slide:
        Slide("title", "cubes.mp4", 2).add_title(new_quiz_name)
    if debug:
        pprint(quiz_questions)
    successful_slides = []
    for index, question in enumerate(quiz_questions):
        curr_slide = Slide("q" + str(index + 1), "cubes.mp4", 2)
        if question["type"] != "multiple":
            curr_slide.delete()
            continue

        curr_slide.add_question(
            question["question"],
            question["incorrect_answers"],
            question["correct_answer"],
        )
        successful_slides.append(curr_slide)

    print_slide_status(successful_slides)

    # open_video("slides/title")
    # open_video("slides/q1")


def print_slide_status(slides):
    out_str = "\n" + str(len(slides)) + " slides created: \n"
    for curr_slide in slides:
        if not isinstance(curr_slide, Slide):
            continue
        out_str += str(curr_slide)
    print(out_str[:-1])

def open_quiz_dict(name) -> dict:
    """OPEN QUIZ"""
    quiz_dict = {}
    with open("quizzes/" + name + ".json", "r", encoding="UTF") as file:
        quiz_dict = json.loads(file.read())
    return quiz_dict


def open_video(path):
    """OPEN WITH VLC"""
    subprocess.run(["vlc", path + ".mp4"])


if __name__ == "__main__":
    main()
