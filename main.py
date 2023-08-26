import subprocess
import subprocess
from quiz import Quiz_Creator, Quiz
from video import *

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4

pos = {
    "center": ("(w-text_w)/2", "(h-text_h)/2"),
    "top": ("(w-text_w)/2", "(h-text_h)/4"),
    "a1": (),
    "a2": (),
    "a3": (),
    "a4": (),
}


def main():
    # QUIZ
    quiz = Quiz_Creator.prompt_create_quiz()
    # Quiz_Creator.create_quizzes(amount=2, length=3)

    # VIDEO
    add_text(quiz.name, 196, *pos["center"])
    open_video("slides/output")

    # s = create_slide
    # s.add_text


def ffmpeg(args): subprocess.run(["ffmpeg", *args])
def open_video(path): subprocess.run(["vlc", path+".mp4"])

if __name__ == "__main__":
    main()
