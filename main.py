import os
import requests
import json

from src.video_processing import extract_video_frames
from src.prompts import SYSTEM_PROMPTS, get_generation_prompt
from src.inference import analyze_video_frame
from src.evaluator import simulate_llm_judge
from src.inference import analyze_video_frame, generate_caption


def run_pipeline(video_path, mock_visual_description):
    print("=" * 60)
    print(f"🎬 Processing Video: {video_path}")
    print("=" * 60)

    try:
        metadata = extract_video_frames(video_path)
        print(f"Successfully processed video. Duration: {metadata['duration_seconds']}s")
    except Exception as e:
        print(f"Skipping frame extraction (Using mock data): {e}")
        metadata = {"duration_seconds": 13.0, "total_frames": 390}


    try:
        print("📸 Analyzing video frames...")
        dynamic_description = analyze_video_frame("data/sample_videos/frame.jpg")
        print(f"📝 Generated Visual Description:\n{dynamic_description}")
    except Exception as e:
        print(f"⚠️ Vision analysis failed, falling back to mock description: {e}")
        dynamic_description = mock_visual_description


    model_id = "accounts/fireworks/models/llama-v3-8b-instruct"
    user_prompt = get_generation_prompt(metadata, dynamic_description)


    results = {}
    for style, system_prompt in SYSTEM_PROMPTS.items():
        print(f"\n🚀 Generating style: [{style.upper()}]...")

        model_id = "accounts/fireworks/models/deepseek-v4-pro"

        caption = generate_caption(
            system_prompt,
            user_prompt,
            model=model_id
        )
        print(f"👉 Caption: {caption}")

        print(f"⚖️ Running Local LLM-Judge Evaluation...")
        evaluation = simulate_llm_judge(
            dynamic_description,
            caption,
            style,
            model=model_id
        )
        print(evaluation)
        print("-" * 40)

        results[style] = {"caption": caption, "evaluation": evaluation}
    return results

if __name__ == "__main__":

    sample_description = (
        "A man tries to assemble a complex piece of flat-pack furniture. He is staring "
        "intently at a confusing instruction manual, holds up a single wooden dowel, "
        "looks at a pile of 50 mismatched screws on the floor, and sighs deeply."
    )


    run_pipeline("data/sample_videos/test_clip.mp4", sample_description)


