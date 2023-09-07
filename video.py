import subprocess

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


class Slide:
    """segment of video"""

    def __init__(self, name, background, duration):
        self.name = name
        self.background = background
        self.duration = duration
        self.question_size = 64
        self.answer_size = 48
        self.pos = {
            "center": ("(w-text_w)/2", "(h-text_h)/2"),
            "top": ("(w-text_w)/2", "(h-text_h)/4"),
            "a1": ("(w-text_w)/4", "((h-text_h) - (h-text_h)/4)"),
            "a2": ("((w-text_w) - (w-text_w)/4)", "((h-text_h) - (h-text_h)/4)"),
            "a3": ("(w-text_w)/4", "((h-text_h) - (h-text_h)/8)"),
            "a4": ("((w-text_w) - (w-text_w)/4)", "((h-text_h) - (h-text_h)/8)"),
        }

    def __str__(self):
        return self.name + " - " + self.background + " - " + str(self.duration) + "s \n"

    def text_box_args(self):
        return [
            ["fontcolor", "white"],
            ["box", "1"],
            ["boxcolor", "black@0.8"],
            ["boxborderw", "5"],
        ]

    def add_question(self, question_slide):
        question, incorrect, correct = (
            question_slide["question"],
            question_slide["incorrect_answers"],
            question_slide["correct_answer"],
        )
        if len(question) >= 40:
            question = self.add_linebreak(question)
        slide_args = [
            ( question, self.question_size, *self.pos["top"]),
            (incorrect[0], self.answer_size, *self.pos["a1"]),
            (incorrect[1], self.answer_size, *self.pos["a2"]),
            (incorrect[2], self.answer_size, *self.pos["a3"]),
            (correct, self.answer_size, *self.pos["a4"]),
        ]
        ffmpeg_text_args = []
        for args in slide_args:
            ffmpeg_text_args.append(self.create_text_arg(*args))
        self.apply_ffmpeg_args(ffmpeg_text_args)

    def add_linebreak(self, text):
        linebreak = int((len(text) / 2))
        while linebreak < len(text):
            if text[linebreak] == " ":
                break
            linebreak += 1
        return text[:linebreak] + "\n" + text[linebreak:]

    def apply_ffmpeg_args(self, ffmpeg_args):
        for slide_index, arg in enumerate(ffmpeg_args):
            if slide_index == 0:
                ffmpeg(("-i", self.background, "-vf") + arg)
            else:
                ffmpeg(("-i", "temp/" + self.name + ".mp4", "-vf") + arg)
            subprocess.run(
                ["mv", "slides/" + self.name + ".mp4", "temp/" + self.name + ".mp4"]
            )

        subprocess.run(
            ["mv", "temp/" + self.name + ".mp4", "slides/" + self.name + ".mp4"]
        )

    def add_title(self, title: str):
        ffmpeg(
            ("-i", self.background, "-vf")
            + self.create_text_arg(title, 196, *self.pos["center"])
        )

    def create_text_arg(self, text, font_size, x, y):
        """returns ffmpeg args which add the given text at the coordinates"""
        filter_args = [
            ["fontfile", "OpenSans-BoldItalic.ttf"],
            ["text", text],
            ["fontsize", str(font_size)],
            ["x", x],
            ["y", y],
        ] + self.text_box_args()

        ffmpeg_args = (
            self.drawtext_filter_maker(filter_args),
            "-codec:a",
            "copy",
            "slides/" + self.name + ".mp4",
        )

        return ffmpeg_args

    def drawtext_filter_maker(self, args: list):
        filter_args_str = "drawtext="
        for arg in args:
            filter_args_str += arg[0] + "=" + arg[1] + ":"
        print(filter_args_str)
        return filter_args_str

    def delete(self):
        subprocess.run(["rm", "slides/" + self.name + ".mp4"])


def ffmpeg(args):
    subprocess.run(["ffmpeg", *args])
