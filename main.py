import os
from subtitle_parser import parse_srt_file
from video_annotator import add_subtitles_to_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_video_path = os.path.join(BASE_DIR, "output", "concatenated_video.mp4")
srt_file_path = os.path.join(BASE_DIR, "output", "temp_1.srt")
output_video_path = os.path.join(BASE_DIR, "done", "done.mp4")

subtitles = parse_srt_file(srt_file_path)
add_subtitles_to_video(input_video_path, subtitles, output_video_path)