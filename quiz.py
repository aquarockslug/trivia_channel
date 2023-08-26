import requests
import json


class Quiz_Creator:
    def prompt_create_quiz():
        Quiz_Creator.list_categories()
        print("---------------------------")
        return Quiz_Creator.create_quiz(
            input("Enter quiz name: "),
            input("Enter quiz length: "),
            input("Enter category number: ")
        )

    def list_categories():
        with open("categories.json", "r") as f:
            for c in json.loads(f.read())[0]["trivia_categories"]:
                print(c["id"], "-", c["name"])

    def create_quizzes(name: str = "quiz", amount: int = 1, length: int = 1, category: int = 9):
        quizzes = []
        for i in range(0, amount):
            quizzes.append(Quiz_Creator.create_quiz(
                name+"_"+str(i+1), length, category))
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
