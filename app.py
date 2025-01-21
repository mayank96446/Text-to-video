import json
import streamlit as st
import requests
import time

# App Title
st.title("AI-Powered Text-to-Video Converter")

# API Configuration
API_URL = "https://viralapi.vadoo.tv/api/generate_video"
API_KEY = "b012WZ2B6mgTRt04b-I7ATcGTmCsSVukHtIqIfJRazE"  # Replace with your actual API key

with st.form("video_form"):
    text = st.text_area("Enter the text/script for the video (max 10000 characters):", height=150)
    voice = st.selectbox("Select Voice:", ["Charlie", "Default"])
    theme = st.selectbox("Select Caption Style (Theme):", ["Hormozi_1", "Default"])
    style = st.selectbox("Select AI Image Style:", ["None", "Default"])
    language = st.selectbox("Select Language:", ["English", "Spanish", "French"])
    duration = st.selectbox(
        "Select Video Duration:", ["30-60", "60-90", "90-120", "5 min", "10 min"]
    )
    aspect_ratio = st.selectbox("Select Aspect Ratio:", ["9:16", "1:1", "16:9"])
    use_ai = st.selectbox("Use AI to Modify Script:", ["1 (Yes)", "0 (No)"])
    submitted = st.form_submit_button("Generate Video")

if submitted:
    char_limit = {
        "30-60": 1000,
        "60-90": 1500,
        "90-120": 2000,
        "5 min": 5000,
        "10 min": 10000,
    }

    script_length = len(text.strip())
    if script_length == 0:
        st.warning("Please enter a valid text/script.")
    elif script_length > char_limit[duration]:
        st.warning(f"Text exceeds the {char_limit[duration]} characters limit for {duration} duration.")
    else:
        st.info("Generating your video... This may take a few minutes.")

        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json",
        }

        payload = {
            "topic": "Custom",
            "voice": voice,
            "theme": theme,
            "style": style,
            "language": language,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "use_ai": int(use_ai.split(" ")[0]),
            "url": None,
        }

        try:
            print("Sending Request to API...")
            print("Payload:", json.dumps(payload, indent=2))
            print("Headers:", headers)

            response = requests.post(API_URL, data=json.dumps(payload), headers=headers)

            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)

            if response.status_code == 200:
                data = response.json()
                vid = data.get("vid")
                if vid:
                    st.success(f"Video generated successfully! Video ID: {vid}")
                    st.info("Video will be available for 30 minutes.")
                else:
                    st.error("No video ID received. Please check the API response.")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")


# Footer
st.write("Powered by Vadoo AI API")

