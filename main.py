from PIL import Image, ImageDraw, ImageFont
import math
print('''
██╗██████╗  █████╗ 
║ ║╚════██╗██╔══██╗
██║ █████╔╝███████║
██║██╔═══╝ ██╔══██║
██║███████╗██║  ██║
╚═╝╚══════╝╚═╝  ╚═╝
                   
image to ascii v0.1.2
''')
 
while True:
    filename = input("Please input the filename of your image: ")
    try:
        image = Image.open("./data/"+filename)
    except Exception:
        print("File not found. Please ensure your file is present in the data folder")
    else:
        break

try:
    sizeC = int(input("Preferred output quality [1: Small, 2: Medium, 3: Large]: "))
    if sizeC not in (1,2,3, -1):
        raise Exception
except Exception:
    print("Invalid, choosing default size")
    sizeC = 0

charWidth = 10
charHeight = 18
w,h = image.size
if sizeC == 0:
    scaleFac = min(0.5, 360/h)
elif sizeC == -1:
    print("**WARNING**\nOVERRIDE: static 0.8x scale. This may generate an excessively large image.")
    scaleFac = 0.8
else:
    scaleFac = (60+300*(sizeC-1))/h
image = image.resize((int(scaleFac*w),int(scaleFac*h*(charWidth/charHeight))),Image.NEAREST)
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
        draw.text((j*charWidth,i*charHeight),getSomeChar(grey),
        font=font,fill = (r,g,b))

outputImage.save("./out/ascii_"+filename)
