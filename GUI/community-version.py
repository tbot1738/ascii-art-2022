# Community Version
import argparse
import pyfiglet

import tkinter.messagebox as ms
from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename

from math import ceil
from random import choice
from time import sleep

from PIL import Image, ImageChops
from rich.console import Console
from rich.terminal_theme import MONOKAI


FILES_IMG_EXTENSION = [
    ("All Images", "*.jpg;*.jpeg;*.png"),
    ("JPEG", "*.jpg"),
    ("JPEG", "*.jpeg"),
    ("PNG", "*.png"),
]

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio/2 * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image):
    return image.convert("L")


def map_pixels_to_ascii_chars(image, range_width, ASCII_CHARS):
    """Maps each pixel to an ascii char based on the range
    in which it lies.
    0-255 is divided into 11 ranges of 25 pixels each.
    """
    # set default ascii character list
    if ASCII_CHARS == None:
        ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [
        ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image
    ]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(
    image,
    range_width,
    new_width=100,
    ASCII_CHARS=None
):
    # set default ascii character list
    if ASCII_CHARS == None:
        ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, range_width, ASCII_CHARS)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in range(0, len_pixels_to_chars, new_width)
    ]

    return "\n".join(image_ascii)


def handle_image_print(image_ascii, color, store):
    verbs = [
        "Articulating",
        "Coordinating",
        "Gathering",
        "Powering up",
        "Clicking on",
        "Backing up",
        "Extrapolating",
        "Authenticating",
        "Recovering",
        "Finalizing",
        "Testing",
        "Upgrading",
    ]

    nouns = [
        "scope",
        "lunch",
        "meetings",
        "skeletons",
        "devices",
        "margins",
        "bookmarks",
        "CPUs",
        "folders",
        "emails",
        "disks",
        "JPEGs",
        "ROMs",
        "Viruses",
    ]

    console = Console()

    # To print beautiful dummy progress bar to the user
    with console.status("[bold green]Turning your image into ASCII art..."):
        for _ in range(4):
            console.log(f"{choice(verbs)} {choice(nouns)}...")
            sleep(1)
        sleep(1)

        # print the ASCII art to the console.
        console.print("[bold green]Here we go...!")
        if color:
            return image_ascii
        else:
            return image_ascii

def write_to_txtfile(txt):
    try:
        with open("output.txt", "w") as text_file:
            text_file.write(txt)
            ms.showinfo("Success","Image converted to ASCII Art ! Check output.txt !")
            root.destroy()
    except:
        return


def inverse_image_color(image):
    inverted_image = ImageChops.invert(image)
    return inverted_image


def handle_image_conversion(image_filepath, range_width, inverse_color, color=None):
    image = None
    try:
        image = Image.open(image_filepath)
        if inverse_color:
            image = inverse_image_color(image)
    except Exception as e:
        ms.showerror("Oops",f"Unable to open image file.")
        root.destroy()
        exit()

    image_ascii = convert_image_to_ascii(image, range_width=range_width, ASCII_CHARS=ASCII_CHARS)
    return image_ascii, color


def init_args_parser():
    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument(
        dest="image_file_path", nargs="?", type=str, help="Image file path."
    )
    parser.add_argument(
        dest="CHAR_SET",
        nargs="?",
        type=str,
        help=(
            "Input 1 or 2 to select pre-defined character sets. "
            "Or, input a list of characters in the format '[a,b,c,d]'."
        ),
    )

    # flag arguments
    parser.add_argument(
        "--inverse", dest="inverse_image", action="store_true", default=False
    )
    parser.add_argument(
        "--color",
        dest="color_ascii",
        type=str,
        help=(
            "Add color to your ascii art by mentioning a color after --color. "
            "For example, --color red produces ascii art of red in color. "
            "It also supports hash code that can help you to choose more colors."
        ),
    )
    parser.add_argument(
        "--store",
        dest="store_art",
        type=str,
        help=(
            "Save the ASCII art of the image to a given path. E.g., --store output.svg. "
            "The result will be great if you choose a svg file extension."
        )
    )

    args = parser.parse_args()

    return args


