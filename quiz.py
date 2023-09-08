import json
import re
import requests


class Quiz_Creator:
    """quiz factory"""

    @staticmethod
    def prompt_create_quiz():
        Quiz_Creator.list_categories()
        print("---------------------------")
        return Quiz_Creator.create_quiz(
            input("Enter quiz name: "),
            int(input("Enter quiz length: ")),
            int(input("Enter category number: ")),
        )

    @staticmethod
    def list_categories():
        with open("categories.json", "r") as f:
            for c in json.loads(f.read())[0]["trivia_categories"]:
                print(c["id"], "-", c["name"])

    @staticmethod
    def create_quizzes(
        name: str = "quiz", amount: int = 1, length: int = 1, category: int = 9
    ):
        quizzes = []
        for i in range(0, amount):
            quizzes.append(
                Quiz_Creator.create_quiz(name + "_" + str(i + 1), length, category)
            )
        return quizzes

    @staticmethod
    def create_quiz(name: str, length: int, category: int):
        new_quiz = Quiz(name, length, category)
        new_quiz.request_questions()
        new_quiz.clean_text()
        new_quiz.save_json_file()
        return new_quiz


class Quiz:
    def __init__(self, name: str = "quiz", length: int = 1, category: int = 9):
        self.name: str = name
        self.length: int = length
        self.category: int = category
        self.questions: dict = {}

    def request_questions(self):
        """makes a request, then returns and saves the json response"""
        self.questions = requests.get(
            "https://opentdb.com/api.php?amount="
            + str(self.length)
            + "&category="
            + str(self.category)
        ).json()["results"]
        return self.questions

    def clean_text(self):
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        for text in self.questions:
            print(text)
            text = re.sub(CLEANR, '', text["question"])

    def get_questions(self) -> dict:
        return self.questions

    def get_name(self) -> str:
        return self.name

    def save_json_file(self):
        with open("quizzes/" + self.name + ".json", "w") as f:
            f.write(json.dumps(vars(self)))

if __name__ == '__main__':
    Quiz_Creator.prompt_create_quiz()
