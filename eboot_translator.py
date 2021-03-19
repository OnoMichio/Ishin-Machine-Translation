import struct
import sys
import pandas as pd


def write_string(data, offset, string):
    pos = offset
    end = data[pos:].index(b'\x00')

    i = 0
    while i < len(data[pos+end:]) and data[pos+end:][i] == 0:
        i += 1

    max_len = end + i - 1

    try:
        byte_string = string.encode("shift-jis").replace(b'\\n', b'\x0A')
        if len(byte_string) > max_len:
            print(f"Text is too long - offset: {offset}, translation: {string}, max length: {max_len}")
        #elif len(byte_string) <= 1:
            #print(f"Broken text - offset: {offset}, translation: {string}, max length: {max_len}")
        else:
            struct.pack_into(f"{max_len}s", data, pos, byte_string)
    except(TypeError):
            print(f"Wrong type - offset: {offset}, translation: {string}, max length: {max_len}")


def replace_strings():
    with open("EBOOT.elf", "rb") as f:
        data = bytearray(f.read())

    #csv file with text
    original_text = 'ishin-eboot-text.csv'
    df = pd.read_csv(original_text, delimiter=';')
    offsets = df.iloc[:, 0]
    strings = df.iloc[:, 1]

    for o, s in zip(offsets, strings):
        write_string(data, int(o, 16), s)
    
    with open("new_EBOOT.elf", "wb") as f:
        f.write(data)


def print_strings():
    with open("EBOOT.elf", "rb") as f:
        data = f.read()

    count = 0
    pos = 0
    while pos < len(data):
        end = data[pos:].index(b'\x00')

        i = 0
        while i < len(data[pos+end:]) and data[pos+end:][i] == 0:
            i += 1

        max_len = end + i

        print(f"str: '{data[pos:pos+end].decode('shift-jis')}', max_len: {max_len}")

        pos += max_len
        count += 1


def main():
    sys.stdout = open('log.txt', 'w')
    replace_strings()


if __name__ == "__main__":
    main()