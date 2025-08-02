import cohere
from dotenv import load_dotenv
import os

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY1")
co = cohere.Client(cohere_api_key)

def generate_roadmap_for_topic(topic):
    topic = topic.strip()

    prompt = f"""Create a step-by-step learning roadmap for the topic "{topic}". 
Start from beginner concepts and go to advanced topics. List the roadmap as numbered steps."""

    try:
        response = co.generate(
    model='command',
    prompt=prompt,
    max_tokens=400,
    temperature=0.6
)

        roadmap = response.generations[0].text.strip()
        return roadmap

    except Exception as e:
        return f"❌ Error generating roadmap: {str(e)}"
