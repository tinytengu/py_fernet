import sys
import os
from pathlib import Path
from cryptography.fernet import Fernet


def get_home():
    return Path.home()


def init_dir():
    home = get_home()
    tdc = home.joinpath('.frnt')

    if not tdc.is_dir():
        tdc.mkdir()

    return tdc


def generate_key():
    return Fernet.generate_key()


def write_key(filename, key):
    with open(filename, 'wb') as file:
        file.write(key)


def read_key(filename):
    with open(filename, 'rb') as file:
        key = file.read()
    return key


def main(args):
    tdc = init_dir()
    tdc_key = tdc.joinpath('key.frnt')

    if not args:
        print('Usage:\ngenkey - Generate new key\nsetkey [key] - Set new key\ngetkey - Get current key\nresetkey - Reset current key\nencrypt [filename] - Encrypt file with current key\ndecrypt [filename] - Decrypt file with current key')
        return

    if args[0] == 'genkey':
        print('Generated key:', generate_key().decode())
        return

    if args[0] == 'setkey':
        if len(args) != 2:
            print('Usage:\nsetkey [key]')
            return

        write_key(tdc_key, args[1].encode())
        return

    if args[0] == 'getkey':
        if not tdc_key.is_file():
            print('* Key is not set yet')
            return

        key = read_key(tdc_key)
        print('Current key:', key.decode())
        return

    if args[0] == 'resetkey':
        if tdc_key.is_file():
            os.remove(tdc_key)
        print('The key was successfully reset')
        return

    if args[0] == 'encrypt':
        if len(args) != 2:
            print('Usage:\necnrypt [filename]')
            return

        fname = Path(args[1])
        if not fname.is_file():
            print('* Invalid filename')
            return

        if not tdc_key.is_file():
            print('* Key is not set yet')
            return

        fernet = Fernet(read_key(tdc_key))

        with open(fname, 'rb') as file:
            content = file.read()

        with open(str(fname) + '.frnt', 'wb') as file:
            file.write(fernet.encrypt(content))

        print(f'File {fname} has been encrypted (Output: {fname}.frnt)')
        return

    if args[0] == 'decrypt':
        if len(args) != 2:
            print('Usage:\ndecrypt [filename]')
            return

        fname = Path(args[1])
        if not fname.is_file():
            print('* Invalid filename')
            return

        if not tdc_key.is_file():
            print('* Key is not set yet')
            return

        fernet = Fernet(read_key(tdc_key))

        with open(fname, 'rb') as file:
            content = file.read()

        newname = str(fname).split('.')
        newname = '.'.join(newname[:-1])

        with open(newname, 'wb') as file:
            file.write(fernet.decrypt(content))

        print(f'File {fname} has been decrypted (Output: {newname})')
        return

    print('* Invalid command')


if __name__ == '__main__':
    main(sys.argv[1:])
