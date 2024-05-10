import os
import cv2


def resize_images(src_dir, dst_dir, size=(157, 159)):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for subdir, dirs, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(subdir, file)
            dst_path = os.path.join(dst_dir, file)

            if src_path.endswith(".jpg") and not os.path.exists(dst_path):
                image = cv2.imread(src_path)
                resized_image = cv2.resize(image, size)
                cv2.imwrite(dst_path, resized_image)


src_dir = "C:/Users/hlawn/Documents/6 sem project/face recognition/image"
dst_dir = 'C:/Users/hlawn/Documents/6 sem project/face recognition/Resized'
# Create the resized dataset directory if it doesn't exist
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

resize_images(src_dir, dst_dir)
