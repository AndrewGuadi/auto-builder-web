
# Auto Builder Web

A modular tool to generate and iteratively refine a website using GPT for code (HTML, CSS, JS) generation and DALL·E for image creation. This project is designed to allow you to continuously improve your website design (including UX/UI, responsiveness, and SEO) via iterative refinements while reusing previous specifications.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Generating an Initial Website Spec](#generating-an-initial-website-spec)
  - [Iterative Refinement](#iterative-refinement)
  - [Generating Images](#generating-images)
- [Command-Line Arguments](#command-line-arguments)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Overview

This project uses a modular approach to generate a website using GPT and iteratively refine it according to your improvement instructions. The system also integrates DALL·E image generation so that your website can include rich media content. You can save the generated website specification (a JSON file containing HTML, CSS, JS, and image details) to reuse or further improve your website later.

## Directory Structure

```
auto-builder-web/
├── webapp/
│   ├── main.py                  # Main orchestrator script
│   ├── generators/
│   │   ├── website_generator.py # GPT-based website spec generation and refinement
│   │   └── image_generator.py   # DALL·E image generation and saving
│   ├── integrators/
│   │   └── asset_integrator.py  # Integrates image paths into website code
│   ├── services/
│   │   └── file_manager.py      # Writes out the final website files to disk
│   └── README.md                # This file!
└── requirements.txt             # Python package dependencies
```

## Requirements

- Python 3.8+
- An OpenAI API key (set in your environment as `OPENAI_API_KEY`)
- The following Python packages (see `requirements.txt`):
  - `openai`
  - `requests`
  - `pydantic`

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/auto-builder-web.git
   cd auto-builder-web
   ```

2. **Create a Virtual Environment and Install Dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Your OpenAI API Key:**

   Make sure your OpenAI API key is available in your environment:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

## Usage

The project is driven by the `main.py` script, which has several command-line arguments to control the pipeline—from initial generation to iterative refinement and image generation.

### Generating an Initial Website Spec

To generate a website spec from scratch and save it to a JSON file:

```bash
python webapp/main.py   --details "I want a heartfelt website for my grandmother's 86th birthday. She was born on January 22, 1939. The website should feature a beautiful hero section, a timeline of her life, messages from family, and photos of memorable moments. It should have a warm, inviting design with accessible, responsive CSS and be optimized for SEO with clear meta tags and semantic HTML."   --model gpt-4o-2024-08-06   --iterations 1   --improvement "Initial generation, no refinements yet."   --output-spec website_spec.json
```

### Iterative Refinement

To load an existing specification and iteratively refine it:

```bash
python webapp/main.py   --spec-file website_spec.json   --skip-web   --model gpt-4o-2024-08-06   --iterations 15   --improvement "Enhance the CSS for a warm, elegant look; improve UX/UI for accessibility; add SEO-friendly meta tags and semantic HTML; emphasize her birthday, key life milestones, and include refined imagery. Generate all images as defined in the spec."   --output-spec refined_website_spec.json
```

### Generating Images

If you do not use the `--skip-images` flag, the script will generate images using DALL·E for each image prompt found in the specification. The images are saved in the directory specified by `--images-dir` (default is `output_website/images`).

## Command-Line Arguments

- `--details`: Textual requirements for the website (only used if generating an initial spec).
- `--model`: GPT model name to use (e.g., gpt-4o-2024-08-06). Default: `gpt-4o-2024-08-06`
- `--iterations`: Number of iterations (the initial generation is counted as one; subsequent iterations refine the spec). Default: `1`
- `--improvement`: Instructions provided to refine the website spec during each iteration.
- `--spec-file`: Path to an existing WebsiteSpec JSON file. If provided (and the file exists), the script loads this file instead of calling GPT to generate a new spec.
- `--skip-web`: If set, the script skips GPT-based website generation. This requires that a valid `--spec-file` is provided.
- `--skip-images`: If set, the script skips the image generation step.
- `--output-spec`: If provided, the final WebsiteSpec (after generation/refinement) is saved to this JSON file.
- `--images-dir`: Directory where generated images will be saved. Default: `output_website/images`
- `--output-dir`: Directory to write the final HTML, CSS, and JS files. Default: `output_website`

## Examples

1. **Generate a New Website Spec for a Grandmother's 86th Birthday**
   ```bash
   python webapp/main.py      --details "I want a heartfelt website for my grandmother's 86th birthday..."      --model gpt-4o-2024-08-06      --iterations 1      --improvement "Initial generation, no refinements yet."      --output-spec website_spec.json
   ```

2. **Refine an Existing Spec and Generate Images**
   ```bash
   python webapp/main.py      --spec-file website_spec.json      --model gpt-4o-2024-08-06      --iterations 15      --improvement "Enhance the CSS for a warm, elegant look..."      --output-spec refined_website_spec.json
   ```

3. **Refine Without Regenerating Images**
   ```bash
   python webapp/main.py      --spec-file website_spec.json      --skip-images      --model gpt-4o-2024-08-06      --iterations 15      --improvement "Refine the design and content for improved clarity..."      --output-spec refined_website_spec.json
   ```

## Troubleshooting

- **FileNotFoundError for Images:** Verify that your image filenames in the WebsiteSpec do not include redundant path segments.
- **Missing Spec File:** Use the `--output-spec` flag during initial generation to create a `website_spec.json` file, then reuse it with the `--spec-file` flag.
- **API Key Issues:** Ensure that your OpenAI API key is correctly set in your environment.

## Future Improvements

- Automated Testing: Integrate automated checks to ensure your website’s HTML, CSS, and SEO meet best practices.
- Refinement Feedback: Enhance the iterative process by prompting for more granular or dynamic improvement instructions.
- Version Control: Use Git to maintain versions of your WebsiteSpec and track improvements over iterations.

## License

MIT License

## Acknowledgments

Special thanks to the OpenAI API for powering the GPT and DALL·E capabilities in this project.
