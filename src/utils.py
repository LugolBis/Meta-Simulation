def color_from_letter(letter: str):
    if len(letter) > 1:
        raise ValueError("This should be a single character, dumbass")

    code = ord(letter[0])
    if 31 < code < 256:
        # 224 letters to encode => 8 bits to hide
        # Let's sacrifice 224 shades of (255, 255, n<225) 
        return (255, 255, code-31)
    else:
        raise ValueError("Character is not printable")

def letter_from_color(color: (int, int, int)):
    if color[0] != 255 or color[1] != 255 or color[2] > 224:
        raise ValueError("Not a valid color code for a letter")

    return chr(color[2]+31)