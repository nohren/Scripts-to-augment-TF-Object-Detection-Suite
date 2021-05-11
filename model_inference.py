import tensorflow as tf
from os import path
import os
import imghdr
import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from PIL import Image
import numpy as np
#import matplotlib
#matplotlib.use('QT5Agg', force=True)
import matplotlib.pyplot as plt
#print(f'Switched to: {matplotlib.get_backend()}')

import warnings
import argparse
#warnings.filterwarnings('ignore') #suppress Matplotlib warnings

#enable GPU dynamic memory allocation
def enable_GPU():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)



#download images

#specify file locations
# default_paths = {'MODEL_DIR': 'C:\\Users\\odn08\\TensorFlow\\workspace\\cloud_model_v1_ssd\\exported-models\\Model3\\saved_model',
#                 'LABEL_FILE': 'C:\\Users\\odn08\\TensorFlow\\workspace\\cloud_model_v1_ssd\\annotations\\cloud_label_map.pbtxt',
#                  'TEST_FILE_DIR': 'C:\\Users\\odn08\\Desktop\\test_source\\test',
#                  'SAVE_FILE_PATH': 'C:\\Users\\odn08\\Desktop\\saved_object_detection_files'}

#load model
def load_model(path_to_model_dir):
    print('Loading model...', end='')
    start_time = time.time()
    model = tf.saved_model.load(path_to_model_dir)
    detect_fn = model.signatures['serving_default']  #returns model dictionary into detect_fn
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Done! Took {elapsed_time} seconds')
    return detect_fn, model

def load_labels(path_to_label_file):
    category_index = label_map_util.create_category_index_from_labelmap(path_to_label_file, use_display_name=True)
    return category_index




def load_image_into_numpy_array(path):
    """load an image from file into a numpy array.
    Turns image into numpy array to feed into tensorflow graph.  Note that by convention we put it into a numpy array
    with shape (height, width, rgb channels), where channels =3 red, green, blue

    Args:
        path: the file path to the image

    Returns:
        uint8 numpy array with shape (img_height, img_width, 3) """

    return np.array(Image.open(path))


def image_loader(image_np, detect_fn, category_index, save_path, index):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    print(f'input tensor shape: {input_tensor.shape}')
    detections = detect_fn(input_tensor)  #detect_fn is the model function that takes in an input image tensor
    num_detections = int(detections.pop('num_detections')) #pops 'num detections' out of the dictionary and stores as int value
    detections = {key: value[0, :num_detections].numpy()  #new dictionary, for all key: value pairs in detections.items()
                  for key, value in detections.items()}   #for each key, we index on the corresponding value
                                                          # 0 is accessing first object of first dimension in shape tupple
                                                          #ex. (1, 51500, 9) 0 accesses the 0 idx of 1 value (1x 3d sheet)
                                                          #ex. (51500,9) 0 accesses the 0 idx of 51500 value (1x 51500 row)
                                                          #: slice notation, we want to access the next tupple dimension
                                                          #and take only the range 0 through num_detections
                                                          #example if num_detections = 100
                                                          #(1, 51500, 9) access 1 value at idx 0, grab 1 and only 3d tensor
                                                          #access 51500 rows and slice/extract only rows 0-100
                                                          #.numpy() - make a new numpy array and store as value
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array( #this is where the magic happens: overlays the
        image_np_with_detections,                       #detection_boxes, classes, and scores onto the image
        detections['detection_boxes'],
        detections['detection_classes'],
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.50,
        agnostic_mode=False)

    # plt.figure()
    # plt.imshow(image_np_with_detections)
    print('done')
    #plt.show()
    img = Image.fromarray(image_np_with_detections)
    img.save(os.path.join(save_path, "image" + str(index) + ".jpg"))

def conduct_detection(image_path, model_dir, label_path, save_path):
    #load model
    enable_GPU()
    detect_fn, model = load_model(model_dir)
    category_index = load_labels(label_path)

    #input image(s)
    if path.isfile(image_path):
        print('I see a single image')
        image_np = load_image_into_numpy_array(image_path)
        image_loader(image_np, detect_fn, category_index, save_path, 1)

    elif path.isdir(image_path):
        print('I see a directory')
        count = 0
        for file in os.listdir(image_path):
            file_path = os.path.join(image_path, file)
            if imghdr.what(file_path) == "jpeg" or imghdr.what(file_path) == "png":
                count += 1
                image_np = load_image_into_numpy_array(file_path)
                image_loader(image_np, detect_fn, category_index, save_path, count)


#conduct_detection(default_paths['TEST_FILE_DIR'], default_paths['MODEL_DIR'], default_paths['LABEL_FILE'], default_paths['SAVE_FILE_PATH'])

if __name__ == "__main__":  # once python script is opened in cmd prompt then __name__ variable is issued as well as it becomes __main__
    parser = argparse.ArgumentParser(description='Conduct Inference on trained model')
    parser.add_argument('-i', '--image', type=str,  metavar='', help='file path for test image or directory of images')
    parser.add_argument('-m', '--model_dir', type=str,  metavar='', help='directory location of trained model')
    parser.add_argument('-l', '--label_path', type=str,  metavar='', help='directory location of label_map.pbtxt')
    parser.add_argument('-s', '--save_path', type=str,  metavar='', help='directory location to save object detection files')
    args = parser.parse_args()

    conduct_detection(args.image, args.model_dir, args.label_path, args.save_path)





