import os
import glob
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def flip_img(imgs_url, new_dir):
    count = 0
    if glob.glob(new_dir):
        pass
    else:
        os.system(f'mkdir {new_dir}')
    for img_url in imgs_url:
        img_obj = Image.open(img_url)
        rotate_img = img_obj.transpose(Image.FLIP_LEFT_RIGHT)
        rotate_img.save(f'{BASE_DIR}/{new_dir}/{count}.jpg')
        count += 1


if __name__ == '__main__':
    imgs = glob.glob('img/*.jpg')
    print(BASE_DIR)
    flip_img(imgs, 'img2')
