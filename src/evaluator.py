from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.getenv("FIREWORKS_API_KEY", "mock_key_for_now")
)

def simulate_llm_judge(visual_description, generated_caption, target_style):
    """
    Simulates the hackathon's LLM-Judge to grade accuracy and tone adherence.
    """
    eval_prompt = f"""
You are an expert Hackathon Judge scoring a Video Captioning challenge.
Target Style: {target_style}
Original Video Description: {visual_description}
Generated Caption to Evaluate: "{generated_caption}"

Evaluate the caption on two metrics from 1 to 5 (5 being perfect):
1. Accuracy: Does it correctly reflect the events in the video description?
2. Tone: Does it perfectly execute the requested style ({target_style})?

Provide your output strictly in this format:
Accuracy: [score]/5
Tone: [score]/5
Reasoning: [one sentence summary]
"""

    try:
        response = client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p1-70b-instruct", # Use a larger model to judge if possible
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Evaluation failed: {str(e)}"