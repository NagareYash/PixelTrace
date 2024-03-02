#Importing Required Modules
import os
from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt


#Defining Constants and Variables
TEMPORARY_IMAGE_PATH = 'Result/Temporary_Image.jpg'
SCALE_FACTOR = 20
DIFFERENCE_THRESHOLD = 50
MARK_COLOR = (255, 0, 0)  # red
BACKGROUND_COLOR = (0, 0, 0)  # black


#Defining ELA function
def Error_Level_Analysis(ORIGINAL_IMAGE_PATH):
    
    # Create a new directory to store the output files
    if not os.path.exists('Result'):
        os.makedirs('Result')

    print('''\n
                --> Starting Image Processing...
        ''')
    
    original_image = Image.open(ORIGINAL_IMAGE_PATH)

    print('''
                --> Compressing Image...
        ''')
    
    original_image.save(TEMPORARY_IMAGE_PATH, quality=90)

    print('''
                --> Creating Temporary Image...
        ''')
    
    temporary_image = Image.open(TEMPORARY_IMAGE_PATH)

    print('''
                --> Processing for ELA...
        ''')
    
    #Comparing both images pixel by pixel 
    difference = ImageChops.difference(original_image, temporary_image)
    pixel_data = difference.load()
    width, height = difference.size


    # Create a new image to hold the marked pixels
    marked_image = Image.new('RGB', (width, height), BACKGROUND_COLOR)
    pixel_mark = marked_image.load()


    # Loop through each pixel and mark the ones with a difference above the threshold
    for x in range(width):
        for y in range(height):
            pixel_diff = sum(pixel_data[x, y])
            if pixel_diff > DIFFERENCE_THRESHOLD:
                # Increase the intensity of the mark by multiplying the color values
                # with the difference between the pixel value and threshold
                intensity = (pixel_diff - DIFFERENCE_THRESHOLD) * SCALE_FACTOR
                pixel_mark[x, y] = tuple(min(c * intensity, 255) for c in MARK_COLOR)

    print('''
                Processed!
        ''')


    # Save the marked image
    marked_image.save('Result/Result_Image.jpg')


    # Scan the marked image for differences and print whether the image is authentic or tampered
    is_authentic = True
    for x in range(width):
        for y in range(height):
            if pixel_mark[x, y] != BACKGROUND_COLOR:
                print(f'''
Result:
                The Image is not authentic
                ''')
                
                is_authentic = False
                break
        if not is_authentic:
            break

    if is_authentic:
        print(f'''
Result:
                The Image is authentic''')


    # Save the authenticity to a file
    with open("Result/authenticity.txt", "w") as f:
        f.write("The Image is authentic" if is_authentic else "The Image is not authentic")
    

    # Create a heatmap from the pixel data
    pixel_values = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            pixel_values[y][x] = sum(pixel_data[x, y])
    plt.imshow(pixel_values, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Heatmap')

    # Save the heatmap as a file
    plt.savefig('Result/Heatmap Graph.png')

    # Save Original Image to file
    original_image.save('Result/Original_Image.jpg')

    print("Result Saved to:")
    print(f'''
                {os.path.abspath("Result")}
        ''')


if __name__ == '__main__':
    print('''
                
                ██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗██████╗  █████╗  ██████╗███████╗
                ██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
                ██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██████╔╝███████║██║     █████╗  
                ██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██╔══██╗██╔══██║██║     ██╔══╝  
                ██║     ██║██╔╝ ██╗███████╗███████╗██║   ██║  ██║██║  ██║╚██████╗███████╗
                ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝                                                    

        ''')
    ORIGINAL_IMAGE_PATH=input("Enter Image Path:")
    
    Error_Level_Analysis(ORIGINAL_IMAGE_PATH)