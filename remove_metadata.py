#Author: Visahl Samson David Selvam

import os
import shutil
from PIL import Image
from mutagen import File as MutagenFile
import PyPDF2

# Function to remove metadata from images
def remove_image_metadata(file_path):
    image = Image.open(file_path)
    data = list(image.getdata())  # Copy image data
    image_no_meta = Image.new(image.mode, image.size)
    image_no_meta.putdata(data)
    
    # Save image without metadata
    output_file = f"{os.path.splitext(file_path)[0]}_no_meta.jpg"
    image_no_meta.save(output_file)
    print(f"Image metadata removed: {output_file}")

# Function to remove metadata from audio files
def remove_audio_metadata(file_path):
    audio_file = MutagenFile(file_path)
    
    if audio_file:
        audio_file.delete()  # Delete all metadata
        audio_file.save()
        print(f"Audio metadata removed: {file_path}")
    else:
        print(f"Unsupported audio format or no metadata found for: {file_path}")

# Function to remove metadata from PDF files
def remove_pdf_metadata(file_path):
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        writer = PyPDF2.PdfWriter()

        # Copy all pages to a new PDF without metadata
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Output PDF without metadata
        output_file = f"{os.path.splitext(file_path)[0]}_no_meta.pdf"
        with open(output_file, 'wb') as new_pdf_file:
            writer.write(new_pdf_file)

        print(f"PDF metadata removed: {output_file}")

# General function to detect and remove metadata
def remove_metadata(file_path):
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    file_type = file_path.lower()
    
    if file_type.endswith(('.jpg', '.jpeg', '.png', '.tiff')):
        remove_image_metadata(file_path)
    elif file_type.endswith(('.mp3', '.flac', '.wav', '.m4a')):
        remove_audio_metadata(file_path)
    elif file_type.endswith('.pdf'):
        remove_pdf_metadata(file_path)
    else:
        print("Unsupported file type or no metadata removal available.")

# Main function to handle file input
def main():
    file_path = input("Enter the full path of the file to remove metadata from: ")
    remove_metadata(file_path)

if __name__ == '__main__':
    main()
