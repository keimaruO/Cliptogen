import datetime
from moviepy.editor import concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import textwrap
from moviepy.editor import TextClip, CompositeVideoClip
def add_subtitles_to_video(input_video_path, subtitles, output_video_path, font_path):
    video = VideoFileClip(input_video_path)
    fps = video.fps
    clips = []

    for subtitle in subtitles:
        start_time = datetime.timedelta(hours=subtitle['start'].hour, minutes=subtitle['start'].minute, seconds=subtitle['start'].second, microseconds=subtitle['start'].microsecond).total_seconds()
        end_time = datetime.timedelta(hours=subtitle['end'].hour, minutes=subtitle['end'].minute, seconds=subtitle['end'].second, microseconds=subtitle['end'].microsecond).total_seconds()
        clip = video.subclip(start_time, end_time)
        annotated_clip = annotate(clip, subtitle['text'], font_path)
        clips.append(annotated_clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_path, fps=fps, codec='libx264', audio_codec='aac')

    video.close()
    for clip in clips:
        clip.close()
    final_clip.close()
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

font_path = 'C:/USERS/KEI11/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NOTOSANSJP-BLACK.TTF'

def annotate(clip, txt, font_path, max_line_length=15, max_lines=4):
    video_width, video_height = clip.size
    fontsize = int(video_height * 0.08)

    parsed_txt_list = sentence_parse_and_line_parse(txt, max_line_length, max_lines)
    parsed_txt = "\n".join(parsed_txt_list)

    txtclip_white = TextClip(parsed_txt,
        fontsize=fontsize,
        font=font_path,
        color='white'
    )
    txtclip_black = TextClip(parsed_txt,
        fontsize=fontsize,
        font=font_path,
        color='black',
        stroke_color="#000000",
        stroke_width=7
    )
    txtclip_ffa3aa = TextClip(parsed_txt,
        fontsize=fontsize,
        font=font_path,
        color='#FFA3AA',
        stroke_color="#FFA3AA",
        stroke_width=12
    )
    cvc = CompositeVideoClip([
        clip,
        txtclip_ffa3aa.set_position(('center', 'bottom')).set_layer(1),
        txtclip_black.set_position(('center', 'bottom')).set_layer(2),
        txtclip_white.set_position(('center', 'bottom')).set_layer(3)
    ])
    return cvc.set_duration(clip.duration)
