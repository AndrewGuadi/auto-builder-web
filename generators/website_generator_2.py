from typing import List
from pydantic import BaseModel
from openai import OpenAI

# Initialize the OpenAI client (ensure you have your API key set up via environment variables or otherwise)
client = OpenAI()

class ImageSpec(BaseModel):
    prompt: str   # DALL·E prompt for generating the image
    filename: str # The resource name to save this image as (e.g., "hero.png", "icon1.png", etc.)

class WebsiteSpec(BaseModel):
    html: str
    css: str
    js: str
    images: List[ImageSpec]

def generate_website_spec(details_doc: str) -> WebsiteSpec:
    """
    Uses GPT to produce a website layout (HTML/CSS/JS) plus image specs
    that define which images should be generated and how they should be named.
    """
    # Use the "beta.chat.completions.parse" method if you're leveraging the structured outputs feature.
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert web developer and creative director. "
                    "When given requirements, you decide the website's HTML, CSS, JS, "
                    "and which images should be generated (with prompts and filenames). "
                    "Output a JSON object that strictly adheres to this schema:\n\n"
                    "{\n"
                    "  \"html\": string,\n"
                    "  \"css\": string,\n"
                    "  \"js\": string,\n"
                    "  \"images\": [\n"
                    "    { \"prompt\": string, \"filename\": string }\n"
                    "  ]\n"
                    "}"
                )
            },
            {
                "role": "user",
                "content": (
                    "Design a landing page with the following requirements:\n"
                    f"{details_doc}\n\n"
                    "Include in your JSON the image specs: each with a prompt and filename."
                )
            }
        ],
        response_format=WebsiteSpec,
    )
    
    return completion.choices[0].message.parsed