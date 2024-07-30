import tkinter as tk
from tkinter import filedialog, messagebox

from rembg import remove

from PIL import Image, ImageTk, UnidentifiedImageError

import io


def select_input_file():
    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif")]
    )
    if file_path:
        input_path.set(file_path)
        try:
            load_image(file_path, image_label_original)
        except UnidentifiedImageError:
            messagebox.showerror("Error", "Selected file is not a valid image.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


def remove_background():
    if not input_path.get():
        messagebox.showwarning("Warning", "No image selected. Please select an image first.")
        return

    try:
        with open(input_path.get(), 'rb') as i:
            input_file = i.read()
            output_file = remove(input_file)
            global output_image
            output_image = output_file
            load_image(io.BytesIO(output_file), image_label_removed)
    except FileNotFoundError:
        messagebox.showerror("Error", "Input file not found.")
    except UnidentifiedImageError:
        messagebox.showerror("Error", "The file is not a valid image.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the image: {e}")


def save_output_file():
    if not output_image:
        messagebox.showwarning("Warning", "No image to save. Please remove the background first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        title="Save the output file",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
    )
    if file_path:
        try:
            with open(file_path, 'wb') as o:
                o.write(output_image)
            messagebox.showinfo("Success", "Image saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the image: {e}")


def load_image(file, image_label):
    try:
        image = Image.open(file)
        image.thumbnail((350, 350))  # Maintains aspect ratio
        img = ImageTk.PhotoImage(image)
        image_label.config(image=img)
        image_label.image = img
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Selected file is not a valid image.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the image: {e}")


def close_program():
    window.destroy()


window = tk.Tk()
window.title("Background Removal")
window.config(padx=30, pady=30)
window.geometry("1000x700")
window.config(background='#808b96')

input_path = tk.StringVar()
output_image = None

frame = tk.Frame(window, bg='#abb2b9')
frame.pack(pady=25)

button_style = {
    "bg": "#d6eaf8",
    "fg": "#2c3e50",
    "font": ("Arial", 12, "bold"),
    "padx": 20,
    "pady": 10
}

select_button = tk.Button(frame, text="Select Image", command=select_input_file, **button_style)
select_button.grid(row=0, column=0, padx=25, pady=10)

remove_button = tk.Button(frame, text="Remove Background", command=remove_background, **button_style)
remove_button.grid(row=0, column=1, padx=25, pady=10)

save_button = tk.Button(frame, text="Save Image", command=save_output_file, **button_style)
save_button.grid(row=0, column=2, padx=25, pady=10)

image_label_original = tk.Label(window, fg='#abb2b9', bg='#808b96', text="Original Image")
image_label_original.pack(pady=20, side=tk.LEFT, padx=20)

image_label_removed = tk.Label(window, fg='#abb2b9', bg='#808b96', text="Image with Background Removed")
image_label_removed.pack(pady=20, side=tk.RIGHT, padx=20)

exit_button = tk.Button(window, text="Exit", command=close_program, **button_style)
exit_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

window.mainloop()