def store_ascii_art():
    pass


def handle_image(image_file_path):
    global ASCII_CHARS
    args = init_args_parser()
    # The user Specified which CHAR_SET to use or included his/her own
    if args.CHAR_SET:
        # Either an integer value specifying which previously made set to use, or a list value with the characters to use
        CHAR_SET = args.CHAR_SET

        if CHAR_SET[0] == "[" and CHAR_SET[-1] == "]":  # is a list
            CHAR_SET = CHAR_SET[1:-1].split(",")  # Convert the string into a list
            print("Using custom character set:", CHAR_SET)
        else:
            try:
                CHAR_SET = int(CHAR_SET)

            except ValueError:
                raise ValueError(
                    "Please insert a correct value, "
                    "either an int value to select which CHAR_SET to use, "
                    "or a list value of characters of your own!"
                )

    else:  # If the user did not select a CHAR_SET
        CHAR_SET = 1  # Default CHAR_SET

    # Check if the CHAR_SET is a list value
    if isinstance(CHAR_SET, list):
        ASCII_CHARS = CHAR_SET
        # as the range width is based on the number of ASCII_CHARS we have
        range_width = ceil((255 + 1) / len(ASCII_CHARS))

    elif isinstance(CHAR_SET, int):
        if CHAR_SET == 1:  # The original CHAR_SET from the example file
            ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
            range_width = 25

        elif CHAR_SET == 2:
            ASCII_CHARS = [" ", ".", "°", "*", "o", "O", "#", "@"]
            range_width = 32

        else:
            raise Exception("Sorry, there are no CHAR_SET of the value you selected.")
    else:
        raise Exception("The value you chose is neither an integer nor a list.")

    # convert the image to ASCII art
    image_ascii, color = handle_image_conversion(
        image_file_path, range_width, args.inverse_image, args.color_ascii
    )
# display the ASCII art to the console
    capture = handle_image_print(image_ascii, color, args.store_art)

### Save the image ###
    if args.store_art:
        try:
            if args.store_art[-4:] == ".txt":
                with open(args.store_art, "wt") as report_file:
                    console = Console(style=color, file=report_file, record=True)
                    if color:
                        ms.showinfo("Success","Successfully Converted !")
                    else:
                        ms.showinfo("Success","Successfully Converted !")
            else:
                raise ms.showerror("The file extension did not match as txt file!")
        except Exception as e:
            ms.showerror("\33[101mOops, I think you have chosen an incorrect file extension. Hint: Please enter name of SVG. e.g., output.txt \033[0m")
    return capture

def main():
    print(pyfiglet.figlet_format("Welcome to ASCII ART Generator"))
    global entry1
    image_file_path = entry1.get()
    ascii_img = handle_image(image_file_path)
    print(ascii_img)
    write_to_txtfile(ascii_img)

def open_file():
    filepath = askopenfilename(filetypes=FILES_IMG_EXTENSION)

    if not filepath:
        return

    global entry1,label1
    entry1.insert(0, filepath)
    label1["text"]="image is ready to convert"

root=Tk()
root.geometry("800x220")
root.title("Image to ASCII converter")
root.configure(background="black")
root.resizable(0,0)

Label(root, text = "Image to ASCII Convertor",fg="black",font=("Times",25,"bold"),width=25).pack()

btn_open = Button(root, text="Open",fg="black",font=(15), command=open_file)
btn_open.place(x=80,y=60)

label1 = Label(root, text = "Oops, you forgot to specify an Image path: ",fg="black",font=(15))
label1.place(x=140,y=60)

entry1=Entry(root,bd = 5,font = (15),width=70)
entry1.bind(main)
entry1.place(x=80,y=100)

button1= Button(root,text= "Convert",font=("Times",20),width=10,padx=5,pady=5,command=main)
button1.place(x=310,y=150)

root.mainloop()
