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

# Step 1: Auto_yt-dlp_DL.pyを実行して.mp4ファイルをダウンロードする
subprocess.run(["python", "E:\\Cliptogen\\Auto_yt-dlp_DL.py"])

# Step 2: E:\Cliptogen\inputのフォルダ内の.mp4ファイルを番号順に連結して、
# E:\Cliptogen\outputにWAVファイルとmp4ファイルを作成する。
input_dir = "E:\\Cliptogen\\output\\yt-dlp"
output_dir = "E:\\Cliptogen\\output"
output_name = "concatenated_video.mp4"
concatenate_videos(input_dir, output_dir, output_name)

# Step 2.1: Extract and concatenate audio from the mp4 files
audio_output_dir = "E:\\Cliptogen\\output"
audio_output_name = "concatenated_audio.wav"
extract_and_concatenate_audio(input_dir, audio_output_dir, audio_output_name)

# Step 3: E:\Cliptogen\input\WAV_Japanese.batを実行して、E:\Cliptogen\output\temp_1.srtを作成する
subprocess.run(["E:\\Cliptogen\\input\\WAV_Japanese.bat"])

# Step 4: Cliptogenフォルダ内のmain.pyを起動して終了。
subprocess.run(["python", "E:\\Cliptogen\\main.py"])

# Step 5: Remove E:\Cliptogen\output\temp_1.wav
temp_1_wav_path = "E:\\Cliptogen\\output\\temp_1.wav"
if os.path.exists(temp_1_wav_path):
    os.remove(temp_1_wav_path)

# Step 6: Remove E:\Cliptogen\input\concat.txt and E:\Cliptogen\input\concat_audio.txt if they exist
concat_txt_path = "E:\\Cliptogen\\input\\concat.txt"
if os.path.exists(concat_txt_path):
    os.remove(concat_txt_path)

concat_audio_txt_path = "E:\\Cliptogen\\input\\concat_audio.txt"
if os.path.exists(concat_audio_txt_path):
    os.remove(concat_audio_txt_path)