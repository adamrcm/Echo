# Echo: Multi-Persona Video Captioning Engine & Evaluation Pipeline

Echo is an automated video processing and captioning pipeline that generates contextual captions across four distinct style tracks, automatically evaluated by a local LLM-Judge for accuracy and tone. It features an interactive, user-friendly Streamlit dashboard to upload videos, track pipeline execution stages, and review results side-by-side.


## 🛠️ Project Architecture

```text
Echo/
├── src/
│   ├── video_processing.py  # Handles frame extraction via OpenCV
│   ├── prompts.py           # Stores strict persona system instructions & prompt templates
│   ├── inference.py         # Configures Fireworks AI endpoints & regex parsing filters
│   └── evaluator.py         # Runs the automated LLM-Judge criteria scoring
├── data/
│   └── sample_videos/       # Local directory for video uploads and extracted frames
├── app.py                   # Streamlit web dashboard interface
├── main.py                  # Core backend orchestration pipeline script
├── requirements.txt         # Project package dependencies manifest
└── .env.example             # Template file for required credential setups