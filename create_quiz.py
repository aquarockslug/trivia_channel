import requests
import json


class Quiz:
    name: int = "sample_quiz"
    length: int = 2
    category: int = 0
    questions_json: str = None

    def get_questions(self):
        self.questions_json = requests.get(
            "https://opentdb.com/api.php?amount="+str(self.length)+"&category="+str(self.category)).json()

    def save(self):
        with open("quizzes/"+self.name+".json", "w") as f:
            f.write(json.dumps(vars(self)))


def main():
    q = Quiz()
    q.get_questions()
    q.save()


if __name__ == "__main__":
    main()
