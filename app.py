import argparse
import os
import img2pdf
from PIL import Image # Used here for image validation before passing to img2pdf

def convert_image_to_pdf(image_path, pdf_path):
    """
    Converts a single image file to a PDF file, preserving maximum detail.

    Args:
        image_path (str): The absolute path to the input image file.
        pdf_path (str): The absolute path for the output PDF file.
    """
    try:
        # Validate that the input is a file and try to open it as an image
        if not os.path.isfile(image_path):
            print(f"Error: Input path is not a file: '{image_path}'")
            return

        try:
            img = Image.open(image_path)
            img.verify()  # Verifies the integrity of an image file
            img.close()   # Close the image after verification
        except FileNotFoundError:
            print(f"Error: Input image file not found at '{image_path}'")
            return
        except IsADirectoryError:
            print(f"Error: Expected an image file, but got a directory: '{image_path}'")
            return
        except Exception as e: # Catches PIL.UnidentifiedImageError and other PIL errors
            print(f"Error: Could not open or read image file '{image_path}'. It might be corrupted or an unsupported format. Details: {e}")
            return

        # Convert the image to PDF using img2pdf
        # img2pdf handles images losslessly where possible (e.g., JPEGs)
        # or uses lossless compression for other formats.
        with open(image_path, "rb") as img_file:
            pdf_bytes = img2pdf.convert(img_file)

        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)

        print(f"Successfully converted '{image_path}' to '{pdf_path}'")

    except img2pdf.ImageOpenError as e: # Specific error from img2pdf if it still fails
        print(f"Error: img2pdf could not process the image '{image_path}'. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during PDF conversion: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert an image file to a PDF file with maximum detail. The image is embedded without recompression if possible."
    )
    parser.add_argument("input_image", help="Path to the input image file.")
    parser.add_argument("output_pdf", help="Path for the output PDF file.")

    args = parser.parse_args()

    # Use absolute paths
    input_image_path = os.path.abspath(args.input_image)
    output_pdf_path = os.path.abspath(args.output_pdf)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_pdf_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}'")

    convert_image_to_pdf(input_image_path, output_pdf_path)

if __name__ == "__main__":
    main()