# webapp/main.py

import sys
import json
import argparse
from pathlib import Path

# Import modules
from generators.website_generator import generate_website_spec, WebsiteSpec
from generators.image_generator import generate_and_save_image
from integrators.asset_integrator import update_website_code
from services.file_manager import write_website_files

def main():
    """
    Main entry point that orchestrates the whole pipeline:
      1) Generate or load an existing WebsiteSpec
      2) Optionally generate images
      3) Integrate image paths into the website code
      4) Write final files
      5) Provide command-line arguments for skipping or reusing previous steps
    """
    parser = argparse.ArgumentParser(description="Generate a website from GPT code + DALL·E images.")
    
    # High-level pipeline controls
    parser.add_argument(
        "--details", 
        type=str, 
        default="We want a modern landing page with a hero section, three feature icons, and a footer...",
        help="Textual requirements for the website (passed to GPT)."
    )
    parser.add_argument(
        "--spec-file",
        type=Path,
        help="Path to an existing website spec JSON file. If provided, we skip GPT generation unless forced."
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip the image generation step (useful if images are already generated)."
    )
    parser.add_argument(
        "--skip-web",
        action="store_true",
        help="Skip the GPT-based website generation (requires --spec-file)."
    )
    
    # I/O controls
    parser.add_argument(
        "--output-spec",
        type=Path,
        help="If set, save the generated WebsiteSpec to this JSON file (for reuse later)."
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=Path("output_website/images"),
        help="Directory in which to store generated images."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output_website"),
        help="Directory in which to store the final HTML/CSS/JS files."
    )
    
    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # 1) Generate or load the WebsiteSpec
    # -------------------------------------------------------------------------
    if args.spec_file and args.spec_file.exists():
        if args.skip_web:
            # Load the existing spec from JSON, skipping GPT entirely
            print(f"Loading existing website spec from {args.spec_file}")
            with open(args.spec_file, "r", encoding="utf-8") as f:
                spec_data = json.load(f)
            website_spec = WebsiteSpec(**spec_data)
        else:
            # If we are not skipping GPT, we could re-generate or confirm usage
            # For clarity, let's just load the file. 
            # In a real app, you might prompt the user or force re-generation.
            print(f"Loading existing website spec from {args.spec_file} (GPT generation not forced).")
            with open(args.spec_file, "r", encoding="utf-8") as f:
                spec_data = json.load(f)
            website_spec = WebsiteSpec(**spec_data)
    else:
        if args.skip_web:
            print("Error: --skip-web is set, but no valid --spec-file provided. Cannot skip GPT generation.")
            sys.exit(1)
        
        # Generate the spec from GPT
        print("Generating website spec from GPT...")
        website_spec = generate_website_spec(args.details)
        
        # Optionally save the spec to a JSON file for reuse
        if args.output_spec:
            args.output_spec.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output_spec, "w", encoding="utf-8") as f:
                json.dump(website_spec.model_dump(), f, indent=2)
            print(f"Website spec saved to {args.output_spec}")

    # Display the loaded or generated spec
    print("Website spec generated or loaded:")
    print(json.dumps(website_spec.model_dump(), indent=2))

    # -------------------------------------------------------------------------
    # 2) Generate images (unless skipped)
    # -------------------------------------------------------------------------
    image_paths = {}
    if args.skip_images:
        print("Skipping image generation step...")
    else:
        # Go through each image and generate it
        for image_spec in website_spec.images:
            local_path = generate_and_save_image(image_spec, args.images_dir)
            if local_path:
                image_paths[image_spec.filename] = local_path.as_posix()

    # -------------------------------------------------------------------------
    # 3) Integrate image paths into the website code
    # -------------------------------------------------------------------------
    updated_spec = update_website_code(website_spec, image_paths)

    # -------------------------------------------------------------------------
    # 4) Write final website files
    # -------------------------------------------------------------------------
    write_website_files(updated_spec, args.output_dir)

    print("All done! You can now serve the contents of:", args.output_dir)

if __name__ == "__main__":
    sys.exit(main())
