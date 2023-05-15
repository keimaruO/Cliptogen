import os
import datetime
import json
from moviepy.editor import concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def add_subtitles_to_video(input_video_path, subtitles, output_video_path, settings):
    video = VideoFileClip(input_video_path)
    fps = video.fps
    clips = []

    video_duration = video.duration

    for index, subtitle in enumerate(subtitles):
        start_time = datetime.timedelta(hours=subtitle['start'].hour, minutes=subtitle['start'].minute, seconds=subtitle['start'].second, microseconds=subtitle['start'].microsecond).total_seconds()
        end_time = datetime.timedelta(hours=subtitle['end'].hour, minutes=subtitle['end'].minute, seconds=subtitle['end'].second, microseconds=subtitle['end'].microsecond).total_seconds()

        if index == len(subtitles) - 1 and end_time > video_duration:
            end_time = video_duration

        clip = video.subclip(start_time, end_time)
        annotated_clip = annotate(clip, subtitle['text'], settings)
        clips.append(annotated_clip.set_audio(clip.audio))

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_path, fps=fps, codec='libx264', audio_codec='aac')

    video.close()
    for clip in clips:
        clip.close()
    final_clip.close()

def calculate_max_chars(video_width, fontsize):
    # This is an estimation, you may need to adjust this value
    chars_per_fontsize_unit = 1.5
    return int(video_width // (fontsize / chars_per_fontsize_unit))

def sentence_parse_and_line_parse(text, video_width, fontsize, max_lines=4, max_chars=21):
    words = text.split(' ')
    lines = []
    line = ""

    for word in words:
        # Check if adding the current word to the current line will exceed the maximum characters.
        if len(line) + len(word) + 1 <= max_chars:
            line += " " + word
        else:
            # If it exceeds the maximum characters, start a new line with the current word.
            lines.append(line.strip())
            line = word

        # Break the loop when the maximum lines is reached.
        if len(lines) == max_lines:
            break

    # Add any remaining words to the last line.
    if line and len(lines) < max_lines:
        lines.append(line.strip())

    # Adjust font size if any line exceeds the maximum characters
    if any(len(line) > max_chars for line in lines):
        fontsize = int(fontsize * (max_chars / max(len(line) for line in lines)))

    return lines[:max_lines], fontsize



def annotate(clip, txt, settings, max_lines=4):
    video_width, video_height = clip.size
    fontsize = int(video_height * 0.088)
    parsed_txt_list, fontsize = sentence_parse_and_line_parse(txt, video_width, fontsize, max_lines=max_lines, max_chars=21)
    parsed_txt = "\n".join(parsed_txt_list)

    txtclip_white = TextClip(parsed_txt,
        fontsize=fontsize,
        font=settings['txtclip_white']['font'],
        color=settings['txtclip_white']['color'],
    )
    txtclip_black = TextClip(parsed_txt,
        fontsize=fontsize,
        font=settings['txtclip_black']['font'],
        color=settings['txtclip_black']['color'],
        stroke_color=settings['txtclip_black']['stroke_color'],
        stroke_width=settings['txtclip_black']['stroke_width']
    )
    txtclip_ffa3aa = TextClip(parsed_txt,
        fontsize=fontsize,
        font=settings['txtclip_ffa3aa']['font'],
        color=settings['txtclip_ffa3aa']['color'],
        stroke_color=settings['txtclip_ffa3aa']['stroke_color'],
        stroke_width=settings['txtclip_ffa3aa']['stroke_width']
    )
    cvc = CompositeVideoClip([
        clip,
        txtclip_ffa3aa.set_position(('center', 'bottom')).set_layer(1),
        txtclip_black.set_position(('center', 'bottom')).set_layer(2),
        txtclip_white.set_position(('center', 'bottom')).set_layer(3)
    ], size=clip.size).set_duration(clip.duration)

    return cvc.set_duration(clip.duration)
