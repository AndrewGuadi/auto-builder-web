# webapp/services/file_manager.py

from pathlib import Path
from generators.website_generator import WebsiteSpec

def write_website_files(website_spec: WebsiteSpec, output_dir: Path):
    """
    Writes the website code to index.html, styles.css, and main.js in output_dir.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "index.html"
    css_path = output_dir / "styles.css"
    js_path = output_dir / "main.js"

    html_path.write_text(website_spec.html, encoding="utf-8")
    css_path.write_text(website_spec.css, encoding="utf-8")
    js_path.write_text(website_spec.js, encoding="utf-8")

    print(f"Website files written to: {output_dir.resolve()}")
