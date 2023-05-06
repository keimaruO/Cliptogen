import os

#options = '-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -N 1 -S vcodec:h264'
options = '-f "bestvideo[height<=720][fps<=12][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][fps<=30][ext=mp4]" -N 1 -S vcodec:h264'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.join(BASE_DIR, 'output', 'yt-dlp')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
counter = 1

with open(os.path.join(BASE_DIR, 'dlurl.txt'), 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('https://youtu.be/'):
            video_id = line.split('/')[-1].split('?')[0]
            url = f'https://www.youtube.com/watch?v={video_id}'
        else:
            start_time, end_time = line.split('-')
            output_path = os.path.join(output_dir, f'{counter}%(title)s.%(ext)s')
            command = f'yt-dlp {options} -o "{output_path}" --download-sections *{start_time}-{end_time} {url}'
            os.system(command)
            counter += 1