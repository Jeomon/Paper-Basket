from os.path import join,abspath,exists
from application.configuration import root_path
from PIL import Image
from secrets import token_hex
from os import remove


def save_image(path,file,size):
    '''To save the image to the specified folder.'''
    filename=f'{token_hex(20)}.jpg'
    path=abspath(root_path+join(path,filename))
    image=Image.open(file)
    image.thumbnail(size)
    image.save(path)
    return filename

def delete_image(path,file):
    '''To delete the image from the specified folder.'''
    if file not in ['default.png','no-image.png']:
        path=abspath(root_path+join(path,file))
        if exists(path):
            remove(path)