from pyperclip import copy, paste
from os import linesep as ls

def excel_to_edc():
    inputStr = paste()
    inputStr = inputStr.replace(",", ".")

    result = ""

    for y, line in enumerate(inputStr.split(ls)):
        for x, val in enumerate(line.split("\t")):
            if val == '':
                result = result + '~'
                continue

            result = result + "{}{}:{}:{}:".format('~' if (x > 0 or y > 0) else '2', x, y, val)

    copy(result)