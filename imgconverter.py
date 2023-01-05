'''
Image converter (mostly PNG to JPG)
1) Get directory
2) Create default folder
3) Convert all PNG to JPG in directory (create new file)
4) Send converted (new files) to default folder
5) yay, it works?

'''

from pathlib import Path
from PIL import Image
import shutil
import os

# USED, get user input directory
def getUserInput():
    while True:
        try:
            user_input = Path(str(input('Enter dir path: ')))
            user_input.exists()
            return user_input    
        except (FileNotFoundError, NotADirectoryError, OSError):
            print("Please enter a directory...\n")  # doesn't reach
        

# USED, moves img to default folder        
def jpgToFolder(image, dir):
    x = dir.as_posix() + '\\001PNG-JPG'
    p = Path(x)
    shutil.move(str(image), p)
    print(f'transfered {image} to folder {p.name}\n')

# NOT USED, prints directory list.
def dirlist(dir):
    [print(x.name) for x in dir.iterdir() if x.suffix == '.png']

# USED, creates default folder in CWD
def createJPGFolder(dir):
    try:
        x = str(dir) + '\\001PNG-JPG\\'
        p = Path(x)
        p.mkdir()
        print('****CREATED FOLDER****')
    except FileExistsError:
        print('****EXISTING FOLDER****')
    
# USED, converts file to JPG
def convert(dir):
    for x in dir.iterdir():
        if x.suffix == '.png':
            output = Path(dir.as_posix() + '\\' + x.stem + '.jpg')
            if output != x:
                try:
                    with Image.open(x) as im:
                        im.save(output.name)
                        # im.show()
                        print(f"converted {x.name} to JPEG.")
                        jpgToFolder(output, dir)
                except OSError:
                    print('Cannot convert', x.name, '\n')          
                

# if file w/o suffix
def fileToJPG():
    pass

# USED, main loop
while True:
    dir = getUserInput()
    os.chdir(dir.as_posix())
    print(os.getcwd())
    # print("\nDirectory:", dir.name)
    # dirlist(dir)
    createJPGFolder(dir)
    convert(dir)
    pass

