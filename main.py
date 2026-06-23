from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO

current_image = None

def choose_file():
    global current_image
    selected_file = filedialog.askopenfilename(
        title = "Select an image",
        filetypes = (
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
            ("All files", "*.*")
        )
    )
    if selected_file:
        current_image = Image.open(selected_file)
        file_text.config(text=os.path.basename(selected_file))

# def collect_text():
#     global current_image
#
#     url = url_button_entry.get()
#
#     response = requests.get(url)
#     current_image = Image.open(BytesIO(response.content))

def create_watermarked_image():
    width, height = current_image.size

    positions = {
        "Top Left": (20, 20),
        "Top Right": (width - 200, 20),
        "Bottom Left": (20, height - 50),
        "Bottom Right": (width - 200, height - 50),
        "Center": (width // 2, height // 2)
    }

    placement = position.get() or "Center"
    size = int(selected_number.get() or 30)
    watermark_text = watermark_text_entry.get()
    color = color_selected.get() or "white"

    try:
        font_text = ImageFont.truetype("arial.ttf", size)
    except OSError:
        font_text = ImageFont.load_default()

    image = current_image.copy()

    draw = ImageDraw.Draw(image)

    draw.text(
        positions[placement],
        text=watermark_text,
        font=font_text,
        fill=color
    )

    return image

def preview():
    if current_image is None:
        return

    image = create_watermarked_image()
    image.show()

def save_image():

    if current_image is None:
        return

    image = create_watermarked_image()

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG", "*.png"),
            ("JPEG", "*.jpg")
        ]
    )

    if filename:
        image.save(filename)
        messagebox.showinfo(
            title="Success",
            message="Image saved successfully!"
        )

BACKGROUND_COLOR = "#BA5A5A"

root = Tk()
root.title("Image Watermark Adder")
root.geometry("850x450+180+100")
root.configure(bg=BACKGROUND_COLOR)

# Variables
selected_number = StringVar()
color_selected = StringVar()
position = StringVar()

# IMAGE FRAME

image_frame = Frame(root, bg=BACKGROUND_COLOR)
image_frame.pack(fill="x", padx=20, pady=10)

Label(image_frame,
      text="Image",
      font=("Times New Roman", 15, "bold"),
      bg=BACKGROUND_COLOR).grid(row=0, column=0, sticky="w")

# Radiobutton(image_frame,
#             text="Image URL",
#             bg=BACKGROUND_COLOR,
#             value=1,
#             font=("Times New Roman", 15)
#             ).grid(row=1, column=0, sticky="w")

# url_button_entry = Entry(image_frame, width=80)
# url_button_entry.grid(row=1, column=1, ipady=10, padx=10)

Radiobutton(image_frame,
            text="Upload Image",
            bg=BACKGROUND_COLOR,
            value=0,
            font=("Times New Roman", 15)
            ).grid(row=2, column=0, sticky="w")

image_frame.grid_columnconfigure(1, weight=1)
upload_button = Button(image_frame,
                       text="Choose Image",
                       bg=BACKGROUND_COLOR,
                       command=choose_file)
upload_button.grid(row=2, column=1,pady=20, ipady=10, sticky="we")

file_text = Label(image_frame,
                  text="No file chosen",
                  font=("Times New Roman", 15),
                  bg=BACKGROUND_COLOR)
file_text.grid(row=2, column=2, sticky="w")

# WATERMARK FRAME

watermark_frame = Frame(root, bg=BACKGROUND_COLOR)
watermark_frame.pack(fill="x", padx=20, pady=10)

Label(watermark_frame,
      text="Watermark",
      bg=BACKGROUND_COLOR,
      font=("Times New Roman", 15, "bold")
      ).grid(row=0, column=0, sticky="w")

Label(watermark_frame,
      text="Text",
      bg=BACKGROUND_COLOR,
      font=("Times New Roman", 15)
      ).grid(row=1, column=0, pady=10)

watermark_text_entry = Entry(watermark_frame, width=80)
watermark_text_entry.grid(row=1, column=1, columnspan=3, ipady=10)


Label(watermark_frame,
      text="Size",
      bg=BACKGROUND_COLOR,
      font=("Times New Roman", 15)
      ).grid(row=2, column=2)

size_dropdown = OptionMenu(
    watermark_frame,
    selected_number,
    *[str(i) for i in range(20, 70,10)]
)

size_dropdown.config(bg=BACKGROUND_COLOR, width=20)
size_dropdown.grid(row=2, column=3)

Label(watermark_frame,
      text="Color",
      bg=BACKGROUND_COLOR,
      font=("Times New Roman", 15)
      ).grid(row=3, column=0)

color_dropdown = OptionMenu(
    watermark_frame,
    color_selected,
    "White",
    "Black",
    "Red",
    "Green",
    "Blue"
)
color_dropdown.config(bg=BACKGROUND_COLOR, width=20)
color_dropdown.grid(row=3, column=1, pady=10)

Label(watermark_frame,
      text="Position",
      bg=BACKGROUND_COLOR,
      font=("Times New Roman", 15)
      ).grid(row=3, column=2)

position_dropdown = OptionMenu(
    watermark_frame,
    position,
    "Top Right",
    "Top Left",
    "Bottom Left",
    "Bottom Right",
    "Center"
)
position_dropdown.config(bg=BACKGROUND_COLOR, width=20)
position_dropdown.grid(row=3, column=3)

# BUTTON FRAME

button_frame = Frame(root, bg=BACKGROUND_COLOR)
button_frame.pack(fill="x", padx=20, pady=20)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

preview_button = Button(
    button_frame,
    text="Preview",
    bg="#4274D9",
    font=("Times New Roman", 15),
    command=preview
)
preview_button.grid(
    row=0,
    column=0,
    padx=(0, 10),
    ipady=10,
    sticky="we"
)

save_image_button = Button(
    button_frame,
    text="Save Image",
    bg="#659287",
    font=("Times New Roman", 15),
    command=save_image
)
save_image_button.grid(
    row=0,
    column=1,
    padx=(10, 0),
    ipady=10,
    sticky="we"
)

root.mainloop()