import requests
import json
import subprocess

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def main():
    Quiz_Creator.prompt_create_quiz()
    # Quiz_Creator.create_quizzes(amount=2, length=3)
    # add_text()


def add_text():
    command = """ -i cubes.mp4 -vf "drawtext=fontfile=OpenSans-BoldItalic.ttf:text='SAMPLE TEXT'" -codec:a copy output.mp4"""
    # command = """-i cubes.mp4 -vf "drawtext=fontfile=OpenSans-BoldItalic.ttf:text='SAMPLE TEXT':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2" -codec:a copy output.mp4"""

    ffmpeg(command)


def ffmpeg(args): subprocess.run(["ffmpeg", args])


class Quiz_Creator:
    def prompt_create_quiz():
        name = input("Enter quiz name: ")
        length = input("Enter quiz length: ")
        Quiz_Creator.list_categories()
        Quiz_Creator.create_quiz(name, length, input("Enter category number: "))

    def list_categories():
        with open("categories.json", "r") as f:
            for c in json.loads(f.read())[0]["trivia_categories"]:
                print(c["id"], "-", c["name"])

    def create_quizzes(name: str = "quiz", amount: int = 1, length: int = 1, category: int = 9):
        quizzes = []
        for i in range(0, amount):
            quizzes.append(Quiz_Creator.create_quiz(name+"_"+str(i+1), length, category))
        return quizzes

    def create_quiz(name: str, length: int, category: int):
        q = Quiz(name, length, category)
        q.get_questions()
        q.save_json_file()
        return q


class Quiz:
    def __init__(self, name: str = "quiz", length: int = 1, category: int = 9):
        self.name: str = name
        self.length: int = length
        self.category: int = category
        self.questions_json: str = None

    def get_questions(self):
        """makes a request, then returns and saves the json response"""
        self.questions_json = requests.get(
            "https://opentdb.com/api.php?amount="+str(self.length) +
            "&category="+str(self.category)
        ).json()["results"]
        return self.questions_json

    def save_json_file(self):
        with open("quizzes/"+self.name+".json", "w") as f:
            f.write(json.dumps(vars(self)))


if __name__ == "__main__":
    main()
