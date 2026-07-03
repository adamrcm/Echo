import os
from openai import OpenAI


client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="fw_6W1f5dfrb6GEmEjyGk8KqM"
)

def generate_caption(system_prompt, user_prompt, model="accounts/fireworks/models/deepseek-v4-pro"):
    """
    Calls the Fireworks AI API to generate a caption based on a specific style.
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