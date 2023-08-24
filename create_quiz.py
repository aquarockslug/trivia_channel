import requests
import json


class Quiz:
    def __init__(self):
        self.name: int = "sample_quiz"
        self.length: int = 2
        self.category: int = 0
        self.questions_json: str = None

    def get_questions(self):
        self.questions_json = requests.get(
            "https://opentdb.com/api.php?amount="+str(self.length)+"&category="+str(self.category)).json()

    def save(self):
        with open("quizzes/"+self.name+".json", "w") as f:
            f.write(json.dumps(vars(self)))


def list_categories():
    with open("categories.json", "r") as f:
        j = json.loads(f.read())[0]
        print(j["trivia_categories"])
        for c in j:
            print(c.id, c.name)


def create_quiz():
    q = Quiz()
    q.get_questions()
    q.save()


def main():
    # list_categories()
    create_quiz()


if __name__ == "__main__":
    main()
