import subprocess

DEBUG = True


class Slide:
    """segment of video"""

    def __init__(
        self,
        name="cube",
        background="img/cube.png",
    ):
        self.name = name
        self.path = "slides/" + name + ".png"
        self.background = background

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
        return self.name + " - " + self.background

    def text_box_args(self):
        return [
            ["fontcolor", "white"],
            ["box", "1"],
            ["boxcolor", "black@0.7"],
            ["boxborderw", "15"],
        ]

    def add_linebreak(self, text):
        linebreak = int((len(text) / 2))
        while linebreak < len(text):
            if text[linebreak] == " ":
                break
            linebreak += 1
        return text[:linebreak] + "\n" + text[linebreak:]

    def add_title(self, title: str):
        self.ffmpeg(
            (
                "-i",
                self.background,
                "-vf",
                self.create_text_arg(title, 196, *self.pos["center"]),
                "slides/" + self.name + ".png",
            )
        )

    def add_answer(self, answer):
        self.ffmpeg(
            (
                "-i",
                self.background,
                "-vf",
                self.create_text_arg(answer, 144, *self.pos["center"]),
                "slides/" + self.name + ".png",
            )
        )

    def add_guesses(self, prompt, guesses):
        if len(prompt) >= 40:
            prompt = self.add_linebreak(prompt)

        slide_args = [(prompt, self.question_size, *self.pos["top"])]
        for i in range(0, 3): slide_args.append(
            (
                guesses[i], 
                self.answer_size, 
                *self.pos["a" + str(i + 1)])
            )

        ffmpeg_text_args = []
        for args in slide_args:
            ffmpeg_text_args.append(self.create_text_arg(*args))
        self.apply_ffmpeg_args(ffmpeg_text_args)

    def create_text_arg(self, text, font_size, x, y):
        """returns ffmpeg args which add the given text at the coordinates"""
        filter_args = [
            ["fontfile", "OpenSans-BoldItalic.ttf"],
            ["text", text],
            ["fontsize", str(font_size)],
            ["x", x],
            ["y", y],
        ] + self.text_box_args()
        return self.drawtext_filter_maker(filter_args)

    def drawtext_filter_maker(self, args: list):
        filter_args_str = "drawtext="
        for arg in args:
            filter_args_str += arg[0] + "=" + arg[1] + ":"
        if DEBUG: print(filter_args_str)
        return filter_args_str

    def apply_ffmpeg_args(self, ffmpeg_args):
        temp_name = "temp/" + self.name +".png"
        img_name = "img/" + self.name +".png"
        for slide_index, arg in enumerate(ffmpeg_args):
            if slide_index == 0:
                self.ffmpeg(
                    ("-i", self.background, "-vf", arg, img_name)
                )
            else:
                self.ffmpeg((
                        "-i", temp_name,
                        "-vf", arg,
                        img_name,
                ))

            subprocess.run(["mv", img_name, temp_name])

        subprocess.run(["mv", temp_name, "slides/" + self.name + ".png"])

    def delete(self):
        subprocess.run(["rm", "slides/" + self.name + ".png"])

    def ffmpeg(self, args):
        if not DEBUG:
            subprocess.run(
                "ffmpeg -y -loglevel quiet -stats".split(" ")
                + [*args]
            )
        else:
            subprocess.run(["ffmpeg", "-y", *args])
