# Converts .cbr and .cbz files to .pdf
#
# Use:  python comic2pdf.py
# -- The script should be in the same directory the file(s) to convert are in.
#
# Author:  esacon
# Date:  11-06-21
#
# License:  You can do what you want with it.

from os import rename, mkdir, scandir, getcwd, remove, chmod
from os.path import abspath
from time import sleep
from pyunpack import Archive
from shutil import copy, rmtree
import stat
import img2pdf
import glob


def extractall(filename, outdir, backend='auto', auto_create_dir=False):
    """
    :param backend: auto, patool or zipfile
    :param filename: path to archive file
    :param outdir: directory to extract to
    :param auto_create_dir: auto create directory
    """
    Archive(filename, backend).extractall(outdir, auto_create_dir=auto_create_dir)


def handle_comic(file):
    tmp_dir = getcwd() + "\\temp\\"
    createDir(tmp_dir)
    try:
        extractall(file, outdir=tmp_dir)
        print("File was successfully extracted.")
    except:
        print("Something occurred, please check it out.")
    name = file.replace(file[-4:], ".pdf")
    imgtopdf(filename=name, path=tmp_dir)
    cleanDir(tmp_dir)
    name = repr(file).split(r"\\")[-1]
    print(f'"{name[:-5]}" successfully converted!')


def createDir(path):
    try:
        mkdir(path)
    except FileExistsError:
        print("Folder was already created.")


def imgtopdf(filename, path):
    files = glob.glob(path + '/**/*', recursive=True)
    images = [file for file in files if file.endswith(".jpg") or file.endswith(".JPG")
              or file.endswith(".png") or file.endswith(".PNG")
              or file.endswith(".jpeg") or file.endswith(".JPEG")]
    with open(filename, "wb") as document:
        document.write(img2pdf.convert(images))


def cleanDir(path):
    try:
        chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        rmtree(path, ignore_errors=False)
    except PermissionError:
        print("Run cmd as administrator!")


def opendir(path):
    # look at all files in directory
    files = [abspath(arch.path) for arch in scandir(path) if arch.is_file()]
    comics = [abspath(arch.path) for arch in scandir(path) if arch.is_file()
              and abspath(arch.path).endswith(".cbr") or abspath(arch.path).endswith(".cbz")]
    tam = len(comics)
    i = 1
    for comic in comics:
        print("\n------------------------------------------------------------\n")
        print(f"File {i} of {tam}...")
        name = repr(comic).split(r'\\')[-1]
        print(f"Converting file '{name.replace(name[-5:], '')}' to .pdf ...")
        out = comic.replace(comic[-4:], ".pdf")
        if out not in files:
            if comic[-4:] == '.cbz' or comic[-4:] == '.zip' \
                    or comic[-4:] == '.cbr' or comic[-4:] == '.rar':
                handle_comic(comic)
        else:
            print("Pdf file already exists, it will not be converted.")
        i += 1


opendir(getcwd())
