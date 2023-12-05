import streamlit as st
import whisper
import os

os.environ["PATH"] += os.pathsep + "/usr/local/bin/ffmpeg"


# 音声を文字に起こす関数
def transcribe_audio(file_path, model_type="base"):
    model = whisper.load_model(model_type)
    result = model.transcribe(file_path)
    return result["text"]


# アップロードされたファイルを保存する関数
def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join("tempDir", uploaded_file.name)
    except Exception as e:
        return None


# Streamlit UI設定
st.title("Whisperを使った音声文字起こしアプリ")

# Whisperモデル選択
model_choice = st.selectbox(
    "モデルを選択してください", ["tiny", "base", "small", "medium", "large"]
)

uploaded_file = st.file_uploader("FLACファイルをアップロードしてください", type=["flac"])

if uploaded_file is not None:
    file_path = save_uploaded_file(uploaded_file)
    if file_path:
        with st.spinner("音声を文字起こししています..."):
            text = transcribe_audio(file_path, model_choice)
        st.text_area("文字起こし結果", text, height=250)
