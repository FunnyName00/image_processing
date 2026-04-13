import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog, ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from scripts.executionList import *
from scripts.ImageModifier import *
from fxRegister import *
import threading
        
class EffectSidebar(tk.Frame):
    def __init__(self, parent, on_add, on_remove, on_up, on_reset):
        super().__init__(parent, width=220, bg="#2e2e2e")
        self.pack(side="left", fill="y", padx=5, pady=5)
        

        self.on_add = on_add
        self.on_remove = on_remove
        self.on_up = on_up
        self.on_reset = on_reset

        self._setup_widgets()

    def _setup_widgets(self):
        tk.Label(self, text="FX PIPELINE", bg="#2e2e2e", fg="white", 
                 font=('Arial', 10, 'bold')).pack(pady=5)

        self.listbox = tk.Listbox(self, height=15, bg="#1e1e1e", fg="white", 
                                  selectbackground="#4a4a4a")
        self.listbox.pack(fill="x", padx=10, pady=5)

        btn_frame = tk.Frame(self, bg="#2e2e2e")
        btn_frame.pack(fill="x", padx=10)
        
        tk.Button(btn_frame, text="↑ Up", command=self.on_up).pack(side="left", expand=True)
        tk.Button(btn_frame, text="Remove", command=self.on_remove).pack(side="left", expand=True)
        tk.Button(btn_frame, text="Reset", command=self.on_reset).pack(side="left", expand=True)

        tk.Label(self, text="Add Effect:", bg="#2e2e2e", fg="#aaaaaa").pack(pady=(15, 0))
        self.effect_var = tk.StringVar()
        self.effect_menu = ttk.Combobox(self, textvariable=self.effect_var, state="readonly")
        self.effect_menu['values'] = (
            "Noise", "Binarize", "Pixel Sort", "Chromatic", 
            "Edge Detect", "Text along edges", "Crosses along edges", "Exagerate color"
        )
        self.effect_menu.pack(fill="x", padx=10, pady=5)
        
        tk.Button(self, text="Add to List", command=self.on_add).pack(fill="x", padx=10, pady=5)

    def get_selected_effect(self):
        return self.effect_var.get()

    def get_selected_index(self):
        selection = self.listbox.curselection()
        return selection[0] if selection else None

    def insert_effect(self, text, index=tk.END):
        self.listbox.insert(index, text)

    def remove_effect(self, index):
        self.listbox.delete(index)

    def clear(self):
        self.listbox.delete(0, tk.END)


class GlitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FunnyName's glitch art engine")
        
        self.original_img = None
        self.processor = None
        self.display_img = None

        # Main Layout
        self.sidebar = EffectSidebar(
            self.root, 
            on_add=self.add_effect_ui, 
            on_remove=self.remove_effect, 
            on_up=self.move_up, 
            on_reset=self.reset_pipeline
        )
        
        self.main_area = tk.Frame(self.root)
        self.main_area.pack(side="right", expand=True, fill="both")
        
        self._setup_main_canvas()

    def _setup_main_canvas(self):
        self.btn_load = tk.Button(self.main_area, text="1. Load Image", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.canvas = tk.Canvas(self.main_area, width=600, height=400, bg="gray")
        self.canvas.pack(padx=10, pady=5)

        self.btn_run = tk.Button(self.main_area, text="2. RUN PIPELINE", command=self.process_image, 
                                 bg="#007acc", fg="white", font=('Arial', 12, 'bold'), height=2)
        self.btn_run.pack(fill="x", padx=10, pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.original_img = Image.open(path)
            
            self.processor = ActionList(self.original_img)
            self.sidebar.clear()
            self.update_canvas(self.original_img)


    def add_effect_ui(self):
        if not self.processor:
            messagebox.showwarning("Warning", "Load an image first")
            return
        
        effect_name = self.sidebar.get_selected_effect()
        
        if effect_name in FX_REGISTRY:
            
            result = FX_REGISTRY[effect_name]() 
            
            if result:
                func, args, display_text = result
                
                self.processor.add(func, *args)

                self.sidebar.insert_effect(display_text)

    def remove_effect(self):
        idx = self.sidebar.get_selected_index()
        if idx is not None:
            self.processor.delete(idx)
            self.sidebar.remove_effect(idx)

    def move_up(self):
        idx = self.sidebar.get_selected_index()
        if idx is not None and idx > 0:
            self.processor.swapPlace(idx, idx - 1)
            text = self.sidebar.listbox.get(idx)
            self.sidebar.remove_effect(idx)
            self.sidebar.insert_effect(text, idx - 1)
            self.sidebar.listbox.select_set(idx - 1)

    def reset_pipeline(self):
        if self.original_img:
            self.processor = ActionList(self.original_img)
            self.sidebar.clear()
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