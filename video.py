from main import ffmpeg

# convert to video:
# ffmpeg -framerate 1 -i happy%d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4


def add_text(text, font_size, x, y):
    filter_args = [
        ["fontfile", "OpenSans-BoldItalic.ttf"],
        ["text", text],
        ["fontsize", str(font_size)],
        ["x", x], ["y", y]
    ] + text_box_args()

    ffmpeg_args = ("-i", "cubes.mp4", "-vf", drawtext_filter_maker(filter_args),
                   "-codec:a", "copy", "slides/output.mp4")

    ffmpeg(ffmpeg_args)


def text_box_args(): return [
    ["fontcolor", "white"],
    ["box", "1"],
    ["boxcolor", "black@0.5"],
    ["boxborderw", "5"],
]


def drawtext_filter_maker(args: list):
    filter_args_str = "drawtext="
    for arg in args:
        filter_args_str += arg[0] + "=" + arg[1] + ":"
    print(filter_args_str)
    return filter_args_str
