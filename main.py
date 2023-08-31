import subprocess
import json
from quiz import Quiz_Creator, Quiz
from video import Slide

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def main():
    # QUIZ

    quiz = open_quiz("Sports")
    # quiz = Quiz_Creator.prompt_create_quiz()
    # quizzes = Quiz_Creator.create_quizzes(amount=2, length=3)
        
    # VIDEO

    s = Slide("cubes.mp4")
    s.add_title(quiz["name"])
    # s.add_question(quiz.question, quiz.incorrect, quiz.correct)

    open_video("slides/output")

def open_quiz(name):
    quiz = None
    with open("quizzes/"+name+".json") as f:
        quiz = json.loads(f.read())
    return quiz

def open_video(path): subprocess.run(["vlc", path+".mp4"])


if __name__ == "__main__":
    main()
