import datetime
from moviepy import editor
from moviepy.video.io.VideoFileClip import VideoFileClip
import textwrap
import budoux


def wrap_text(text, max_length=16, max_lines=4):
    wrapped_lines = textwrap.wrap(text, width=max_length)

    if len(wrapped_lines) > max_lines:
        wrapped_lines = wrapped_lines[:max_lines - 1] + [''.join(wrapped_lines[max_lines - 1:])]

    return wrapped_lines

def sentence_parse_and_line_parse(text, max_line_length=15, max_lines=4):
    space_parsed_text_list = text.split(' ')
    parsed_text_list = []

    current_line = ""
    for space_parsed_text in space_parsed_text_list:
        wrapped_text_list = wrap_text(space_parsed_text, max_line_length)
        for wrapped_text in wrapped_text_list:
            if len(current_line) + len(wrapped_text) + 1 <= max_line_length:
                current_line += " " + wrapped_text
            else:
                parsed_text_list.append(current_line.strip())
                current_line = wrapped_text
                if len(parsed_text_list) == max_lines - 1:
                    break

    if current_line:
        parsed_text_list.append(current_line.strip())

    return parsed_text_list[:max_lines]



def budoux_parse_text(text, max_length=16):
    budoux_parser = budoux.load_default_japanese_parser()
    parsed_text_list = []

    while len(text) > 0:
        parsed_text = ""
        overflow_text = ""

        for budoux_parsed_text in budoux_parser.parse(text):
            if max_length > len(parsed_text + budoux_parsed_text):
                parsed_text += budoux_parsed_text
            elif len(parsed_text) == 0 and len(budoux_parsed_text) > max_length:
                parsed_text = budoux_parsed_text[0:max_length]
                overflow_text += budoux_parsed_text[max_length:]
            else:
                overflow_text += budoux_parsed_text

        parsed_text_list.append(parsed_text)
        text = overflow_text

    return parsed_text_list

def annotate(clip, txt, max_line_length=15, max_lines=4):
    parsed_txt_list = sentence_parse_and_line_parse(txt, max_line_length, max_lines)
    parsed_txt = "\n".join(parsed_txt_list)
    txtclip_white = editor.TextClip(parsed_txt,
        fontsize=75,
        font='C:/USERS/KEI11/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NOTOSANSJP-BLACK.TTF',
        color='white'
    )
    txtclip_black = editor.TextClip(parsed_txt,
        fontsize=75,
        font='C:/USERS/KEI11/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NOTOSANSJP-BLACK.TTF',
        color='black',
        stroke_color="#000000",
        stroke_width=7
    )
    txtclip_ffa3aa = editor.TextClip(parsed_txt,
        fontsize=75,
        font='C:/USERS/KEI11/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NOTOSANSJP-BLACK.TTF',
        color='#FFA3AA',
        stroke_color="#FFA3AA",
        stroke_width=12
    )
    cvc = editor.CompositeVideoClip([
        clip, 
        txtclip_ffa3aa.set_position(('center', 'bottom')).set_layer(1),
        txtclip_black.set_position(('center', 'bottom')).set_layer(2),
        txtclip_white.set_position(('center', 'bottom')).set_layer(3)
    ])
    return cvc.set_duration(clip.duration)



def add_subtitles_to_video(input_video_path, subtitles, output_video_path):
    video = VideoFileClip(input_video_path)
    clips = []

    for subtitle in subtitles:
        start_time = datetime.timedelta(hours=subtitle['start'].hour, minutes=subtitle['start'].minute, seconds=subtitle['start'].second, microseconds=subtitle['start'].microsecond).total_seconds()
        end_time = datetime.timedelta(hours=subtitle['end'].hour, minutes=subtitle['end'].minute, seconds=subtitle['end'].second, microseconds=subtitle['end'].microsecond).total_seconds()
        clip = video.subclip(start_time, end_time)
        annotated_clip = annotate(clip, subtitle['text'])
        clips.append(annotated_clip)

    final_clip = editor.concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_path)