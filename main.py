import json
import os
import subprocess
from pprint import pprint

from quiz import Quiz_Creator
from video import Slide

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def main():
    """creates quizzes and slides, then adds the questions and answers
    for the quiz to each slide"""

    # CONFIG ##############################################
    new_quiz = True
    include_title_slide = True
    title_duration = 5
    create_question_slides = True
    debug = False

    # QUIZ ################################################
    quiz_questions = {}
    if new_quiz:  # TODO should make new Quiz object even if not a new quiz
        new_quiz = Quiz_Creator.prompt_create_quiz()
        quiz_questions: dict = new_quiz.get_questions()
        new_quiz_name = new_quiz.name
    else:
        new_quiz = open_quiz_dict(input("Select quiz to open: "))
        quiz_questions = new_quiz["questions"]
        new_quiz_name = new_quiz["name"]

    # quizzes = Quiz_Creator.create_quizzes(amount=2, length=3)
    if debug:
        pprint(quiz_questions)

    # IMAGE ###############################################
    scale_img("img/cubes_small.jpg", "img/cubes.jpg")

    # VIDEO ###############################################

    # create title
    if include_title_slide:
        Slide("title", "img/cubes.jpg", "bg_video/cube2.mp4", title_duration).add_title(
            new_quiz_name
        )

    # create question slides: (question_slide, answer_slide)
    # TODO get answers out of quiz_questions to make it (quiz_questions: [""], quiz_answers: [""])
    question_slides = (
        set(add_question_slides(quiz_questions)) if create_question_slides else ""
    )
    if not question_slides:
        print("No questions found")
        return

    # remove empty slides and print status
    print_slide_status(question_slides)
    for q_slide, a_slide in question_slides:
        if os.path.getsize("slides/" + q_slide.name + ".mp4") > 0:
            pprint(q_slide.name + " and " + a_slide.name)
        else:
            q_slide.delete()

    # open_video("slides/title")
    # open_video("slides/q1")


def add_question_slides(questions, q_duration=1, a_duration=1):
    question_slides, answer_slides = [], []
    for index, question_tuple in enumerate(questions):
        question, answer = question_tuple
        # create question slide
        question_slide = Slide(
            "q" + str(index + 1), "img/cubes.jpg", "bg_video/cubes_q.mp4", q_duration
        )
        if question["type"] != "multiple":
            question_slide.delete()
            continue
        question_slide.add_question(question)
        question_slides.append(question_slide)

        # create answer slide
        answer_slide = Slide(
            "a" + str(index + 1), "img/cubes.jpg", "bg_video/cubes_a.mp4", a_duration
        )

        answer_slide.add_answer(answer)
        answer_slides.append(answer_slide)

    return zip(question_slides, answer_slides)


def print_slide_status(slides):
    out_str = "\n" + str(len(slides)) + " questions created: \n"
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


def scale_img(input_path, output_path):
    subprocess.run(["ffmpeg", "-i", input_path, "-vf", "scale=1920:1080", output_path])


if __name__ == "__main__":
    main()
