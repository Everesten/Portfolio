from PIL import Image
import numpy as np

def image_to_list(image_file):

    image = Image.open(image_file)

    # Check for RGB here
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixel_array = []
    pixels = image.load()

    # Dimensions
    width, height = image.size
  
    for j in range(height):
        row = []
        for i in range(width):
            row.append(pixels[i,j])
        pixel_array.append(row)
    return pixel_array

def output_image(pixel_grid,filename):
    img = Image.fromarray(np.array(pixel_grid).astype(np.uint8), "RGB")
    img.save(filename)
     
def show_image(pixel_grid):
    img = Image.fromarray(np.array(pixel_grid).astype(np.uint8), "RGB")
    img.show()
