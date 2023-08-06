import random
import os
from PIL import Image

# define characters used
SET1 = ['/', '!', '=', '+', '|', '#', '%', '@', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '?', '[', ']',
        '{', '}', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
SET2 = ["0", "O", "o", "8", "9", "6", "@", "&", ".", '"', ":"]
SET3 = ["▀", "▄", "▌", "▐", "■", "◽", "◆", "►", "●", "░", "▒", "▓", "█"]


def get_char_set(set_choice):

    # return character set
    if set_choice == "1":
        return SET1
    elif set_choice == "2":
        return SET2
    elif set_choice == "3":
        return SET3
    else:
        print("Error: Invalid character set. Please choose 1, 2, or 3.")
        exit()


def randomize(args):
    CHAR_SET = get_char_set(args.set)
    # if the argument is random shuffle the character set
    if args.random:
        random.shuffle(CHAR_SET)


def get_gray_value(pixel):
    # calculate the grey value of a pixel
    return int(sum(pixel) / 2)


def convert_to_ascii(args):

    # input is set
    BRUSH = int(args.darkness)
    INVERT = bool(args.invert)
    CHAR_SET = get_char_set(args.set)
    FULL_PATH = os.path.abspath(args.path)

    # set the current working directory to the one of the input image
    os.chdir(os.path.dirname(args.path))

    # run other functions
    randomize(args)
    pathcheck(args)

    # resize image
    with Image.open(FULL_PATH) as image:
        image = image.resize((args.width, args.height))

    # *convert the image to ASCII art
    ascii_art = ""
    for y in range(args.height):
        for x in range(args.width):
            pixel = image.getpixel((x, y))
            gray_value = get_gray_value(pixel)
            if INVERT:
                gray_value = 255 - gray_value
            if gray_value >= BRUSH:
                ascii_char = " "
            else:
                index = int(gray_value / 10)
                ascii_char = CHAR_SET[index % len(CHAR_SET)]
            ascii_art += ascii_char
        ascii_art += "\n"

    # generate output file into text
    # add -ascii.txt to imagename
    file_name = args.path.split(".")[0] + "-ascii.txt"
    output_file = os.path.join(FULL_PATH, file_name)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ascii_art)

    # print to output file
    print(f"ASCII art written to {os.path.abspath(output_file)}")


def print_cmd(args):

    CHAR_SET = get_char_set(args.set)
    INVERT = bool(args.invert)

    # print chosen options
    print(f"Set {args.set} chosen.")
    print(
        " ".join([f"{i+1}. {CHAR_SET[i]}, " for i in range(len(CHAR_SET))])[:-2])
    print(f"{'Randomization is on.' if args.random else 'Randomization is off.'}")
    print(f"{'Invert is on.' if INVERT else 'Invert is off.'}")
