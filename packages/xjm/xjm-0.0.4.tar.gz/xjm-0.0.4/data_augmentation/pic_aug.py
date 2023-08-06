import os

from PIL import Image

image_root_path = '/home/xjm/xjm/xjm_pycharm/swin_transformer/datasets/3_data/train/2/'
mask_root_path = '/home/data/zgdata/mask_img/mask/'

image_save_path = '/home/xjm/xjm/xjm_pycharm/swin_transformer/datasets/3_data/train_aug/2/'
mask_save_path = '/home/data/zgdata/mask_img/aug_data/mask/'

i = 0
for img_name in os.listdir(image_root_path):
    # mask_name = img_name.replace('jpg', 'png')

    if img_name != 'Thumbs.db':

        img = Image.open(os.path.join(image_root_path,img_name))
        # mask = Image.open(os.path.join(mask_root_path,mask_name))

        img.save(image_save_path + 'original_' + img_name)
        # mask.save(mask_save_path + 'original_' + f'{i:012d}.png')


        '''
        上下翻转
        '''
        img_flip_TB = img.transpose(Image.FLIP_TOP_BOTTOM)
        # mask_flip_TB = mask.transpose(Image.FLIP_TOP_BOTTOM)

        img_flip_TB.save(image_save_path + 'FLIP_T_B_' + img_name)
        # img_flip_TB.save(mask_save_path + 'FLIP_T_B_' + f'{i:012d}.png')

        '''
        左右翻转
        '''
        img_flip_lr = img.transpose(Image.FLIP_LEFT_RIGHT)
        # mask_flip_lr = mask.transpose(Image.FLIP_LEFT_RIGHT)

        img_flip_lr.save(image_save_path + 'FLIP_L_R_' + img_name)
        # mask_flip_lr.save(mask_save_path + 'FLIP_L_R_' + f'{i:012d}.png')

        '''
        旋转30度
        '''
        img_rotate_30 = img.rotate(30)
        # mask_rotate_30 = mask.rotate(30)

        img_rotate_30.save(image_save_path + 'Rotate_30_' + img_name)
        # mask_rotate_30.save(mask_save_path + 'Rotate_30_' + f'{i:012d}.png')

        '''
        旋转60度
        '''
        img_rotate_60 = img.rotate(60)
        # mask_rotate_60 = mask.rotate(60)

        img_rotate_60.save(image_save_path + 'Rotate_60_' + img_name)
        # mask_rotate_60.save(mask_save_path + 'Rotate_60_' + f'{i:012d}.png')

        '''
        旋转120度
        '''
        img_rotate_120 = img.rotate(120)
        # mask_rotate_120 = mask.rotate(120)

        img_rotate_120.save(image_save_path + 'Rotate_120_' + img_name)
        # mask_rotate_120.save(mask_save_path + 'Rotate_120_' + f'{i:012d}.png')

        '''
        旋转150度
        '''
        img_rotate_150 = img.rotate(150)
        # mask_rotate_150 = mask.rotate(150)

        img_rotate_150.save(image_save_path + 'Rotate_150_' + img_name)
        # mask_rotate_150.save(mask_save_path + 'Rotate_150_' + f'{i:012d}.png')

        i += 1