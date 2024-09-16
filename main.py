### TODO
# - output to text file/html
# - speed up gif processing (buffer?)
# - refactoring
vernum = "0.2.0"

print('''
██╗██████╗  █████╗ 
║ ║╚════██╗██╔══██╗
██║ █████╔╝███████║
██║██╔═══╝ ██╔══██║
██║███████╗██║  ██║
╚═╝╚══════╝╚═╝  ╚═╝''')      
print("image to ascii v"+vernum)
print("by @smaran_")
#----------
from PIL import Image, ImageDraw, ImageTk, ImageSequence, ImageFont, ImageShow
import os
import math
import platform
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.title('i2A '+vernum)
root.minsize(400, 300)  # Increase the minimum size of the window for better button scaling
#root.geometry('500x400')  # Optional: Set a starting size that looks good for the buttons

filepath = None
original_filename = ""
image_preview = None
label_kitty = None

color_button_text = tk.StringVar(root)
color_button_text.set("Color")

filename = tk.StringVar(root)
filename.set("📂: No file selected")

output_quality = tk.StringVar(root)
output_quality.set("Quality: Medium")

charsets = {
    "Simple": " .:-=+*#%@",
    "Detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1],
    "Blocks": "░▒▓█"
}

charset_var = tk.StringVar(root)
charset_var.set("Simple")

charset_preview_var = tk.StringVar(root)
charset_preview_var.set(charsets[charset_var.get()])

def select_file():
    global filepath, image_preview, original_filename, label_kitty

    filepath = filedialog.askopenfilename(initialdir=os.getcwd())
    if not filepath:  # If filepath is not empty
        return None
    
    file_name = filepath.split('/')[-1]  # Get filename from the path
    original_filename = file_name  # Store the original filename
    if len(file_name) > 15:  # Limit the length of filename displayed
        file_name = file_name[:12] + '...' 
    filename.set("📁: " + file_name)

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

def toggle_color():
    global color_button_text
    current_mode = color_button_text.get()
    if current_mode == "Color":
        color_button_text.set("Greyscale")
    elif current_mode == "Greyscale":
        color_button_text.set("Invert")
    else:
        color_button_text.set("Color")

def toggle_quality():
    if output_quality.get() == "Quality: Low":
        output_quality.set("Quality: Medium")
    elif output_quality.get() == "Quality: Medium":
        output_quality.set("Quality: High")
    elif output_quality.get() == "Quality: High":
        output_quality.set("Quality: Ultra")
    else:
        output_quality.set("Quality: Low")

def toggle_charset():
    """ Toggle between different charsets """
    current_charset = charset_var.get()
    if current_charset == "Simple":
        charset_var.set("Detailed")
    elif current_charset == "Detailed":
        charset_var.set("Blocks")
    else:
        charset_var.set("Simple")

    charset_preview_var.set(charsets[charset_var.get()])


# Open file dialog to select an image file
def generate_image():
    global filepath, font

    if output_quality.get() == "Quality: Ultra":
        if not messagebox.askokcancel("Warning", "Ultra quality images may be of exceedingly large file size, and can take a long time to generate.\nUse at your own risk."):
            return
        
    if filepath is None:  # If no file selected, open file dialog
        filepath = select_file()
    image = Image.open(filepath)

    if not os.path.exists('./out'):
        os.mkdir('./out')

    try:
        font = ImageFont.truetype('lucon.ttf',15)
    except:
        font = ImageFont.truetype('Andale Mono.ttf',15)

    output_basename = os.path.splitext(original_filename)[0]  # Get the base name of the original file
    if filepath.lower().endswith('.gif'):
        output_filename = "./out/ascii_" + output_basename + ".gif"
        frames = [process_frame(frame, font) for frame in ImageSequence.Iterator(image)]
        frames[0].save(output_filename, save_all=True, append_images=frames[1:], loop=0)
    else:
        output_filename = "./out/ascii_" + output_basename + ".png"
        outputImage = process_frame(image, font)
        outputImage.save(output_filename)

    # Open the output image in the default image viewer
    ImageShow.show(Image.open(output_filename), title='ASCII Art')


