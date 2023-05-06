from subtitle_parser import parse_srt_file
from video_annotator import add_subtitles_to_video

input_video_path = "E:\\Cliptogen\\output\\concatenated_video.mp4"
srt_file_path = "E:\\Cliptogen\\output\\temp_1.srt"
output_video_path = "E:\\Cliptogen\\done\\done.mp4"

subtitles = parse_srt_file(srt_file_path)
add_subtitles_to_video(input_video_path, subtitles, output_video_path)