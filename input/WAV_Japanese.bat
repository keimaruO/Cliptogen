@echo off
chcp 65001
setlocal enabledelayedexpansion
set input_dir=E:\Cliptogen\output
set output_dir=E:\Cliptogen\output
set counter=1

for /f "delims=" %%i in ('dir /b /a-d /o:d "%input_dir%\*.wav"') do (
    set "temp_file=temp_!counter!.wav"
    move /y "%input_dir%\%%i" "%input_dir%\!temp_file!" >nul
    set /a counter+=1
)


whisper-ctranslate2 "E:\Cliptogen\output\temp_1.wav" --model large-v2 --output_dir "E:\Cliptogen\output" --compute_type auto --language Japanese --initial_prompt="金の玉 ホロ鯖 ほろさば 平和の像 キッスマシーン ホロライブ 5期生 ねぽらぼ あずきち そらちゃん ときのそら そら先輩 まつり先輩 シオン シオン先輩 しおんたん スバル先輩 大空スバル スバル 兎田ぺこら ぺこ ぺこーら ぺこちゃん ぺこら先輩 るしあ るーちゃん先輩 かなた先輩 天音かなた かなたん へい民 わため先輩 トワワ トワワ先輩 常闇トワ トワ様 ルーナ ルーナ先輩 雪花ラミィ 雪花さん ラミィ ワミィ 雪民 桃鈴ねね ねね ねねち ねっ子  ねっ子 獅白ぼたん ししろん こより こよちゃん クロエ いろは またねね こんねね カブトムシ"