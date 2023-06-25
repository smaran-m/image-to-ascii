print('''
██╗██████╗  █████╗ 
║ ║╚════██╗██╔══██╗
██║ █████╔╝███████║
██║██╔═══╝ ██╔══██║
██║███████╗██║  ██║
╚═╝╚══════╝╚═╝  ╚═╝
                   
image to ascii v0.1.3
by @smaran_
''')
### TODO
# - better image size selection (determinate dimensions)
# - output to text file/html
# - invert color option (white background, dark text)
# - speed up gif processing
#----------
from PIL import Image, ImageDraw, ImageTk, ImageSequence, ImageFont, ImageShow
import os
import math
import platform
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.title('i2A v0.1.3')
root.minsize(300, 250)

filepath = None
image_preview = None
label_kitty = None

filename = tk.StringVar(root)
filename.set("No file selected")

output_quality = tk.StringVar(root)
output_quality.set("Output Quality: Medium")

def select_file():
    global filepath, image_preview, label_ascii_art

    filepath = filedialog.askopenfilename()
    file_name = filepath.split('/')[-1]  # Get filename from the path
    if len(file_name) > 15:  # Limit the length of filename displayed
        file_name = file_name[:12] + '...' 
    filename.set("Selected File: " + file_name)

    # Create a PIL image and resize it
    pil_image = Image.open(filepath)

    # Calculate the aspect ratio
    image_ratio = pil_image.width / pil_image.height

    # Provided space for the image
    max_width = 200
    max_height = 150

    # Calculate the new width and height
    if image_ratio > max_width / max_height:
        # If image width is bigger scale by width
        new_width = max_width
        new_height = int(max_width / image_ratio)
    else:
        # If image height is bigger scale by height
        new_height = max_height
        new_width = int(max_height * image_ratio)

    # Resize the image maintaining the aspect ratio
    pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a Tkinter PhotoImage out of the PIL image
    tk_image = ImageTk.PhotoImage(pil_image)

    # If the image preview already exists, update it
    if image_preview is not None:
        image_preview.config(image=tk_image)
        image_preview.image = tk_image
    # If the image preview doesn't exist, create it
    else:
        image_preview = tk.Label(root, image=tk_image)
        image_preview.image = tk_image
        image_preview.grid(row=3, column=0, columnspan=2)
    
    # If the ASCII art label exists, remove it
    if label_kitty is not None:
        label_kitty.grid_remove()

    return filepath

def toggle_quality():
    if output_quality.get() == "Output Quality: Low":
        output_quality.set("Output Quality: Medium")
    elif output_quality.get() == "Output Quality: Medium":
        output_quality.set("Output Quality: High")
    elif output_quality.get() == "Output Quality: High":
        output_quality.set("Output Quality: Ultra")
    else:
        output_quality.set("Output Quality: Low")

# Open file dialog to select an image file
def generate_image():
    global filepath, font, suppress_warning

    if output_quality.get() == "Output Quality: Ultra":
        if not messagebox.askokcancel("Warning", "Ultra quality images may be of exceedingly large file size, and can take a long time to generate.\nUse at your own risk."):
            return
        
    if filepath is None:  # If no file selected, open file dialog
        filepath = select_file()

    image = Image.open(filepath)

    if not os.path.exists('./out'):
        os.mkdir('./out')

    output_filename = "./out/ascii_" + filename.get().split(': ')[-1]

    if filepath.lower().endswith('.gif'):
        frames = [process_frame(frame) for frame in ImageSequence.Iterator(image)]
        frames[0].save(output_filename, save_all=True, append_images=frames[1:], loop=0)
    else:
        outputImage = process_frame(image)
        outputImage.save(output_filename)

    # Open the output image in the default image viewer

    ImageShow.show(Image.open(output_filename), title='ASCII Art')

def process_frame(image):
    charWidth = 10
    charHeight = 14
    image = image.convert('RGB')
    w,h = image.size
    sizeC = ["Output Quality: Low", "Output Quality: Medium", "Output Quality: High", "Output Quality: Ultra"].index(output_quality.get()) + 1
    if sizeC == 0:
        scaleFac = min(0.5, 260/h)
    else:
        scaleFac = (60+200*(sizeC-1))/h
    image = image.resize((int(scaleFac*w),int(scaleFac*h*(charWidth/charHeight))),Image.Resampling.NEAREST)
    w,h = image.size
    pixels = image.load()

    try:
        font = ImageFont.truetype('lucon.ttf',15)
    except:
        font = ImageFont.truetype('Andale Mono.ttf',15)
    outputImage = Image.new('RGB',(charWidth*w,charHeight*h),color=(0,0,0))
    draw = ImageDraw.Draw(outputImage)

    def getSomeChar(h):
        chars  = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
        charArr = list(chars)
        l = len(charArr)
        mul = l/256
        return charArr[math.floor(h*mul)]

    for i in range(h):
        for j in range(w):
            r,g,b = pixels[j,i]
            grey = int((r/3+g/3+b/3))
            pixels[j,i] = (grey,grey,grey)
            draw.text((j*charWidth,i*charHeight),getSomeChar(grey), font=font, fill = (r,g,b))
    return outputImage


### FONTS
def get_font():
    if platform.system() == 'Windows':
        return 'lucon'
    elif platform.system() == 'Darwin': #MacOS
        return 'Andale Mono' 
    elif platform.system() == 'Linux':
        return 'Andale Mono'
    else:
        return 'Courier New'

# Get the font based on the OS
font_name = get_font()
font_size = 10

### TKINTER
# Create the widgets
label_filename = tk.Label(root, textvariable=filename, font=(font_name, 10))
button_file = tk.Button(root, text="Select File!", command=select_file, font=(font_name, 10))
label_quality = tk.Label(root, textvariable=output_quality, font=(font_name, 10))
button_quality = tk.Button(root, text="Toggle Quality", command=toggle_quality, font=(font_name, 10))
button_generate = tk.Button(root, text="Generate Image", command=generate_image, font=(font_name, 10))
label_credit = tk.Label(root, text="a tool by @smaran_", font=(font_name, 8))

ascii_art = """

  ／\、      
（ﾟ､ ｡ ７   
  l  ~ヽ   
  じしf_,)ノ
"""
label_kitty = tk.Label(root, text=ascii_art, font=(font_name, 20))

# Arrange the widgets
label_filename.grid(row=0, column=0, columnspan=1)
button_file.grid(row=1, column=0, sticky='ew')
label_quality.grid(row=0, column=1, columnspan=1)
button_quality.grid(row=1, column=1, sticky='ew')
button_generate.grid(row=2, column=0, columnspan=2, sticky='ew')
label_kitty.grid(row=3, column=0, columnspan=2)
label_credit.grid(row=4, column=0, columnspan=2)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

