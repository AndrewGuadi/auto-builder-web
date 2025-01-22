import os
from pathlib import Path
from pydantic import BaseModel
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Define the Pydantic schema for our website code.
class WebsiteCode(BaseModel):
    html: str
    css: str
    js: str

def build_website(details_doc: str) -> WebsiteCode:
    """
    Build the HTML, CSS, and JavaScript for a landing page that meets the specified requirements.
    The assistant's output will conform to the WebsiteCode schema.
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert web developer who creates production-ready websites with HTML, CSS, and JavaScript. "
                    "When provided a set of requirements, return only a valid JSON object that has three keys: 'html', 'css', and 'js'. "
                    "Each should contain the respective code as a string."
                )
            },
            {
                "role": "user",
                "content": (
                    "Build me a landing page that meets the following requirements: "
                    f"{details_doc}"
                )
            }
        ],
        response_format=WebsiteCode,  # Use our Pydantic model to enforce the output schema.
    )

    website_code = completion.choices[0].message.parsed
    return website_code

def write_files(website_code: WebsiteCode, output_dir: Path):
    """
    Writes the generated website code to separate files in the specified directory.
    """
    # Ensure the output directory exists.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define file paths.
    html_file = output_dir / "index.html"
    css_file  = output_dir / "styles.css"
    js_file   = output_dir / "main.js"

    # Write the content to each file.
    html_file.write_text(website_code.html, encoding="utf-8")
    css_file.write_text(website_code.css, encoding="utf-8")
    js_file.write_text(website_code.js, encoding="utf-8")
    
    print(f"Website files written to: {output_dir.resolve()}")

if __name__ == "__main__":
    # Define the requirements for the landing page.
    details = (
        "The landing page should have a modern design with clear call-to-action buttons, a responsive layout, "
        "an input field for email submissions, animations on hover, and a sticky navigation menu."
    )
    # Build the website code.
    website_code = build_website(details)
    
    # Define an output directory for the website files.
    output_directory = Path("output_website")
    
    # Write the generated code to files.
    write_files(website_code, output_directory)
