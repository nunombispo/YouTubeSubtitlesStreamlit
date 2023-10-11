import streamlit as st
import assemblyai as aai
from yt_dlp import YoutubeDL


@st.cache_data
def download_video_from_url(url):
    videoinfo = YoutubeDL().extract_info(url=url, download=False)
    filename = f"./youtube/{videoinfo['id']}.mp4"
    options = {
        'format': 'bestvideo/best',
        'keepvideo': True,
        'outtmpl': filename,
    }
    with YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])
    return filename


@st.cache_data
def download_audio_from_url(url):
    videoinfo = YoutubeDL().extract_info(url=url, download=False)
    filename = f"./youtube/{videoinfo['id']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }
    with YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])
    return filename


@st.cache_data
def generate_subtitles(filename):
    aai.settings.api_key = "YOUR_API_KEY"
    transcript = aai.Transcriber().transcribe(filename)
    subtitles = transcript.export_subtitles_srt()
    return subtitles



def main():
    st.title("YouTube Video Downloader and Subtitle Generator")
    video_url = st.text_input("Enter the YouTube video URL:")

    if st.button("Generate Subtitles"):
        with st.status("Processing video file...", expanded=True):
            st.write("Downloading audio from YouTube video..")
            filename_audio = download_audio_from_url(video_url)
            st.write("Downloading video from YouTube video..")
            filename_video = download_video_from_url(video_url)
            st.write("Generating subtitles from audio file..")
            subtitles = generate_subtitles(filename_audio)
        col1, col2 = st.columns(2)
        with col1:
            st.video(filename_video)
            with open(filename_video, "rb") as f:
                st.download_button("Download Video", data=f, file_name="video.mp4")
        with col2:
            st.text_area("Subtitles", value=subtitles, height=200, label_visibility="collapsed")
            st.download_button("Download Subtitles", data=subtitles, file_name="video.srt")


if __name__ == "__main__":
    main()
