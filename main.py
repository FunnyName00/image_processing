from PIL import Image
import random


#path = input("Enter the path to the image :\n ")

img = Image.open("Sil80.jpg")

def pixelSortBrightness(brightness, pixels, img):
    img = img.convert('RGB')
    width, height = img.size

    for x in range(width):
        y = 0
        while y < height - pixels:
            pixel = img.getpixel((x, y))
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


def chomaticAbberation(brightness, pixels, img, rgb_index):
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
    img=img.convert("L")
    for x in range(img.width):
        for y in range(img.height):
            if img.getpixel((x,y))< threshold:
                img.putpixel( (x,y), 0 )
            else:
                img.putpixel( (x,y), 255 )
    return img


def exagerateColor(img, threshold, rgb, factor):
    img=img.convert("RGB")
    for x in range(img.width):
            for y in range(img.height):
                pixel = img.getpixel((x,y))
                
                if pixel[rgb]< threshold:
                    li = list(pixel) 
                    li[rgb] //= factor
                    pixel = tuple(li)
                    img.putpixel( (x,y), pixel )
                if pixel[rgb]> threshold:
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


img = chomaticAbberation(150, 50, img, 1)
img = exagerateColor(img, 100, 2, 5)
img = pixelSortBrightness(200, 100, img)
#img = binarize(img, 100)
#img = noiseGenerator(img, 20)

#img = pixelSortBrightness(100, 50, img, 1)

img.save("result.jpg")




