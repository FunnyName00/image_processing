from tkinter import simpledialog
from scripts.ImageModifier import ImageModifier

def get_noise_params():
    val = simpledialog.askinteger("Noise", "Probability (0-100):", initialvalue=5)
    return (ImageModifier.noiseGenerator, (val,), f"Noise ({val}%)") if val is not None else None

def get_pixel_sort_params():
    threshold = simpledialog.askinteger("Pixel Sort", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
    trail = simpledialog.askinteger("Pixel Sort", "Trail Length (0-200):", initialvalue=20, minvalue=0, maxvalue=200)
    return (ImageModifier.pixelSortBrightness, (threshold, trail), f"Pixel Sort ({threshold}, {trail})") if threshold is not None else None

def get_binarize_params():
    threshold = simpledialog.askinteger("Binarize", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
    return (ImageModifier.binarize, (threshold,), f"Binarize ({threshold})") if threshold is not None else None
   
def get_chromatic_params():

    threshold = simpledialog.askinteger("Chromatic Abberation", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
    trail = simpledialog.askinteger("Chromatic Abberation", "Trail Length (0-200):", initialvalue=20, minvalue=0, maxvalue=200)
    rgb_index = simpledialog.askinteger("Chromatic Abberation", "RGB Index (0:Red, 1:Green, 2:Blue):", initialvalue=0, minvalue=0, maxvalue=2)
    return (ImageModifier.chromaticAbberation, (threshold, trail, rgb_index), f"Chromatic Abberation ({threshold}, {trail}, {rgb_index})") if threshold is not None else None

def get_text_edge_params():
    words = simpledialog.askstring("Input", "Words (comma separated):", initialvalue="GLITCH, ERROR, SYSTEM")
    if not words: return None
    
    words_list = [w.strip() for w in words.split(",")]
    threshold = simpledialog.askinteger("Input", "Edge threshold (0-255):", initialvalue=128)
    space = simpledialog.askinteger("Input", "Spacing:", initialvalue=20)
    
    if threshold is not None and space is not None:
        return (ImageModifier.textAlongEdge, (words_list, threshold, space), f"TextEdge ({len(words_list)} words)")
    return None

def get_crosses_params():
    threshold = simpledialog.askinteger("Cross", "Threshold (0-255):", initialvalue=128)
    saturation = simpledialog.askfloat("Cross", "Saturation (1-2):", initialvalue=1.2)
    size = simpledialog.askinteger("Cross", "Size:", initialvalue=5)
    
    if all(v is not None for v in (threshold, saturation, size)):
        return (ImageModifier.crossBrightness, (threshold, saturation, size), f"Crosses ({threshold})")
    return None


def get_color_exagerate_params():
    threshold = simpledialog.askinteger("Color", "Threshold:", initialvalue=128)
    rgb = simpledialog.askinteger("Color", "RGB index (0-2):", initialvalue=0)
    factor = simpledialog.askinteger("Color", "Factor (0-10):", initialvalue=3)
    
    if all(v is not None for v in (threshold, rgb, factor)):
        return (ImageModifier.exagerateColor, (threshold, rgb, factor), f"Color Exagerate ({rgb})")
    return None

# "Noise", "Binarize", "Pixel Sort", "Chromatic", 
# "Edge Detect", "Text along edges", "Crosses along edges", "Exagerate color"

FX_REGISTRY = {
    "Noise": get_noise_params,
    "Pixel Sort": get_pixel_sort_params,
    "Edge Detect": lambda: (ImageModifier.edgeDetect, (), "Edge Detection"),
    "Chromatic" : get_chromatic_params,
    "Binarize" : get_binarize_params,
    "Text along edges" : get_text_edge_params,
    "Crosses along edges" : get_crosses_params,
    "Exagerate color" : get_color_exagerate_params
}


"""
def add_effect_ui(self):
        if not self.processor:
            messagebox.showwarning("Warning", "Load an image first")
            return
        
        effect = self.sidebar.get_selected_effect()
        if not effect: return

        if effect == "Noise":
            val = simpledialog.askinteger("Noise", "Probability (0-100):", initialvalue=5)
            if val is not None:
                self.processor.add(ImageModifier.noiseGenerator, val)
                self.sidebar.insert_effect(f"Noise ({val}%)")

        elif effect == "Binarize":  
            val = simpledialog.askinteger("Binarize", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
            if val is not None:
                self.processor.add(ImageModifier.binarize, val)
                self.sidebar.insert_effect(f"Binarize ({val})")

        elif effect == "Pixel Sort":
            threshold = simpledialog.askinteger("Pixel Sort", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
            trail = simpledialog.askinteger("Pixel Sort", "Trail Length (0-200):", initialvalue=20, minvalue=0, maxvalue=200)

            if threshold != None and trail != None:
                self.processor.add(ImageModifier.pixelSortBrightness, threshold, trail)
                self.sidebar.insert_effect(f"Pixel Sort ({threshold}, {trail})")

        elif effect == "Chromatic":
            threshold = simpledialog.askinteger("Chromatic Abberation", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
            trail = simpledialog.askinteger("Chromatic Abberation", "Trail Length (0-200):", initialvalue=20, minvalue=0, maxvalue=200)
            rgb_index = simpledialog.askinteger("Chromatic Abberation", "RGB Index (0:Red, 1:Green, 2:Blue):", initialvalue=0, minvalue=0, maxvalue=2)
            if threshold != None and trail != None and rgb_index != None:
                self.processor.add(ImageModifier.chromaticAbberation, threshold, trail, rgb_index)
                self.sidebar.insert_effect(f"Chromatic Abberation ({threshold}, {trail}, {rgb_index})")
        
        elif effect == "Edge Detect":
            self.processor.add(ImageModifier.edgeDetect)
            self.sidebar.insert_effect("Edge Detection")


        elif effect == "Text along edges":
            input = simpledialog.askstring("Input", "Enter words separated by commas (e.g. Hate, Life, Joy):"\
                                           , initialvalue="GLITCH, ERROR, SYSTEM")

            if input:
                words_list = [w.strip() for w in input.split(",")]
                threshold = simpledialog.askinteger("Input", "Edge threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
                space = simpledialog.askinteger("Input", "Spacing:", initialvalue=20)

                if threshold is not None and space is not None:
                    self.processor.add(ImageModifier.textAlongEdge, words_list, threshold, space)
                    self.sidebar.insert_effect(f"TextEdge ({len(words_list)} words)")

        elif effect == "Crosses along edges":
            threshold = simpledialog.askinteger("Cross", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
            saturation = simpledialog.askfloat("Cross", "Saturation (1-2):", initialvalue=1.2, minvalue=1, maxvalue=2)
            size = simpledialog.askinteger("Cross", "Size (0-255):", initialvalue=5, minvalue=0, maxvalue=255)
            if threshold is not None and saturation is not None and size is not None:
                self.processor.add(ImageModifier.crossBrightness, threshold, saturation, size)
                self.sidebar.insert_effect(f"Crosses ({threshold}, {saturation}, {size})")

        elif effect == "Exagerate color":
            threshold = simpledialog.askinteger("Color", "Threshold (0-255):", initialvalue=128, minvalue=0, maxvalue=255)
            rgb_index = simpledialog.askinteger("Color", "RGB index (0:Red, 1:Green, 2:Blue):", initialvalue=0, minvalue=0, maxvalue=2)
            factor = simpledialog.askinteger("Color", "Multiply factor(0-10):", initialvalue=3, minvalue=0, maxvalue=10)
            if threshold is not None and rgb_index is not None and factor is not None:

                self.processor.add(ImageModifier.exagerateColor, threshold, rgb_index, factor)
                self.sidebar.insert_effect(f"Color exagerate ({threshold}, {rgb_index}, {factor})")
"""