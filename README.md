# Cliptogen

Cliptogenは[プロジェクトの説明]です。

# 環境構築

新品のPCでも以下の手順で環境構築ができます。
前提条件

以下のソフトウェアがインストールされていることを確認してください。

Git https://git-scm.com/downloads

Python https://www.python.org/downloads

CUDA Toolkit 11.3 https://developer.nvidia.com/cuda-11.3.0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local

cuDNN https://developer.nvidia.com/rdp/cudnn-download

zlib https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#install-zlib-windows

# インストール手順

エクスプローラーを開き保存したい場所で上にあるファイルパスでcmdと入力してEnterキーを押すとコマンドプロンプトが起動します。

そして以下のコマンドを実行して、環境構築を行います。
    
```
git clone https://github.com/keimaruO/Cliptogen.git && cd Cliptogen && python -m pip install --upgrade pip && pip install -r requirements.txt && curl -L https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip -o ffmpeg.zip && curl -L https://github.com/yt-dlp
```
