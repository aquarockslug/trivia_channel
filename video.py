import subprocess

FONTS = {
    "coolvetica": "fonts/coolvetica.ttf",
    "opensans": "fonts/OpenSans-BoldItalic.ttf",
    "iosevka_curly": "fonts/iosevka-curly-semibold.ttc",
    "iosevka_semi": "iosevka-semiboldoblique.ttf",
}


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

        self.title_size = 212
        self.question_size = 72
        self.guess_size = 48
        self.answer_size = 128

        self.guesses_font = "iosevka_curly"

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
            ["fontcolor", "black"],
            # ["box", "1"],
            # ["boxcolor", "black@0.7"],
            # ["boxborderw", "15"],
        ]

    def add_linebreak(self, text):
        linebreak = int((len(text) / 2))
        while linebreak < len(text):
            if text[linebreak] == " ":
                break
            linebreak += 1
        return text[:linebreak] + "\n" + text[linebreak:]

    def add_title(self, title: str):
        self.center_text(title, "coolvetica", self.title_size)

    def add_answer(self, answer):
        self.center_text(answer, "coolvetica", self.answer_size)

    def center_text(self, text: str, font_name: str, size: int):
        self.ffmpeg(
            (
                "-i",
                self.background,
                "-vf",
                self.create_text_arg(text, font_name, size, *self.pos["center"]),
                "slides/" + self.name + ".png",
            )
        )

    def add_guesses(self, prompt, guesses):
        if len(prompt) >= 40:
            prompt = self.add_linebreak(prompt)
        slide_args = [
            (prompt, str("coolvetica"), self.question_size, *self.pos["top"]),
        ]
        for guess_index in range(0, 3):
            slide_args.append(
                (
                    guesses[guess_index],
                    str(self.guesses_font),
                    self.question_size,
                    *self.pos["a" + str(guess_index + 1)],
                )
            )
        ffmpeg_text_args = []
        for args in slide_args:
            ffmpeg_text_args.append(self.create_text_arg(*args))
        self.apply_ffmpeg_args(ffmpeg_text_args)

    def create_text_arg(self, text, font_name, font_size, x, y):
        """returns ffmpeg args which add the given text at the coordinates"""
        filter_args = [
            ["fontfile", FONTS[font_name]],
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
        print(filter_args_str)
        return filter_args_str

    def apply_ffmpeg_args(self, ffmpeg_args):
        for slide_index, arg in enumerate(ffmpeg_args):
            if slide_index == 0:
                self.ffmpeg(
                    ("-i", self.background, "-vf", arg, "img/" + self.name + ".png")
                )
            else:
                self.ffmpeg(
                    (
                        "-i",
                        "temp/" + self.name + ".png",
                        "-vf",
                        arg,
                        "img/" + self.name + ".png",
                    )
                )

            subprocess.run(
                ["mv", "img/" + self.name + ".png", "temp/" + self.name + ".png"]
            )

        subprocess.run(
            ["mv", "temp/" + self.name + ".png", "slides/" + self.name + ".png"]
        )

    def delete(self):
        subprocess.run(["rm", "slides/" + self.name + ".png"])

    def ffmpeg(self, args):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args])
