import os
import base64
from openai import OpenAI

# Initialize OpenAI SDK pointed directly at Fireworks AI
client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ.get("FIREWORKS_API_KEY", "fw_Q5W83bWvL7tdJoomzKZ6LF")
)

def generate_caption(system_prompt, user_prompt, model="accounts/fireworks/models/deepseek-v4-pro"):
    """
    Generates a caption style variation using DeepSeek-V4-Pro.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API Error: {str(e)}"


def analyze_video_frame(image_path="data/sample_videos/frame.jpg"):
    """
    Encodes a local frame image to base64 and uses Qwen3.7 Plus to describe the scene.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No extracted frame found at {image_path} to analyze.")

    # Read and encode the image to base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    print("👁️  Sending video frame to Vision LLM for analysis...")
    try:
        response = client.chat.completions.create(
            model="accounts/fireworks/models/qwen3p7-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe what is happening in this video frame in clear, objective detail. Focus on the main subject, actions, and setting. Keep it to 2-3 detailed sentences."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Vision API Error: {str(e)}"