import os
import datetime
import subprocess
import re
import shutil

def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "ffmpeg.exe")

def fix_special_characters(name):
    return re.sub(r'[^\x00-\x7F]+', '', name)

def concatenate_videos(input_dir, output_dir, output_name):
    file_list = [file for file in os.listdir(input_dir) if file.endswith('.mp4')]
    file_list = sorted(file_list, key=lambda x: int(re.search(r'\d+', x).group()))
    
    # Encode each video before concatenating
    encoded_file_list = []
    for index, file in enumerate(file_list):
        input_file = os.path.join(input_dir, file)
        encoded_file = os.path.join(input_dir, f'encoded_{index}.mp4')
        encoded_file_list.append(encoded_file)
        
        ffmpeg_path = get_ffmpeg_path()
        encode_command = f'{ffmpeg_path} -y -i "{input_file}" -c:v libx264 -crf 23 -c:a aac -b:a 192k "{encoded_file}"'
        os.system(encode_command)

    with open("concat.txt", "w", encoding="utf-8") as f:
        for encoded_file in encoded_file_list:
            f.write(f"file '{encoded_file}'\n")

    ffmpeg_path = get_ffmpeg_path()
    concat_command = f'{ffmpeg_path} -y -f concat -safe 0 -i concat.txt -c copy "{os.path.join(output_dir, output_name)}"'
    os.system(concat_command)
    os.remove("concat.txt")

    # Remove encoded files
    for encoded_file in encoded_file_list:
        os.remove(encoded_file)

def extract_and_concatenate_audio(input_dir, output_dir, output_name):
    file_list = [file for file in os.listdir(input_dir) if file.endswith('.mp4')]
    file_list = sorted(file_list, key=lambda x: int(re.search(r'\d+', x).group()))
    audio_files = []
    ffmpeg_path = get_ffmpeg_path()
    for file in file_list:
        audio_output = os.path.join(output_dir, "{}.wav".format(re.search(r'\d+', file).group()))
        audio_files.append(audio_output)
        extract_command = f'ffmpeg -y -i "{os.path.join(input_dir, file)}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_output}"'
        subprocess.run(extract_command, shell=True, env=os.environ)
        extract_command = f'{ffmpeg_path} -y -i "{os.path.join(input_dir, file)}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_output}"'
        os.system(extract_command)

    with open("concat_audio.txt", "w", encoding="utf-8") as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")

    concat_audio_command = f'ffmpeg -y -f concat -safe 0 -i concat_audio.txt -c copy "{os.path.join(output_dir, output_name)}"'
    subprocess.run(concat_audio_command, shell=True, env=os.environ)
    concat_audio_command = f'{ffmpeg_path} -y -f concat -safe 0 -i concat_audio.txt -c copy "{os.path.join(output_dir, output_name)}"'
    os.system(concat_audio_command)
    os.remove("concat_audio.txt")
    for audio_file in audio_files:
        os.remove(audio_file)

def move_files_to_archive(archive_base_dir, srt_destination):
    output_yt_dlp_dir = os.path.join(BASE_DIR, "output", "yt-dlp")
    archive_dir = os.path.join(archive_base_dir, "Kanata", "アーカイブ")
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    srt_file_path = os.path.join(BASE_DIR, "output", "temp_1.srt")
    if os.path.exists(srt_file_path):
        # ファイル名に日付と時刻を追加
        srt_destination_with_timestamp = os.path.join(srt_destination, f'temp_1_{timestamp}.srt')
        shutil.move(srt_file_path, srt_destination_with_timestamp)

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    existing_folders = [int(folder) for folder in os.listdir(archive_dir) if folder.isdigit()]
    next_folder_number = max(existing_folders) + 1 if existing_folders else 1
    new_archive_folder = os.path.join(archive_dir, str(next_folder_number))
    os.makedirs(new_archive_folder)

    files_to_move = [
        os.path.join(BASE_DIR, "output", "concatenated_video.mp4"),
        os.path.join(BASE_DIR, "output", "temp_1.tsv"),
        os.path.join(BASE_DIR, "output", "temp_1.txt"),
        os.path.join(BASE_DIR, "output", "temp_1.vtt"),
    ]

    for file_path in files_to_move:
        if os.path.exists(file_path):
            shutil.move(file_path, new_archive_folder)

    for file in os.listdir(output_yt_dlp_dir):
        if file != ".gitignore":
            file_path = os.path.join(output_yt_dlp_dir, file)
            shutil.move(file_path, new_archive_folder)

    srt_file_path = os.path.join(BASE_DIR, "output", "temp_1.srt")
    if os.path.exists(srt_file_path):
        shutil.move(srt_file_path, srt_destination)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
subprocess.run(["python", os.path.join(BASE_DIR, "Auto_yt-dlp_DL.py")])


input_dir = os.path.join(BASE_DIR, "output", "yt-dlp")
output_dir = os.path.join(BASE_DIR, "output")
output_name = "concatenated_video.mp4"
concatenate_videos(input_dir, output_dir, output_name)

audio_output_dir = os.path.join(BASE_DIR, "output")
audio_output_name = "temp_1.wav"
extract_and_concatenate_audio(input_dir, audio_output_dir, audio_output_name)

input_wav = os.path.join(BASE_DIR, "output", "temp_1.wav")
whisper_command = f'whisper-ctranslate2 "{input_wav}" --model large-v2 --compute_type auto --language Japanese --initial_prompt="ホロ鯖 ほろさば ホロライブ 5期生 ねぽらぼ あずきち そらちゃん ときのそら そら先輩 まつり先輩 シオン シオン先輩 しおんたん スバル先輩 大空スバル スバル 兎田ぺこら ぺこ ぺこーら ぺこちゃん ぺこら先輩 るしあ るーちゃん先輩 かなた先輩 天音かなた かなたん へい民 わため先輩 トワワ トワワ先輩 常闇トワ トワ様 ルーナ ルーナ先輩 雪花ラミィ 雪花さん ラミィ ワミィ 雪民 桃鈴ねね ねね ねねち ねっ子  ねっ子 獅白ぼたん ししろん こより こよちゃん クロエ いろは またねね こんねね カブトムシ"'
print(whisper_command)
subprocess.run(whisper_command, shell=True, cwd=output_dir)

output_srt_path = os.path.join(BASE_DIR, "output", "temp_1.srt")


subprocess.run(["python", os.path.join(BASE_DIR, "main.py")])

if os.path.exists(input_wav):
    os.remove(input_wav)
    
archive_base_dir = "F:\\TEEEEEEEEESSSSSSSSTTTTTTT"
srt_destination = "G:\\GoogleDrive\\_Share\\Share"
move_files_to_archive(archive_base_dir, srt_destination)
