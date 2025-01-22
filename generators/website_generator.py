# webapp/generators/website_generator.py

from typing import List, Optional
from pydantic import BaseModel
from openai import OpenAI

# Initialize the OpenAI client (ensure you have your API key set up)
client = OpenAI()

class ImageSpec(BaseModel):
    prompt: str
    filename: str

class WebsiteSpec(BaseModel):
    html: str
    css: str
    js: str
    images: List[ImageSpec]

def generate_website_spec(details_doc: str, model_name: str) -> WebsiteSpec:
    """
    Uses GPT to produce an initial website spec (HTML/CSS/JS) plus
    image specs. 
    """
    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert web developer and creative director. "
                    "When given requirements, you decide the website's HTML, CSS, JS, "
                    "and which images should be generated (with prompts and filenames; files will be kept in images directory and tagged as such in src). "
                    "Output a JSON object that strictly follows the WebsiteSpec schema:\n\n"
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

def refine_website_spec(current_spec: WebsiteSpec, improvement_instructions: str, model_name: str) -> WebsiteSpec:
    """
    Refines an existing WebsiteSpec based on some improvement or refinement instructions.
    We supply the current code and any user-specified improvement instructions to GPT.
    """
    # Convert the current spec to a textual representation
    current_code = (
        f"HTML:\n{current_spec.html}\n\n"
        f"CSS:\n{current_spec.css}\n\n"
        f"JS:\n{current_spec.js}\n\n"
        "IMAGES:\n"
        + "\n".join(
            [f"- {img.filename}: {img.prompt}" for img in current_spec.images]
        )
    )

    refinement_prompt = (
        "Here is the current website specification:\n"
        f"{current_code}\n\n"
        "Please refine or improve it based on these additional instructions:\n"
        f"{improvement_instructions}\n\n"
        "Output a JSON object that still strictly follows the WebsiteSpec schema."
    )

    completion = client.beta.chat.completions.parse(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert web developer and creative director. "
                    "You refine existing website code (HTML, CSS, JS, images) based on improvement instructions."
                )
            },
            {
                "role": "user",
                "content": refinement_prompt
            }
        ],
        response_format=WebsiteSpec,
    )
    return completion.choices[0].message.parsed
