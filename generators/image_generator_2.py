# webapp/generators/image_generator.py

import requests
from pathlib import Path
from openai import OpenAI
from .website_generator import ImageSpec

# Reuse or initialize a new OpenAI client
client = OpenAI()

def generate_and_save_image(image_spec: ImageSpec, output_dir: Path, size: str = "1024x1024", quality: str = "standard") -> Path:
    """
    Calls the OpenAI Images API to generate an image based on image_spec.prompt.
    Saves the image to output_dir under image_spec.filename.
    Returns the local file path if successful, or None if there's an error.
    """
    try:
        response = client.images.generate(
            model="dall-e-3",  # or "dall-e-2"
            prompt=image_spec.prompt,
            size=size,
            quality=quality,
            n=1
        )
    except Exception as e:
        print(f"Error generating image for prompt '{image_spec.prompt}': {e}")
        return None

    if not response.data or not response.data[0].url:
        print("No valid image URL returned.")
        return None

    image_url = response.data[0].url
    print(f"Generated image URL for prompt '{image_spec.prompt}': {image_url}")

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / image_spec.filename

    # Download the image
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(image_response.content)
        print(f"Image saved to: {file_path.resolve()}")
        return file_path
    else:
        print(f"Failed to download image. Status code: {image_response.status_code}")
        return None
