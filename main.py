import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog, ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from scripts.executionList import *
from scripts.ImageModifier import *
import threading
        

class GlitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FunnyName's glitch art engine")
        
        self.original_img = None
        self.processor = None
        self.display_img = None

        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, width=220, bg="#2e2e2e")
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        tk.Label(self.sidebar, text="FX PIPELINE", bg="#2e2e2e", fg="white", font=('Arial', 10, 'bold')).pack(pady=5)

        # Pipeline Display
        self.listbox = tk.Listbox(self.sidebar, height=15, bg="#1e1e1e", fg="white", selectbackground="#4a4a4a")
        self.listbox.pack(fill="x", padx=10, pady=5)

        # Control Buttons
        btn_frame = tk.Frame(self.sidebar, bg="#2e2e2e")
        btn_frame.pack(fill="x", padx=10)
        
        tk.Button(btn_frame, text="↑ Up", command=self.move_up).pack(side="left", expand=True)
        tk.Button(btn_frame, text="Remove", command=self.remove_effect).pack(side="left", expand=True)
        tk.Button(btn_frame, text="Reset", command=self.reset_pipeline).pack(side="left", expand=True)

        # Fx selection
        tk.Label(self.sidebar, text="Add Effect:", bg="#2e2e2e", fg="#aaaaaa").pack(pady=(15, 0))
        self.effect_var = tk.StringVar()
        self.effect_menu = ttk.Combobox(self.sidebar, textvariable=self.effect_var, state="readonly")
        self.effect_menu['values'] = ("Noise", "Binarize", "Pixel Sort", "Chromatic", "Edge Detect", "Text along edges", "Crosses along edges")
        self.effect_menu.pack(fill="x", padx=10, pady=5)
        
        tk.Button(self.sidebar, text="Add to List", command=self.add_effect_ui).pack(fill="x", padx=10, pady=5)

        # Main Area
        self.main_area = tk.Frame(self.root)
        self.main_area.pack(side="right", expand=True, fill="both")

        self.btn_load = tk.Button(self.main_area, text="1. Load Image", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.canvas = tk.Canvas(self.main_area, width=600, height=400, bg="gray")
        self.canvas.pack(padx=10, pady=5)

        self.btn_run = tk.Button(self.main_area, text="2. RUN PIPELINE", command=self.process_image, 
                                 bg="#007acc", fg="white", font=('Arial', 12, 'bold'), height=2)
        self.btn_run.pack(fill="x", padx=10, pady=10)

    # --- Logic Methods ---

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.original_img = Image.open(path)
            
            self.processor = ActionList(self.original_img)
            self.listbox.delete(0, tk.END) 
            self.update_canvas(self.original_img)

    def add_effect_ui(self):
        if not self.processor:
            messagebox.showwarning("Warning", "Load an image first")
            return
        
        effect = self.effect_var.get()
        if not effect: return

        # Fx setup
        if effect == "Noise":
            val = simpledialog.askinteger("Noise", "Probability (0-100):", initialvalue=5)
            if val is not None:
                self.processor.add(ImageModifier.noiseGenerator, val)
                self.listbox.insert(tk.END, f"Noise ({val}%)")

        elif effect == "Binarize":  
            val = simpledialog.askinteger("Binarize", "Threshold (0-255):", initialvalue=128)
            if val is not None:
                self.processor.add(ImageModifier.binarize, val)
                self.listbox.insert(tk.END, f"Binarize ({val})")

        elif effect == "Pixel Sort":
            threshold = simpledialog.askinteger("Pixel Sort", "Threshold (0-255):", initialvalue=128)
            trail = simpledialog.askinteger("Pixel Sort", "Trail Length (0-200):", initialvalue=20)

            if threshold != None and trail != None:
                self.processor.add(ImageModifier.pixelSortBrightness, threshold, trail)
                self.listbox.insert(tk.END, f"Pixel Sort ({threshold}, {trail})")

        elif effect == "Chromatic":
            threshold = simpledialog.askinteger("Chromatic Abberation", "Threshold (0-255):", initialvalue=128)
            trail = simpledialog.askinteger("Chromatic Abberation", "Trail Length (0-200):", initialvalue=20)
            rgb_index = simpledialog.askinteger("Chromatic Abberation", "RGB Index (0:Red, 1:Green, 2:Blue):", initialvalue=0)
            if threshold != None and trail != None and rgb_index != None:
                self.processor.add(ImageModifier.chromaticAbberation, threshold, trail, rgb_index)
                self.listbox.insert(tk.END, f"Chromatic Abberation ({threshold}, {trail}, {rgb_index})")

        elif effect == "Edge Detect":
            self.processor.add(ImageModifier.edgeDetect)
            self.listbox.insert(tk.END, "Edge Detection")

        elif effect == "Text along edges":
            input = simpledialog.askstring("Input", "Enter words separated by commas (e.g. Hate, Life, Joy):", initialvalue="GLITCH, ERROR, SYSTEM")

            if input:
                words_list = [w.strip() for w in input.split(",")]
                threshold = simpledialog.askinteger("Input", "Edge threshold (0-255):", initialvalue=128)
                space = simpledialog.askinteger("Input", "Spacing:", initialvalue=20)

                if threshold is not None and space is not None:
                    self.processor.add(ImageModifier.textAlongEdge, words_list, threshold, space)
                    self.listbox.insert(tk.END, f"TextEdge ({len(words_list)} words)")

        elif effect == "Crosses along edges":
            threshold = simpledialog.askinteger("Cross", "Threshold (0-255):", initialvalue=128)
            saturation = simpledialog.askfloat("Cross", "Saturation (0-1):", initialvalue=0.2)
            size = simpledialog.askinteger("Cross", "Size (0-255):", initialvalue=1)
            if threshold is not None and saturation is not None and size is not None:
                self.processor.add(ImageModifier.crossBrightness, threshold, saturation, size)
                self.listbox.insert(tk.END, f"Crosses ({threshold}, {saturation}, {size})")

    def remove_effect(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            self.processor.delete(idx)
            self.listbox.delete(idx)

    def move_up(self):
        selection = self.listbox.curselection()
        if selection and selection[0] > 0:
            idx = selection[0]
            self.processor.swapPlace(idx, idx - 1)
            
            # Update Listbox UI
            text = self.listbox.get(idx)
            self.listbox.delete(idx)
            self.listbox.insert(idx - 1, text)
            self.listbox.select_set(idx - 1)

    def reset_pipeline(self):
        if self.original_img:
            self.processor = ActionList(self.original_img)
            self.listbox.delete(0, tk.END)
            self.update_canvas(self.original_img)

    def process_image(self):
        if not self.processor or not self.original_img:
            return
        
        self.btn_run.config(state="disabled", text="Processing...")
        
        
        thread = threading.Thread(target=self.run_task)
        thread.start()

    def run_task(self):
        
        result = self.processor.execute("img/final_result.png")
        
        self.root.after(0, self.finalize_render, result)

    def finalize_render(self, result):
        self.update_canvas(result)
        self.btn_run.config(state="normal", text="2. RUN PIPELINE")

    def update_canvas(self, pil_img):
      
        display_copy = pil_img.copy()
        display_copy.thumbnail((600, 400))
        self.display_img = ImageTk.PhotoImage(display_copy)
        self.canvas.delete("all")
        self.canvas.create_image(300, 200, image=self.display_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = GlitchApp(root)
    root.mainloop()