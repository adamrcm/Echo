import os
from src.video_processing import extract_video_frames
from src.prompts import SYSTEM_PROMPTS, get_generation_prompt
from src.inference import generate_caption
from src.evaluator import simulate_llm_judge


def run_pipeline(video_path, mock_visual_description):
    print("=" * 60)
    print(f"🎬 Processing Video: {video_path}")
    print("=" * 60)

    # 1. Video Processing Step
    try:
        metadata = extract_video_frames(video_path)
        print(f"Successfully processed video. Duration: {metadata['duration_seconds']}s")
    except Exception as e:
        print(f"Skipping frame extraction (Using mock data): {e}")
        metadata = {"duration_seconds": 12.5, "total_frames": 375}

    # 2. Construct User Prompt
    user_prompt = get_generation_prompt(metadata, mock_visual_description)

    # 3. Generate and Evaluate for each required style
    results = {}
    for style, system_prompt in SYSTEM_PROMPTS.items():
        print(f"\n🚀 Generating style: [{style.upper()}]...")
        caption = generate_caption(system_prompt, user_prompt)
        print(f"👉 Caption: {caption}")

        print(f"⚖️ Running Local LLM-Judge Evaluation...")
        evaluation = simulate_llm_judge(mock_visual_description, caption, style)
        print(evaluation)
        print("-" * 40)

        results[style] = {"caption": caption, "evaluation": evaluation}


if __name__ == "__main__":
    # Temporary mock scene description until launch day provides video formats/VLM access
    sample_description = (
        "A man tries to assemble a complex piece of flat-pack furniture. He is staring "
        "intently at a confusing instruction manual, holds up a single wooden dowel, "
        "looks at a pile of 50 mismatched screws on the floor, and sighs deeply."
    )

    # Run with a dummy path to test our string/mock pipeline integration
    run_pipeline("data/sample_videos/test_clip.mp4", sample_description)