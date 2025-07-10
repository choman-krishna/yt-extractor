import streamlit as st
import yt_dlp
import pandas as pd

st.title("🎥 YouTube Playlist Info Extractor")

playlist_url = st.text_input("Enter YouTube Playlist URL:")

if st.button("Fetch Playlist Info"):
    if playlist_url:
        ydl_opts = {
            'extract_flat': False,
            'quiet': True,
            'ignoreerrors': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            videos = result['entries']

            data = []

            for video in videos:
                if video is None:
                    continue

                title = video.get('title', 'N/A')
                video_id = video.get('id')
                url = f"https://www.youtube.com/watch?v={video_id}"
                duration = video.get('duration', 'N/A')
                upload_date = video.get('upload_date', 'N/A')

                if upload_date != 'N/A' and len(upload_date) == 8:
                    upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

                data.append({
                    'Title': title,
                    'URL': url,
                    'Duration (s)': duration,
                    'Upload Date': upload_date
                })

            df = pd.DataFrame(data)

            st.write("✅ **Fetched Playlist Info:**")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name='playlist_videos.csv',
                mime='text/csv',
            )
    else:
        st.warning("Please enter a valid YouTube playlist URL.")
