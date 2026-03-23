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
    output_image=img.convert("L")
    for x in range(output_image.width):
        for y in range(output_image.height):
            if output_image.getpixel((x,y))< threshold:
                output_image.putpixel( (x,y), 0 )
            else:
                output_image.putpixel( (x,y), 255 )
    return output_image

def exagerateColor(img, threshold, rgb, factor):
    output_image=img.convert("RGB")
    for x in range(output_image.width):
            for y in range(output_image.height):
                pixel = output_image.getpixel((x,y))
                
                if pixel[rgb]< threshold:
                    li = list(pixel) 
                    li[rgb] //= factor
                    pixel = tuple(li)
                    output_image.putpixel( (x,y), pixel )
                if pixel[rgb]> threshold:
                    li = list(pixel) 
                    li[rgb] *= factor
                    pixel = tuple(li)
                    output_image.putpixel( (x,y), pixel)
    return output_image


def randomPixel(img, probability):
    output_image=img.convert("RGB")
    for x in range(output_image.width):
            for y in range(output_image.height):
                
                threshold = random.randint(0, 100)
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                if threshold >= probability:
                    output_image.putpixel( (x,y), (r,g,b))
    return output_image


#img = binarize(img, 100)

img = pixelSortBrightness(100, 100, img)
#img = randomPixel(img, 99)
#img = exagerateColor(img, 50, 2, 10)

#img = pixelSortBrightness(100, 50, img, 1)

img.save("result.jpg")




