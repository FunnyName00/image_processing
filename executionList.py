from ImageModifier import *
from PIL import Image


class ActionList:
    def __init__(self, image: Image.Image) -> None:
        """
        Creates a new pipeline specific to an image
        
        Args:
            image (Image.Image) : Image to be processed with the pipeline 
        Returns:
            None
        
        """
        self.image = image
        self.pipeline = []

    def add(self, modifier_func: function, *args) -> None:
        """
        Add a new modifier at the end of the pipeline
        
        Args:
            modifier_func (function) : modifier to be added to the pipline
            args (multiples) : different arguments for the modifier
            
        Returns:
            None
        
        """
        self.pipeline.append((modifier_func, args))
    

    def delete(self, index:int) -> None:
        """
        Delete an element of the pipeline
        
        Args:
            index (int) : index of the element to be deleted
            
        Returns:
            None
        
        """
        self.pipeline.pop(index)
    
    def swapPlace(self, indexFirst:int, indexSecond:int) -> None:
        """
        Swap places between 2 elementsin the pipeline
        
        Args:
            indexFirst (int) : index of first element to be swaped
            indexSecond (int) : index of second element to be swaped
        Returns:
            None
        
        """
        temp = self.pipeline[indexFirst]
        
        self.pipeline[indexFirst] = self.pipeline[indexSecond]
        self.pipeline[indexSecond] = temp

    def execute(self, filename: str) -> None:
        """
        Execute the pipeline in order and save the result

        Args:
            filename (str) : name of the final result file
        Returns:
            None

        """
        current_img = self.image
        
        for index, (func, args) in enumerate(self.pipeline):
           
            current_img = func(*args, current_img)
            #current_img.save(f"step_{index}.png")
        
        self.image = current_img
        self.image.save(filename)

    def __repr__(self) -> str:
        """
        prints the pipeline 
        
        Args:
        
        Returns:
            The string to be printed
        
        """
        string = f''
        for index, (func, args) in enumerate(self.pipeline):
            string += f'Func :  {func}, Args : , {args} \n'
        
        return string

## Utilisation Example 

img = Image.open("Sil80.jpg")
processor = ActionList(img)

processor.add(ImageModifier.noiseGenerator, 2)
processor.add(ImageModifier.binarize, 150)
processor.add(ImageModifier.chromaticAbberation, 100, 25, 0) 
processor.add(ImageModifier.exagerateColor, 150, 0, 2)
processor.add(ImageModifier.pixelSortBrightness, 100, 15)   
processor.add(ImageModifier.textAlongEdge, ["Hate", "Life", "Joy"], 100, 20) 
processor.add(ImageModifier.pixelSortBrightness, 200, 12)  
processor.add(ImageModifier.crossBrightness, 250, 1.3, 2) 

# print(processor)
# print("--------")

# processor.swapPlace(0, 1)

# print(processor)
# print("--------")
# processor.delete(0)

# print(processor)

processor.execute("final_result.png")
