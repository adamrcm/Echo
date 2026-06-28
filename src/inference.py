import os
from openai import OpenAI

# Initialize the client. Fireworks uses standard OpenAI structure.
# Make sure to set your FIREWORKS_API_KEY environment variable.
client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=os.getenv("FIREWORKS_API_KEY", "mock_key_for_now")
)

def generate_caption(system_prompt, user_prompt, model="accounts/fireworks/models/llama-v3p1-8b-instruct"):
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
            temperature=0.8, # Slightly higher temperature for better humor/creativity
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API Error: {str(e)}"