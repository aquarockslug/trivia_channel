import requests
import json
import subprocess


def main():
    list_categories()
    category = input("Enter category number: ")
    create_quizzes(2, 3, category)

    #command = """-i cubes.mp4 -vf "drawtext=fontfile=OpenSans-BoldItalic.ttf:text='SAMPLE TEXT':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2" -codec:a copy output.mp4"""
    #ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4

    command = """ -i cubes.mp4 -vf "drawtext=fontfile=OpenSans-BoldItalic.ttf:text='SAMPLE TEXT'" -codec:a copy output.mp4"""

    #ffmpeg(command)


def list_categories():
    with open("categories.json", "r") as f:
        for c in json.loads(f.read())[0]["trivia_categories"]:
            print(c["id"], "-", c["name"])


def ffmpeg(args): subprocess.run(["ffmpeg", args])


def create_quizzes(amount: int = 1, length: int = 1, category: int = 9):
    quizzes = []
    for i in range(0, amount):
        q = Quiz("quiz_"+str(i), length, category)
        q.get_questions()
        quizzes.append(q)
        q.save_json_file()
    return quizzes


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
        ).json()
        return self.questions_json

    def save_json_file(self):
        with open("quizzes/"+self.name+".json", "w") as f:
            f.write(json.dumps(vars(self)))


if __name__ == "__main__":
    main()
