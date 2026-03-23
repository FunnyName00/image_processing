from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random


#path = input("Enter the path to the image :\n ")

img = Image.open("image.png")

def pixelSortBrightness(brightness, pixels, img):
    img = img.convert('RGB')
    width, height = img.size
    img_data = img.load()
    for x in range(width):
        y = 0
        while y < height - pixels:
            pixel = img_data[x, y]
            pixel_brightness = sum(pixel) // 3
            # Check if the specific channel meets the threshold
            if pixel_brightness >= brightness:
                # 1. Collect the segment
                segment = []
                for i in range(pixels):
                    segment.append(img.getpixel((x, y + i)))

                # 2. Sort the segment (using the rgb channel as the key)
                segment.sort(key=lambda p: p, reverse=True)

                # 3. Put the pixels back
                for i in range(pixels):
                    img.putpixel((x, y + i), segment[i])
                
                # Jump ahead to the end of the sorted segment
                y += pixels
            else:
                y += 1 
    return img


def chromaticAbberation(brightness, pixels, img, rgb_index):
    channels = list(img.convert('RGB').split())
    
    target_channel = channels[rgb_index]
    width, height = target_channel.size
    
    target_data = target_channel.load()

    for x in range(width):
        y = 0
        while y < height - pixels:
            val = target_data[x, y]

            if val >= brightness:
                segment = []
                for i in range(pixels):
                    segment.append(target_data[x, y + i])

                segment.sort(reverse=True)

                for i in range(pixels):
                    target_data[x, y + i] = segment[i]
                
                y += pixels
            else:
                y += 1 

    channels[rgb_index] = target_channel
    return Image.merge("RGB", channels)


def binarize(img, threshold):
    img = img.convert("L")
    img_data = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if img_data[x,y] < threshold:
                img.putpixel( (x,y), 0 )
            else:
                img.putpixel( (x,y), 255 )
    return img


def exagerateColor(img, threshold, rgb, factor):
    img=img.convert("RGB")
    img_data = img.load()
    for x in range(img.width):
            for y in range(img.height):
                pixel = img_data[x, y]
                
                if pixel[rgb]< threshold:
                    li = list(pixel) 
                    li[rgb] //= factor
                    pixel = tuple(li)
                    img.putpixel( (x,y), pixel )
                if pixel[rgb] > threshold:
                    li = list(pixel) 
                    li[rgb] *= factor
                    pixel = tuple(li)
                    img.putpixel( (x,y), pixel)
    return img


def noiseGenerator(img, probability):
    img=img.convert("RGB")
    for x in range(img.width):
            for y in range(img.height):
                
                threshold = random.randint(0, 100)
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                if threshold <= probability:
                    img.putpixel( (x,y), (r,g,b))
    return img


def edgeDetect(img):
    img = img.convert("L")
    final = img.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8,
                                               -1, -1, -1, -1), 1, 0))
    return final



def textAlongEdge(img: Image, words: list, threshold: int, spacing: int = 15):
    edge = edgeDetect(img)
    edge_data = edge.load()
    width, height = edge.size
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except OSError:
        print("Font not found at that path. Try 'fc-list' in terminal to find your paths.")

    for x in range(0, width, spacing):
        for y in range(0, height, spacing):
            if edge_data[x, y] >= threshold:
                word = random.choice(words)
                draw.text((x, y), word, font=font, fill=(255, 0, 0))
    
    return img

#img = binarize(img, 100)
#img = noiseGenerator(img, 10)
img = chromaticAbberation(150, 50, img, 0)
img = exagerateColor(img, 100, 2, 5)
img = pixelSortBrightness(200, 100, img)
img = textAlongEdge(img, ["Death","Life", "Hate","Joy"], 200)

img = pixelSortBrightness(150, 10, img)

img.save("result.jpg")




