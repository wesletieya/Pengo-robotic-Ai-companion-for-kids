import os
from PIL import Image

def process_images(source_dir, destination_dir, new_width, new_height):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Iterate over all files in the source directory
    for i, file_name in enumerate(files):
        # Construct full file path
        file_path = os.path.join(source_dir, file_name)

        # Open an image file
        with Image.open(file_path) as img:
            # Resize the image
            img = img.resize((new_width, new_height))

            # Convert the image to grayscale
            img = img.convert("L")

            # Create a new name for the image
            new_file_name = f'image_{i+641}.jpg'
            new_file_path = os.path.join(destination_dir, new_file_name)

            # Save the image to the destination directory
            img.save(new_file_path)

# Parameters
source_directory = r'C:\Users\ayabe\vs projects\teeth_brushing\people using toothbrush'
destination_directory = r'C:\Users\ayabe\vs projects\data_teeth_brushing\brushing'
width, height = 512,512 

# Process the images
process_images(source_directory, destination_directory, width, height)
