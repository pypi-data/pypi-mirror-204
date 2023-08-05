import argparse
from func import convert_to_ascii


def main():
    # cmd arguments
    # define the command line arguments
    parser = argparse.ArgumentParser(
        description="Converts an image to ASCII art.")
    parser.add_argument("path", metavar="path", type=str,
                        help="The path to the image")
    parser.add_argument("--width", type=int, default=62,
                        help="The width of the output")
    parser.add_argument("--height", type=int, default=26,
                        help="The height of the output")
    parser.add_argument("--set", type=str, default="1",
                        help="Character set to use for the ASCII art (1, 2, or 3)",)
    parser.add_argument("--random", type=bool, default=False,
                        help="Character set is scrambled")
    parser.add_argument("--invert", type=bool, default=False,
                        help="Output is inverted")
    parser.add_argument("--darkness", type=int, default=100,
                        help="Darkness of line-art")
    args = parser.parse_args()

    # call the conversion function from ascii.py
    convert_to_ascii(args)


if __name__ == '__main__':
    main()
