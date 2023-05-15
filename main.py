import os
import datetime
import json
from subtitle_parser import parse_srt_file
from video_annotator import add_subtitles_to_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(BASE_DIR, "settings.json")

with open(settings_path, 'r') as f:
    settings = json.load(f)

input_video_path = os.path.join(BASE_DIR, "output", "concatenated_video.mp4")
srt_file_path = os.path.join(BASE_DIR, "output", "temp_1.srt")
current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_video_filename = f"done_{current_datetime}.mp4"
output_video_path = os.path.join("G:/GoogleDrive/_Share/Share", output_video_filename)
subtitles = parse_srt_file(srt_file_path)
font_path = "Cliptogen/fonts/NOTOSANSJP-EXTRABOLD.TTF"
add_subtitles_to_video(input_video_path, subtitles, output_video_path, settings)
