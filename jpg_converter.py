from PIL import Image
import os
import argparse
import imghdr

not_jpg = []
actual_file_type = []
convert_record = []
image_tupple = ('.png', '.webp', 'jpeg')

#function iterating through images in folder looking for png or webp or jpeg files
def Loop_through(dir):
    for file in os.listdir(dir):
        if file.endswith(image_tupple):
            file_path = os.path.join(dir, file)
            ConvertImage(file_path)
    print()
    print(f'Operation finished. Converted {len(convert_record)} images.')
    print()
    print(f'Image Convert Record: {convert_record}')


#converts image in file_path to jpg copy at same file path and deletes original image
def ConvertImage(image_path):
    index_period = image_path.rfind('.')
    path_without_extension = image_path[0:index_period]
    img = Image.open(image_path).convert('RGB')
    os.remove(image_path)
    img.save(path_without_extension + '.jpg')
    convert_record.append(image_path[image_path.rfind('\\')+1:index_period])



def check_image(dir):
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if not imghdr.what(file_path) == "jpeg":
            not_jpg.append(file)

    for file in not_jpg:
        if not file.endswith(".xml"):
            file_path = os.path.join(dir, file)
            type = imghdr.what(file_path)
            actual_file_type.append(file)
            actual_file_type.append(type)
            ConvertImage(file_path)

    print()
    print(f'Non jpg list: {not_jpg}')
    print()
    print(f'Number of files not jpg: {len(not_jpg)}')
    print()
    print(f'Files converted to jpg: {actual_file_type}')
#argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Replace image formats with correct jpg type')
    parser.add_argument('-d', '--directory', type=str, metavar='', help='directory location of .jpg files')
    #parser.add_argument('-v', '--verify_images', action='store_true', help='verify jpg image count in dir')
    args = parser.parse_args()

#if args.convert:
    #Loop_through(args.directory)


    check_image(args.directory)