def process_frame(image, font):
    charWidth = 10
    charHeight = 14
    image = image.convert('RGB')
    w,h = image.size
    # Here, instead of "sizeC", use an explicit mapping to the maximum widths.
    max_widths = [1000, 2000, 4000, 8000]
    quality_index = ["Quality: Low", "Quality: Medium", "Quality: High", "Quality: Ultra"].index(output_quality.get())
    max_width = max_widths[quality_index]
    
    # Calculate the scale factor to achieve the desired width, but don't let it go over 1 (to avoid upsizing).
    scaleFac = min(1, max_width / w / charWidth)

    image = image.resize((int(scaleFac*w), int(scaleFac*h*(charWidth/charHeight))), Image.Resampling.NEAREST)
    w, h = image.size
    pixels = image.load()
    
    if color_button_text.get() == "Invert":
        background_color = (255, 255, 255)  # White background
    else:
        background_color = (0, 0, 0)  # Default black background

    outputImage = Image.new('RGB', (charWidth*w, charHeight*h), color=background_color)
    draw = ImageDraw.Draw(outputImage)

    def getSomeChar(h):
        selected_charset = charset_var.get()
        chars = charsets[selected_charset]
        
        # Reverse the charset if we're in Invert mode
        if color_button_text.get() == "Invert":
            chars = chars[::-1]
        
        charArr = list(chars)
        l = len(charArr)
        mul = l / 256
        return charArr[math.floor(h * mul)]


    color = not (color_button_text.get() == "Greyscale")

    for i in range(h):
        for j in range(w):
            r,g,b = pixels[j,i]
            grey = int((r/3+g/3+b/3))
            pixels[j,i] = (grey,grey,grey)
            if (color):
                draw.text((j*charWidth,i*charHeight),getSomeChar(grey), font=font, fill = (r,g,b))
            else:
                draw.text((j*charWidth,i*charHeight),getSomeChar(grey), font=font, fill = (grey, grey, grey))
    return outputImage


### FONTS
def get_font():
    if platform.system() == 'Windows':
        return 'Courier'
    elif platform.system() == 'Darwin': #MacOS
        return 'Andale Mono' 
    else:
        return 'Courier New'

# Get the font based on the OS
font_name = get_font()
font_size = 10

### TKINTER
# Create the widgets
button_file = tk.Button(root, textvariable=filename, command=select_file, font=(font_name, font_size))
button_quality = tk.Button(root, textvariable=output_quality, command=toggle_quality, font=(font_name, font_size))
label_credit = tk.Label(root, text="a tool by @smaran_", font=(font_name, int(font_size * 0.8)))
label_charset_preview = tk.Label(root, textvariable=charset_preview_var, font=(font_name, int(font_size * 0.8)))
button_color = tk.Button(root, textvariable=color_button_text, command=toggle_color, font=(font_name, font_size))
button_generate = tk.Button(root, text="Generate Image", command=generate_image, font=(font_name, int(font_size * 1.2)))
button_charset = tk.Button(root, text="Charset: Simple", command=lambda: [toggle_charset(), button_charset.config(text=f"Charset: {charset_var.get()}")], font=(font_name, 10))


ascii_art = """
  ／\、      
（ﾟ､ ｡ ７   
  l  ~ヽ   
  じしf_,)ノ
"""
label_kitty = tk.Label(root, text=ascii_art, font=(font_name, 20))

# Arrange the widgets
button_file.grid(row=1, column=0, sticky='ew')
button_quality.grid(row=1, column=1, sticky='ew')
button_color.grid(row=2, column=1, sticky='ew')
button_charset.grid(row=2, column=0, sticky='ew')
# row 3 for image preview
label_charset_preview.grid(row=5, column=0, columnspan=2)
label_kitty.grid(row=4, column=0, columnspan=2)
label_credit.grid(row=6, column=0, columnspan=2)
button_generate.grid(row=7, column=0, columnspan=2, sticky='nsew')

for i in range(7):  # Assume you have 6 rows
    root.grid_rowconfigure(i, weight=1)
for i in range(2):  # Assume you have 2 columns
    root.grid_columnconfigure(i, weight=1)

root.grid_rowconfigure(5, weight=2)  # 10 is arbitrarily chosen; any large number would work

root.mainloop()

