import random
import shutil
import os

img_root_path = '/home/data/zgdata/new_zg/devide_data/train/images/'
mask_root_path = '/home/data/zgdata/new_zg/devide_data/train/mask/'

test_img_path = '/home/data/zgdata/new_zg/devide_data/test/images/'
test_mask_path = '/home/data/zgdata/new_zg/devide_data/test/mask/'

test_percent = 0.2     #percent of train_pic

total_img = len(os.listdir(img_root_path))
test_num = int(test_percent * total_img)

'''
   move pic to train_dir
'''
for img_name in random.sample(os.listdir( img_root_path ), test_num):
    if img_name != 'Thumbs.db':
        mask_name = img_name.replace('jpg', 'png')
        shutil.move(os.path.join(img_root_path, img_name), test_img_path)

        # mask_name = img_name.replace('jpg','png')

        shutil.move(os.path.join(mask_root_path, mask_name), test_mask_path)
        print('move succeed')
    else:
        print('img name is not right')


# for class_dir in os.listdir(os.path.join(img_root_path,'train')):
#     test_img_path = os.path.join(img_root_path,'val', class_dir)
#     train_img_dir = os.path.join(img_root_path,'train',class_dir)
#
#     if not os.path.exists(test_img_path):
#         os.makedirs(test_img_path)
#
#     train_percent = 0.1  # percent of train_pic
#
#     total_img = len(os.listdir(train_img_dir))
#     train_num = int(train_percent * total_img)
#
#     for img_name in random.sample(os.listdir(train_img_dir), train_num):
#         if img_name != 'Thumbs.db':
#             shutil.move(os.path.join(train_img_dir, img_name), test_img_path)
#
#             # shutil.move(os.path.join(mask_root_path, mask_name), train_mask_path)
#             print('move succeed')
#         else:
#             print('img name is not right')
#
# for sub in os.listdir(img_root_path):
#     shutil.move(os.path.join(img_root_path, sub), train_img_path)
# for sub in os.listdir(mask_root_path):
#     shutil.move(os.path.join(mask_root_path, sub), train_mask_path)