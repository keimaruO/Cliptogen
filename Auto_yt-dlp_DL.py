import os
import re

options = '-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -N 1 -S vcodec:h264'　#最高画質,最高音質
#options = '-f "bestvideo[height<=144][fps<=8][ext=mp4]+bestaudio[ext=m4a]/best[height<=144][fps<=8][ext=mp4]" -N 1 -S vcodec:h264'
#options = '-f "bestvideo[height<=720][fps<=12][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][fps<=12][ext=mp4]" -N 1 -S vcodec:h264'
#options = '-f "bestvideo[height<=720][fps<=12][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][fps<=30][ext=mp4]" -N 1 -S vcodec:h264' #720p,最高音質

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(BASE_DIR, 'output', 'yt-dlp')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
counter = 1

with open(os.path.join(BASE_DIR, 'dlurl.txt'), 'r') as f:
    url = ''
    for line in f:
        line = line.strip()
        if line.startswith('https://youtu.be/') or line.startswith('https://www.youtube.com/'):
            video_id = re.search(r'(?<=\bv=)[^&]*|(?<=\b/)[^&/?]*', line).group(0)
            if video_id != 'watch':
                url = f'https://www.youtube.com/watch?v={video_id}'
                timecode = re.search(r'(?<=\bt=)[0-9]+', line)
                if timecode:
                    start_time = int(timecode.group(0))
                else:
                    start_time = 0
        elif re.match(r'\d+:\d+:\d+-\d+:\d+:\d+|\d+:\d+-\d+:\d+', line) and url != '':
            if start_time != 0:
                parts = line.split('-')
                start_time += int(parts[0].split(':')[0]) * 60 + int(parts[0].split(':')[1])
                end_time = start_time + int(parts[1].split(':')[0]) * 60 + int(parts[1].split(':')[1])
                line = f'{start_time}-{end_time}'
            output_path = os.path.join(output_dir, f'{counter}%(title)s.%(ext)s')
            command = f'yt-dlp {options} -o "{output_path}" --download-sections *{line} {url}'
            os.system(command)
            counter += 1
            start_time = 0
        else:
            continue
