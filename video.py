import subprocess
# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4

class Slide:
    """ segment of video """
    def __init__(self, background):
        self.background = background
        self.pos = {
            "center": ("(w-text_w)/2", "(h-text_h)/2"),
            "top": ("(w-text_w)/2", "(h-text_h)/4"),
            "a1": ("(w-text_w)/2", "(h-text_h)/2"),
            "a2": ("(w-text_w)/2", "(h-text_h)/2"),
            "a3": ("(w-text_w)/2", "(h-text_h)/2"),
            "a4": ("(w-text_w)/2", "(h-text_h)/2"),
        }

    def text_box_args(self): 
        return [
            ["fontcolor", "white"],
            ["box", "1"],
            ["boxcolor", "black@0.8"],
            ["boxborderw", "5"],
        ]

    def add_question(self):
        self.add_text("Question", 48, *self.pos["top"])
        self.add_text("A1", 24, *self.pos["a1"])
        self.add_text("A2", 24, *self.pos["a2"])
        self.add_text("A3", 24, *self.pos["a3"])
        self.add_text("A4", 24, *self.pos["a4"])

    def add_title(self, title: str):
        self.add_text(title, 196, *self.pos["center"])

    def add_text(self, text, font_size, x, y):
        filter_args = [
            ["fontfile", "OpenSans-BoldItalic.ttf"],
            ["text", text],
            ["fontsize", str(font_size)],
            ["x", x], ["y", y]
        ] + self.text_box_args()

        ffmpeg_args = ("-i", self.background, "-vf", self.drawtext_filter_maker(filter_args),
                       "-codec:a", "copy", "slides/output.mp4")

        ffmpeg(ffmpeg_args)

    def drawtext_filter_maker(self, args: list):
        filter_args_str = "drawtext="
        for arg in args:
            filter_args_str += arg[0] + "=" + arg[1] + ":"
        print(filter_args_str)
        return filter_args_str


def ffmpeg(args): subprocess.run(["ffmpeg", *args])
