import base64
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
import os

class Base64ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Base64 ⇄ Image Converter")
        self.root.geometry("800x600")

        # Text area for Base64 input/output
        self.text_area = Text(root, wrap=WORD, height=15)
        self.text_area.pack(fill=BOTH, padx=10, pady=10, expand=True)

        # Button frame
        btn_frame = Frame(root)
        btn_frame.pack(pady=5)

        Button(btn_frame, text="Base64 → Image", command=self.base64_to_image).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Image → Base64", command=self.image_to_base64).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Clear", command=lambda: self.text_area.delete(1.0, END)).grid(row=0, column=2, padx=5)

        # Label for showing preview
        self.preview_label = Label(root)
        self.preview_label.pack(pady=10)

    def base64_to_image(self):
        try:
            b64_string = self.text_area.get(1.0, END).strip()
            if not b64_string:
                messagebox.showwarning("Warning", "Please enter a Base64 string.")
                return

            img_data = base64.b64decode(b64_string)
            image = Image.open(io.BytesIO(img_data))

            # Show preview
            image.thumbnail((300, 300))
            self.tk_image = ImageTk.PhotoImage(image)
            self.preview_label.config(image=self.tk_image)

            # Ask to save
            if messagebox.askyesno("Save Image", "Do you want to save the image?"):
                file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
                if file_path:
                    image.save(file_path)
                    messagebox.showinfo("Saved", f"Image saved at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert Base64 to image.\n\n{e}")

    def image_to_base64(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if not file_path:
                return

            with open(file_path, "rb") as image_file:
                b64_string = base64.b64encode(image_file.read()).decode("utf-8")

            self.text_area.delete(1.0, END)
            self.text_area.insert(END, b64_string)

            # Show preview
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            self.tk_image = ImageTk.PhotoImage(image)
            self.preview_label.config(image=self.tk_image)

            # Optionally save to file
            if messagebox.askyesno("Save Base64", "Do you want to save the Base64 text to a file?"):
                txt_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
                if txt_path:
                    with open(txt_path, "w") as f:
                        f.write(b64_string)
                    messagebox.showinfo("Saved", f"Base64 saved at:\n{txt_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image to Base64.\n\n{e}")

if __name__ == "__main__":
    root = Tk()
    app = Base64ImageConverter(root)
    root.mainloop()
