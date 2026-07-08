import os
import base64
from openai import OpenAI
import re



client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.environ.get("FIREWORKS_API_KEY", "your_api_key")
)

import re


def generate_caption(system_prompt, user_prompt, model="accounts/fireworks/models/deepseek-v4-pro"):

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        raw_content = response.choices[0].message.content.strip()


        tag_match = re.search(r"<caption_output>(.*?)</caption_output>", raw_content, re.DOTALL)
        if tag_match:
            return tag_match.group(1).strip()


        if "<caption_output>" in raw_content:
            clean_split = raw_content.split("<caption_output>")[-1].replace("</caption_output>", "")
            return clean_split.strip()


        lines = [line.strip() for line in raw_content.split('\n') if line.strip()]
        if lines:

            last_line = lines[-1]

            if (last_line.startswith('"') and last_line.endswith('"')) or (
                    last_line.startswith("'") and last_line.endswith("'")):
                return last_line[1:-1].strip()


            if len(lines) > 1 and (
                    last_line.lower().startswith("or ") or last_line.endswith(":") or len(last_line) < 15):
                fallback_line = lines[-2]
                return fallback_line.strip(' "')

            return last_line.strip(' "')

        return raw_content

    except Exception as e:
        return f"API Error: {str(e)}"


def analyze_video_frame(image_path="data/sample_videos/frame.jpg"):

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