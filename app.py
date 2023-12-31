import streamlit as st
import whisper
import os
import uuid
import shutil
import subprocess  # FFmpegを実行するために必要

os.environ["PATH"] += os.pathsep + "/usr/local/bin/ffmpeg"

# 一時ディレクトリを作成
temp_dir = "tempDir"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


# 音声を文字に起こす関数
def transcribe_audio(file_path, model_type="base"):
    model = whisper.load_model(model_type)
    result = model.transcribe(file_path)
    return result["text"]


# アップロードされたファイルを保存し、必要に応じて変換する関数
def save_and_convert_file(uploaded_file):
    try:
        # 一意のファイル名を生成
        unique_filename = str(uuid.uuid4()) + "_" + uploaded_file.name
        file_path = os.path.join(temp_dir, unique_filename)
        file_path_flac = os.path.splitext(file_path)[0] + ".flac"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # アップロードされたファイルがFLAC形式でない場合は変換
        if not uploaded_file.type == "audio/flac":
            subprocess.run(["ffmpeg", "-i", file_path, file_path_flac])
            os.remove(file_path)
            return file_path_flac
        else:
            return file_path
    except Exception as e:
        return None


# Streamlit UI設定
st.title("Whisperを使った音声文字起こしアプリ")

# Whisperモデル選択
model_choice = st.selectbox("モデルを選択してください", ["tiny", "base", "small", "medium"])

# 対応するファイル形式をリストに追加
uploaded_file = st.file_uploader(
    "音声ファイルをアップロードしてください", type=["flac", "mp3", "wav", "wma", "m4a"]
)

# 「文字起こし」ボタンを追加
if st.button("文字起こし"):
    if uploaded_file is not None:
        file_path = save_and_convert_file(uploaded_file)
        if file_path:
            with st.spinner("音声を文字起こししています..."):
                text = transcribe_audio(file_path, model_choice)

            # 文字起こし結果を表示
            st.text_area("文字起こし結果", text, height=250)

            # 一時ファイルの削除
            os.remove(file_path)
    else:
        st.warning("ファイルをアップロードしてください。")
