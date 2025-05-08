import os
try:
    import img2pdf
except ImportError:
    raise ImportError("The 'img2pdf' module is not installed. Please install it using 'pip install img2pdf'.")
from PIL import Image # Used here for image validation before passing to img2pdf
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def convert_image_to_pdf(image_path, pdf_path):
    """
    Converts a single image file to a PDF file, preserving maximum detail.

    Args:
        image_path (str): The absolute path to the input image file.
        pdf_path (str): The absolute path for the output PDF file.

    Returns:
        tuple: (bool, str) indicating success and a message.
    """
    try:
        # Validate that the input is a file and try to open it as an image
        if not os.path.isfile(image_path):
            return False, f"Error: Input path is not a file: '{image_path}'"

        try:
            img = Image.open(image_path)
            img.verify()  # Verifies the integrity of an image file
            img.close()   # Close the image after verification
        except FileNotFoundError:
            return False, f"Error: Input image file not found at '{image_path}'"
        except IsADirectoryError:
            return False, f"Error: Expected an image file, but got a directory: '{image_path}'"
        except Exception as e: # Catches PIL.UnidentifiedImageError and other PIL errors
            return False, f"Error: Could not open or read image file '{image_path}'. It might be corrupted or an unsupported format. Details: {e}"

        # Ensure output directory exists
        output_dir = os.path.dirname(pdf_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return False, f"Error: Could not create output directory '{output_dir}'. Details: {e}"

        # Convert the image to PDF using img2pdf
        # img2pdf handles images losslessly where possible (e.g., JPEGs)
        # or uses lossless compression for other formats.
        with open(image_path, "rb") as img_file:
            pdf_bytes = img2pdf.convert(img_file)
        
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)

        return True, f"Successfully converted '{image_path}' to '{pdf_path}'"

    except img2pdf.ImageOpenError as e: # Specific error from img2pdf if it still fails
        return False, f"Error: img2pdf could not process the image '{image_path}'. Details: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred during PDF conversion: {e}"

class ImageToPdfConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Image to PDF Converter")

        self.input_image_path = tk.StringVar()
        self.output_pdf_path = tk.StringVar()
        self.status_message = tk.StringVar()
        self.status_message.set("Ready. Select an image and an output PDF location.")

        # --- UI Layout ---
        frame = ttk.Frame(master, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input Image
        ttk.Label(frame, text="Input Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.input_image_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_input_image).grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)

        # Output PDF
        ttk.Label(frame, text="Output PDF:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.output_pdf_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_output_pdf).grid(row=1, column=2, sticky=tk.E, padx=5, pady=5)

        # Convert Button
        self.convert_button = ttk.Button(frame, text="Convert to PDF", command=self.convert)
        self.convert_button.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Clear Button
        ttk.Button(frame, text="Clear", command=self.clear_fields).grid(row=2, column=2, pady=10, padx=5, sticky=tk.E)

        # Status Label
        ttk.Label(frame, textvariable=self.status_message, wraplength=480, justify=tk.LEFT).grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Configure column weights for resizing
        frame.columnconfigure(1, weight=1)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

    def browse_input_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=(("Image files", "*.jpeg *.jpg *.png *.bmp *.gif *.tiff *.webp"), ("All files", "*.*"))
        )
        if file_path:
            abs_path = os.path.abspath(file_path)
            self.input_image_path.set(abs_path)
            # Suggest an output path based on input if output is empty
            if not self.output_pdf_path.get():
                base, _ = os.path.splitext(abs_path)
                self.output_pdf_path.set(base + ".pdf")
            self.status_message.set(f"Input: {os.path.basename(abs_path)}")

    def browse_output_pdf(self):
        # Suggest a filename based on input if available
        initial_filename = ""
        input_path = self.input_image_path.get()
        if input_path:
            base, _ = os.path.splitext(os.path.basename(input_path))
            initial_filename = base + ".pdf"
        
        file_path = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            initialfile=initial_filename,
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
        )
        if file_path:
            self.output_pdf_path.set(os.path.abspath(file_path))
            self.status_message.set(f"Output: {os.path.basename(file_path)}")

    def convert(self):
        input_path = self.input_image_path.get()
        output_path = self.output_pdf_path.get()

        if not input_path:
            messagebox.showerror("Error", "Please select an input image file.")
            self.status_message.set("Error: No input image selected.")
            return
        if not output_path:
            messagebox.showerror("Error", "Please specify an output PDF file path.")
            self.status_message.set("Error: No output PDF path specified.")
            return

        self.status_message.set(f"Converting '{os.path.basename(input_path)}'...")
        self.master.update_idletasks() # Update GUI before potentially long operation

        success, message = convert_image_to_pdf(input_path, output_path)
        self.status_message.set(message)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Conversion Failed", message)

    def clear_fields(self):
        self.input_image_path.set("")
        self.output_pdf_path.set("")
        self.status_message.set("Ready. Select an image and an output PDF location.")

def main():
    root = tk.Tk()
    app = ImageToPdfConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()