#!/usr/bin/env python3
import numpy as np
from PIL import Image

def convert_10bit_to_16bit(pixels_10bit):
    # Scale 10-bit pixel values (0-1023) to 16-bit (0-65535)
    return (pixels_10bit * (65535 / 1023)).astype(np.uint16)

def extract_frame_data(mcf_file, start, frame_size, width, height):
    # Seek to the frame data position in the file
    mcf_file.seek(start)
    # Read the frame data
    frame_data = np.frombuffer(mcf_file.read(frame_size), dtype=np.uint16)  # Assuming 10-bit packed in 16-bit
    # Reshape into the frame (height x width)
    return frame_data.reshape((height, width))

# Open the .mcf file
with open('yourfile.mcf', 'rb') as mcf:
    # Assume we have already found the starting point of the frame data
    frame_data_start = 100000  # Example offset where frame data starts
    frame_size_bytes = 1280 * 896 * 2  # 2 bytes per pixel (for 10-bit packed in 16-bit)
    
    # Extract the first frame
    first_frame = extract_frame_data(mcf, frame_data_start, frame_size_bytes, 1280, 896)
    
    # Convert the 10-bit data to 16-bit
    frame_16bit = convert_10bit_to_16bit(first_frame)
    
    # Save the frame as a TIFF file
    img = Image.fromarray(frame_16bit)
    img.save('frame0.tiff')

    # Repeat for subsequent frames by incrementing the start position

