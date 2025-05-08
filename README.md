# pdf-maker
make a pdf of any image into pdf and save it 
# Image to PDF Converter (Max Detail)

This Python script converts an image file (e.g., JPG, PNG, TIFF) into a PDF document,
focusing on preserving as much image detail as possible. It uses the `img2pdf`
library, which embeds images into PDFs without re-compressing them if they are
already in a suitable format (like JPEG), or uses lossless compression otherwise.

## Features

- Preserves original image quality and resolution.
- Supports a wide range of image formats (via Pillow).
- Command-line interface.
- Pure Python solution with easily installable dependencies.

## Requirements

- Python 3.7+
- Pillow
- img2pdf

## Setup

1.  Clone or download this project.
2.  Navigate to the project directory (e.g., `/tmp/image_detail_pdf_converter/`).
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from your terminal:

```bash
python image_to_pdf.py /path/to/your/input_image.jpg /path/to/your/output_document.pdf
```

Replace `/path/to/your/input_image.jpg` with the actual path to your image file and `/path/to/your/output_document.pdf` with your desired output PDF file path. The script will use absolute paths for processing.

For example:
```bash
python /tmp/image_detail_pdf_converter/image_to_pdf.py "my vacation photo.png" "vacation_photo_converted.pdf"
```

This will create `vacation_photo_converted.pdf` in the current working directory (if a full path isn't specified for the output) or at the specified absolute path.