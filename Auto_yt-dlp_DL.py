import os
import subprocess

# 現在のスクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# yt-dlpが存在するディレクトリのパスを設定
yt_dlp_dir = "yt-dlp"

# dlurl.txtファイルの絶対パスを指定
DLURL_FILE = "dlurl.txt"

def main():
    # dlurl.txtファイルを開く
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(DLURL_FILE, "r") as file:
        lines = file.readlines()

    current_url = ""
    output_counter = 1

    # 各行を処理する
    for line in lines:
        line = line.strip()

        # 空行をスキップ
        if not line:
            continue

        # URLの場合
        if "http" in line:
            current_url = line
        # 時間範囲の場合
        else:
            start_time, end_time = line.split("-")
            output_path = f'output/yt-dlp/{output_counter}%(title)s.%(ext)s'
            output_counter += 1

            # yt-dlpコマンドを実行
            cmd = " ".join([
                "yt-dlp",
                "-f", "\"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]\"",
                "-N", "1",
                "-S", "vcodec:h264",
                "-o", output_path,
                "--download-sections", f'*{start_time}-{end_time}',
                current_url
            ])

            print("Executing command:", cmd)
            subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    main()
