import os
import requests
from pathlib import Path
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def generate_image(prompt: str, output_dir: Path, filename: str, size: str = "1024x1024", quality: str = "standard") -> Path:
    """
    Uses the OpenAI Images API to generate an image from a text prompt,
    downloads it, and saves it to the specified output directory.
    
    Args:
        prompt (str): The image generation prompt.
        output_dir (Path): The directory where the image will be saved.
        filename (str): The name of the file to save (should include an extension, e.g. 'image.png').
        size (str): The desired image size (default "1024x1024").
        quality (str): The image quality (default "standard").
    
    Returns:
        Path: The path to the saved image.
    """
    # Generate image using the Images API (using DALL·E 3)
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1  # Generate one image
        )
    except Exception as e:
        print("Error generating image:", e)
        return None
    
    # Get the image URL from the response (this URL usually expires after an hour)
    image_url = response.data[0].url
    print("Generated image URL:", image_url)
    
    # Ensure the output directory exists.
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download the image from the URL.
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        file_path = output_dir / filename
        with open(file_path, "wb") as f:
            f.write(image_response.content)
        print(f"Image saved to: {file_path.resolve()}")
        return file_path
    else:
        print("Failed to download image. Status code:", image_response.status_code)
        return None

# Example usage:
if __name__ == "__main__":
    prompt = "a futuristic city skyline at sunset with neon signs"
    images_output_dir = Path("generated_images")
    image_path = generate_image(prompt, images_output_dir, "futuristic_city.png")
