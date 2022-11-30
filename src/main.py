from PIL import Image, ImageDraw, ImageFont
import math

filename = input("Please input the filename of your image: ")
image = Image.open("../data/"+filename)
# Allow output size choice
'''sizeC = 0
while sizeC not in (1,2,3):
    try:
        sizeC = int(input("Output size [1: Small, 2: Medium, 3: Large]"))
    except:
        print("Invalid input. Please enter a number [1,2,3]")'''
scaleFac = 0.5
charWidth = 10
charHeight = 18
w,h = image.size
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

outputImage.save("../out/ascii_"+filename)
