import os
import subprocess
import re

def fix_special_characters(name):
    return re.sub(r'[^\x00-\x7F]+', '', name)

def concatenate_videos(input_dir, output_dir, output_name):
    file_list = sorted(os.listdir(input_dir), key=lambda x: int(re.search(r'\d+', x).group()))
    with open("concat.txt", "w", encoding="utf-8") as f:
        for file in file_list:
            f.write(f"file '{os.path.join(input_dir, file)}'\n")

    concat_command = f'ffmpeg -y -f concat -safe 0 -i concat.txt -c copy "{os.path.join(output_dir, output_name)}"'
    os.system(concat_command)
    os.remove("concat.txt")

def extract_and_concatenate_audio(input_dir, output_dir, output_name):
    file_list = sorted(os.listdir(input_dir), key=lambda x: int(re.search(r'\d+', x).group()))
    audio_files = []

    for file in file_list:
        audio_output = os.path.join(output_dir, "{}.wav".format(re.search(r'\d+', file).group()))
        audio_files.append(audio_output)
        extract_command = f'ffmpeg -y -i "{os.path.join(input_dir, file)}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_output}"'
        os.system(extract_command)

    with open("concat_audio.txt", "w", encoding="utf-8") as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")

    concat_audio_command = f'ffmpeg -y -f concat -safe 0 -i concat_audio.txt -c copy "{os.path.join(output_dir, output_name)}"'
    os.system(concat_audio_command)

    os.remove("concat_audio.txt")
    for audio_file in audio_files:
        os.remove(audio_file)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

subprocess.run(["python", os.path.join(BASE_DIR, "Auto_yt-dlp_DL.py")])

input_dir = os.path.join(BASE_DIR, "output", "yt-dlp")
output_dir = os.path.join(BASE_DIR, "output")
output_name = "concatenated_video.mp4"
concatenate_videos(input_dir, output_dir, output_name)

audio_output_dir = os.path.join(BASE_DIR, "output")
audio_output_name = "concatenated_audio.wav"
extract_and_concatenate_audio(input_dir, audio_output_dir, audio_output_name)

subprocess.run([os.path.join(BASE_DIR, "input", "WAV_Japanese.bat")])
subprocess.run(["python", os.path.join(BASE_DIR, "main.py")])

temp_1_wav_path = os.path.join(BASE_DIR, "output", "temp_1.wav")
if os.path.exists(temp_1_wav_path):
    os.remove(temp_1_wav_path)

concat_txt_path = os.path.join(BASE_DIR, "input", "concat.txt")
if os.path.exists(concat_txt_path):
    os.remove(concat_txt_path)

concat_audio_txt_path = os.path.join(BASE_DIR, "input", "concat_audio.txt")
if os.path.exists(concat_audio_txt_path):
    os.remove(concat_audio_txt_path)
