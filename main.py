# webapp/main.py

import sys
import json
import argparse
from pathlib import Path


# Import modules
from generators.website_generator import generate_website_spec, refine_website_spec, WebsiteSpec
from generators.image_generator import generate_and_save_image
from integrators.asset_integrator import update_website_code
from services.file_manager import write_website_files




def main():
    """
    Main entry point that orchestrates:
      1) Generate or load a WebsiteSpec
      2) Optionally do multiple refinement iterations
      3) Optionally generate images
      4) Integrate image paths
      5) Write the final website
    """
    parser = argparse.ArgumentParser(description="Generate or refine a website with GPT + DALL·E images.")

    # High-level pipeline controls
    parser.add_argument(
        "--details", 
        type=str, 
        default=(
            "We want a modern landing page with a hero section, three feature icons, and a footer."
        ),
        help="Textual requirements for the initial website (passed to GPT)."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini-2024-07-18",  # or "o1-mini-2024-12-17" depending on your plan
        help="Model name to use for GPT calls."
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of refinement iterations after the initial spec is generated."
    )
    parser.add_argument(
        "--improvement",
        type=str,
        default="Please enhance the design and add a testimonial section.",
        help="Instructions for refining the website spec each iteration."
    )
    parser.add_argument(
        "--spec-file",
        type=Path,
        help="Path to an existing website spec JSON file. If provided, skip initial GPT generation unless forced."
    )
    parser.add_argument(
        "--skip-web",
        action="store_true",
        help="Skip the GPT-based website generation (requires --spec-file)."
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Skip the image generation step."
    )
    parser.add_argument(
        "--output-spec",
        type=Path,
        help="If set, save the final WebsiteSpec to this JSON file."
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=Path("output_website/images"),
        help="Directory for generated images."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output_website"),
        help="Directory to store final HTML/CSS/JS files."
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
            # Just load the file. In a real app, you might ask the user
            # if they want to re-generate or refine from scratch.
            print(f"Loading existing website spec from {args.spec_file} (GPT generation not forced).")
            with open(args.spec_file, "r", encoding="utf-8") as f:
                spec_data = json.load(f)
            website_spec = WebsiteSpec(**spec_data)
    else:
        if args.skip_web:
            print("Error: --skip-web is set, but no valid --spec-file provided. Cannot skip GPT generation.")
            sys.exit(1)
        
        # Generate the initial spec from GPT
        print(f"Generating initial website spec from GPT using model: {args.model}")
        website_spec = generate_website_spec(args.details, args.model)

    # -------------------------------------------------------------------------
    # 2) Refinement Iterations (if any)
    # -------------------------------------------------------------------------
    for i in range(1, args.iterations):
        print(f"\n--- Refinement Iteration {i} of {args.iterations - 1} ---")
        website_spec = refine_website_spec(
            website_spec,
            args.improvement,  # Single instruction repeated or dynamically changed
            args.model
        )

    # Display the final spec after all iterations
    print("\nWebsite spec after all iterations:")
    spec_dict = website_spec.model_dump()
    print(json.dumps(spec_dict, indent=2))

    # Optionally save the final spec to a JSON file
    if args.output_spec:
        args.output_spec.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_spec, "w", encoding="utf-8") as f:
            json.dump(spec_dict, f, indent=2)
        print(f"Final WebsiteSpec saved to {args.output_spec}")

    # -------------------------------------------------------------------------
    # 3) Generate images (unless skipped)
    # -------------------------------------------------------------------------
    image_paths = {}
    if args.skip_images:
        print("Skipping image generation step...")
    else:
        for image_spec in website_spec.images:
            local_path = generate_and_save_image(image_spec, args.images_dir)
            if local_path:
                image_paths[image_spec.filename] = local_path.as_posix()

    # -------------------------------------------------------------------------
    # 4) Integrate image paths
    # -------------------------------------------------------------------------
    updated_spec = update_website_code(website_spec, image_paths)

    # -------------------------------------------------------------------------
    # 5) Write final website files
    # -------------------------------------------------------------------------
    write_website_files(updated_spec, args.output_dir)

    print(f"\nAll done! You can now serve the contents of: {args.output_dir}")

if __name__ == "__main__":
    sys.exit(main())
