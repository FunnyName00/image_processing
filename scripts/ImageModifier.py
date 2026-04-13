from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random

class ImageModifier:

    @staticmethod 
    def pixelSortBrightness(brightness: int, length: int, img) -> Image:
        """
        Sorts 'length' number of pixel on y after a pixel's average brightness >= 'brightness'

        Args:
            brightness (int) : avg brightness to start pixel sorting
            length (int) : length of sort

        Returns:
            Image : result 
        """
        img = img.convert('RGB')
        width, height = img.size
        img_data = img.load()
        for x in range(width):
            y = 0
            while y < height - length:
                pixel = img_data[x, y]
                pixel_brightness = sum(pixel) // 3
                if pixel_brightness >= brightness:
                    segment = []
                    for i in range(length):
                        segment.append(img.getpixel((x, y + i)))

                    segment.sort(key=lambda p: p, reverse=True)

                    for i in range(length):
                        img.putpixel((x, y + i), segment[i])
                    
                    y += length
                else:
                    y += 1 
        return img

    @staticmethod
    def chromaticAbberation(brightness: int, length: int, rgb_index: int, img: Image) -> Image:
        """
        Sorts 'length' number of pixel on y after a pixel's 'rgb_index' brightness >= 'brightness'

        Args:
            brightness (int) : avg brightness to start pixel sorting
            length (int) : length of sort
            rgb_index (int) : index of the rgb channel affected

        Returns:
            Image : result 
        """
        channels = list(img.convert('RGB').split())
        
        target_channel = channels[rgb_index]
        width, height = target_channel.size
        
        target_data = target_channel.load()

        for x in range(width):
            y = 0
            while y < height - length:
                val = target_data[x, y]

                if val >= brightness:
                    segment = []
                    for i in range(length):
                        segment.append(target_data[x, y + i])

                    segment.sort(reverse=True)

                    for i in range(length):
                        target_data[x, y + i] = segment[i]
                    
                    y += length
                else:
                    y += 1 

        channels[rgb_index] = target_channel
        img = Image.merge("RGB", channels)
        return img 
        

    @staticmethod
    def binarize(threshold: int, img: Image) -> Image:
        """
        Make pixel black where pixel < threshold and white if pixel > threshold

        Args:
            threshold (int) : threshold at which the pixel goes from black to white

        Returns:
            Image : result
        """
        img = img.convert("L")
        img_data = img.load()
        for x in range(img.width):
            for y in range(img.height):
                if img_data[x,y] < threshold:
                    img.putpixel( (x,y), 0 )
                else:
                    img.putpixel( (x,y), 255 )
        return img

    @staticmethod
    def exagerateColor(threshold: int, rgb_index: int, factor: int, img: Image) -> Image:
        """
        If pixel > threshold : channel of rgb_index * factor, else color/factor

        Args:
            threshold (int) : threshold at which color either fades or exagerates
            rgb_index (int) : index of the rgb channel affected
            factor (int) : factor by which the rgb channel is multiplied

        Returns:
            Image : result
        """
        img=img.convert("RGB")
        img_data = img.load()
        for x in range(img.width):
                for y in range(img.height):
                    pixel = img_data[x, y]
                    
                    if pixel[rgb_index]< threshold:
                        li = list(pixel) 
                        li[rgb_index] //= factor
                        pixel = tuple(li)
                        img.putpixel( (x,y), pixel )
                    if pixel[rgb_index] > threshold:
                        li = list(pixel) 
                        li[rgb_index] *= factor
                        pixel = tuple(li)
                        img.putpixel( (x,y), pixel)
        return img

    @staticmethod
    def noiseGenerator(probability: int, img: Image) -> Image:
        """
        Generate noise with probability of probability

        Args:
            probability (int) : probability / 100

        Returns:
            Image : result
        """
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

    @staticmethod
    def edgeDetect(img):
        """
        Returns an image with only the edges of the original image

        Args:

        Returns:
            Image : result
        """
        img = img.convert("L")
        img = img.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8,
                                                -1, -1, -1, -1), 1, 0))
        return img


    @staticmethod
    def textAlongEdge(words: list, threshold: int, spacing: int, img):
        """
        Write random words from words[] at spacing if pixel's avg brightness < threshold on the edge 

        Args:
            words (list) : List of words to be put where
            threshold (int) : threshold at which words are put on the image following the edges
            spacing (int) : Spacing of the words

        Returns:
            Image : result
        """
        edge = ImageModifier.edgeDetect(img)
        edge_data = edge.load()
        img_data = img.load()
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
                    #draw.text((x, y), word, font=font, fill=(img_data[x,y]))
                    draw.text((x, y), word, font=font, fill=((200,0,0)))
        
        return img
    
    @staticmethod
    def crossBrightness(threshold: int, saturation: float, size: int, img: Image):
        """
        Puts cross where brightness > threshold

        Args:
            threshold (int) : threshold at which cross appear
            saturation (float) : value by which pixel's color is multiplied on cross (?)
            size (int) : size of cross (recommend 2 <= size <= 15)
            
        Returns:
            Image : result
        """
        img = img.convert('RGB')
        edge = ImageModifier.edgeDetect(img)
        read_data = edge.load()
        write_data = img.load()
        width, height = img.size

        for x in range(size, width - size):
            for y in range(size, height - size):
                brightness = read_data[x, y]
                
                if brightness >= threshold:
                    new_color = tuple(min(255, int(c * saturation)) for c in write_data[x, y])
                    
                    write_data[x, y] = new_color
                    
                    for i in range(1, size + 1):
                        write_data[x + i, y] = new_color # Right
                        write_data[x - i, y] = new_color # Left
                        write_data[x, y + i] = new_color # Bottom
                        write_data[x, y - i] = new_color # Top

        return img
    