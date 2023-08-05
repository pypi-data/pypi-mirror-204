import random
from PIL import Image


def convert_to_ascii(args):

    # define characters used
    SET1 = ['/', '!', '=', '+', '|', '#', '%', '@', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '?', '[', ']',
            '{', '}', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    SET2 = ["0", "O", "o", "8", "9", "6", "@", "&", ".", '"', ":"]
    SET3 = ["▀", "▄", "▌", "▐", "■", "◽", "◆", "►", "●", "░", "▒", "▓", "█"]

    # input is set
    BRUSH = int(args.darkness)
    INVERT = bool(args.invert)

    # choose the character set  & shuffle
    if args.set == "1":
        CHAR_SET = SET1
        print("Set one chosen:")
    elif args.set == "2":
        CHAR_SET = SET2
        print("Set two chosen:")
    elif args.set == "3":
        CHAR_SET = SET3
        print("Set three chosen:")
    else:
        print("Invalid character set. Please choose 1, 2, or 3.")
        exit()

    # print the character set
    print(
        " ".join([f"{i+1}. {CHAR_SET[i]}, " for i in range(len(CHAR_SET))])[:-2])

    # shuffle the character set
    if args.random == True:
        random.shuffle(CHAR_SET)
        print("Randomization is on.")
    else:
        print("Randomization is off.")

    if INVERT == True:
        print("Invert is on.")
    else:
        print("Invert is off.")

    # resize image
    with Image.open(args.path) as image:
        image = image.resize((args.width, args.height))

    # convert the image to ASCII art
    ascii_art = ""
    for y in range(args.height):  # for every pixel in the Y value
        for x in range(args.width):  # for every pixel in the X value
            if INVERT == True:  # *if invert argument is true
                pixel = image.getpixel((x, y))  # scan every pixel in image
                gray_value = int(sum(pixel) / 2)  # and turn it into a number
                if gray_value >= BRUSH:  # *if inverted gray value check
                    ascii_char = " "  # replace with white-space
                else:  # if the pixel colour is not black
                    # if the ascii art has reached the end of the pixel line
                    index = int(gray_value / 25)
                    # if the index is longer then the character set repeat character set
                    if index >= len(CHAR_SET):
                        index %= len(CHAR_SET)  # repeat character set
                    # ascii character length is the same as the index length
                    ascii_char = CHAR_SET[index]
                ascii_art += ascii_char  # add character to ascii art line
            else:  # *otherwise do the same but with normal gray check
                pixel = image.getpixel((x, y))
                gray_value = int(sum(pixel) / 2)
                if gray_value <= BRUSH:  # *if normal gray value check
                    ascii_char = " "  # replace with white-space
                else:  # if the pixel colour is not black
                    # if the ascii art has reached the end of the pixel line
                    index = int(gray_value / 25)
                    # if the index is longer then the character set repeat character set
                    if index >= len(CHAR_SET):
                        index %= len(CHAR_SET)  # repeat character set
                    # ascii character length is the same as the index length
                    ascii_char = CHAR_SET[index]
                ascii_art += ascii_char  # add character to ascii art line
        ascii_art += "\n"  # adds a new line at the end of each row

    # generate output file into text
    # add -ascii.txt to imagename
    output_file = args.path.split(".")[0] + "-ascii.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(ascii_art)

    # print to output file
    print(f"ASCII art written to {output_file}")
