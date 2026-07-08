import os
import streamlit as st
from main import run_pipeline

# Configure the page layout
st.set_page_config(page_title="Echo - Video Captioning Engine", layout="wide")

st.title("🎬 Echo: AI Video Captioning & Evaluation")
st.markdown("Upload a video clip to generate multi-style captions evaluated by an LLM-Judge.")

# Sidebar configuration
st.sidebar.header("Pipeline Configurations")
video_file = st.sidebar.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

if video_file:
    # Ensure a local directory exists to save the uploaded file
    os.makedirs("data/sample_videos", exist_ok=True)
    target_path = os.path.join("data/sample_videos", video_file.name)

    # Save video file locally for processing
    with open(target_path, "wb") as f:
        f.write(video_file.getbuffer())

    st.sidebar.success(f"Loaded: {video_file.name}")

    # Render a video player preview in the UI
    st.video(target_path)

    if st.button("🚀 Run Captioning Pipeline", type="primary"):
        with st.spinner("Processing video frames and running LLM tracks..."):
            try:
                # Provide an empty string or standard fallback fallback descriptor text
                mock_fallback = "A video clip waiting for dynamic vision API processing."

                # Execute your verified main pipeline function
                pipeline_results = run_pipeline(target_path, mock_fallback)

                st.success("✅ Pipeline Executed Successfully!")
                st.divider()

                st.subheader("💡 Generated Variations & Judge Scores")

                # Create 4 distinct tab sections dynamically based on your styles dictionary
                style_names = [style.upper() for style in pipeline_results.keys()]
                tabs = st.tabs(style_names)

                # Zip your tabs together with the results data to keep them isolated and clean
                for tab, (style, data) in zip(tabs, pipeline_results.items()):
                    with tab:
                        st.markdown(f"### Track Persona: `{style.upper()}`")

                        st.markdown("#### 📝 Generated Caption:")
                        st.info(data.get("caption", "N/A"))

                        st.markdown("#### ⚖️ LLM-Judge Evaluation Summary:")
                        st.code(data.get("evaluation", "N/A"), language="markdown")

            except Exception as e:
                st.error(f"Pipeline Error encountered: {str(e)}")
else:
    st.info("👈 Please drop a video file into the sidebar uploader to begin.")
