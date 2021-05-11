import xml.etree.ElementTree as ET
import argparse
import os

count_cb_change = 0
"""
edit xml file to make sure it properly refers to its matching jpg file in folder, name and path
  :arg input
  a string for the input image directory
  :arg edit
  a boolean if editing the files
  :arg unity
  a boolean that checks against file name errors by checking if the jpg and xml file names match, then checking 
  that the xml file name matches.  ***This has been incorporated into the edit argument and phased out***
  :arg verify
  a boolean that verifies how many jpg and xml are in the input directory
  :arg label 
  a boolean that outputs a list of unique labels from the input directory
  """
def edit_xml(input, edit, label, find):
    if edit:
        #collect references
        folder_name = input[input.rfind('\\')+1:len(input)]
        for file in os.listdir(input):
            if not file.endswith(".xml"):
                file_path = os.path.join(input, file)
                file_name = os.path.split(file_path)[1]
                xml_path = os.path.splitext(file_path)[0]+'.xml'
                # change xml file according to jpg folder, name and path
                editor(xml_path, folder_name, file_name, file_path)
        print('Finished editing xml files')
        print(f'Changed {count_cb_change} XML files containing Wc, Sc labels into Cb labels')

    if label:
        print(find_labels(input))

    if find:
        jpg_list = []
        xml_list = []
        for file in os.listdir(input):
            if not file.endswith(".xml"):
                file_path = os.path.join(input, file)
                xml_path = os.path.splitext(file_path)[0] + '.xml'
                if not os.path.isfile(xml_path):
                    jpg_list.append(file)


        for file in os.listdir(input):
            if file.endswith(".xml"):
                file_path = os.path.join(input, file)
                jpg_path = os.path.splitext(file_path)[0] + '.jpg'
                if not os.path.isfile(jpg_path):
                    jpeg_path = os.path.splitext(file_path)[0] + '.jpeg'
                    if not os.path.isfile(jpeg_path):
                        xml_list.append(file)


        print(f'jpg/jpeg files with no xml: {jpg_list}\nxml files with no jpg/jpeg: {xml_list}')


        #if count = 0
        #get list of xml items
        #get their jpg handle
        #if not isfile(), print xml with no jpg file
        #count 1


def editor(xml_path, folder_name, file_name, file_path):
    file_changed = False
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for folder in root.iter('folder'):
        folder.text = folder_name
    for name in root.iter('filename'):
        name.text = file_name
    for path in root.iter('path'):
        path.text = file_path
    # iterate on object<name>
    for object in root.findall('object'):
        # find nested name in root object
        name = str(object.find('name').text)
        # if shelf_cloud || wall_cloud
        if name == 'shelf_cloud' or name == 'wall_cloud':
            global count_cb_change
            # change to cumulonimbus
            object.find('name').text = 'cumulonimbus'
            if file_changed == False:
                count_cb_change += 1
                file_changed = True

    tree.write(xml_path)


def find_labels(dir):
    #initialize array
    label_list = []
    #loop through all .xml files
    for file in os.listdir(dir):
        if file.endswith(".xml"):
            #grab xml root
            xml_path = os.path.join(dir, file)
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for object in root.findall('object'):
                #find nested name in root object
                name = str(object.find('name').text)
                #add to list
                if name not in label_list:
                    label_list.append(name)
    return label_list





#loop and grap all xml then feed into the function
# def LoopThrough(directory_path):
#     slice1 = directory_path.rfind('\\') + 1
#     slice2 = len(directory_path)
#     folder_name = directory_path[slice1:slice2]
#     for filename in os.listdir(directory_path):
#         if filename.endswith(".xml"):
#             global count
#             xml_path = os.path.join(directory_path, filename)
#             count += 1
#             ChangeFolderAndPath(xml_path, folder_name)
#     print(f'Edited {count} files successfully')
#
# def ChangeFolderAndPath(xml_path, folder_name):
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#     for folder in root.iter('folder'):
#         folder.text = folder_name
#
#     for file_name in root.iter('filename'):
#         name = file_name.text
#
#     for path in root.iter('path'): #iterate through XML root 'path'
#         # crawl to slicing locations
#         image_name = name
#         join_name = dir_path['Images_Folder']+folder_name
#         path.text = os.path.join(join_name, image_name)
#
#         #path.text = path.text.replace(path.text[location3:location1], '')
#
#     tree.write(xml_path)
#
#
# def Verify(directory_path):
#     for filename in os.listdir(directory_path):
#         if filename.endswith(".xml"):
#             global count_xml
#             count_xml += 1
#         else:
#             global count_picture
#             count_picture += 1
#     print(f'There are {count_picture} pictures and {count_xml} XML files for a total of {count_picture + count_xml} items')
#
# def DetectAndUnifyXMLAndFileSystemNameDiscrepancy(directory_path):
#     #get list of directory contents
#     contents = os.listdir(directory_path)
#     global count_pair
#     #loop through pictures
#     for ind, name in enumerate(contents):
#         if not name.endswith(".xml"): #grabbed picture
#             name_without_extension = name[0:name.rfind('.')] #picture name for commparison
#             #is matching xml file above or below picture
#             try:
#                 if name_without_extension == contents[ind + 1][0:contents[ind + 1].rfind('.')]: #if filenames == below
#                     count_pair += 1
#                     xml_path = os.path.join(directory_path, contents[ind +1])
#                     CheckOutXMLTree(xml_path, name)
#                 elif name_without_extension == contents[ind - 1][0:contents[ind - 1].rfind('.')]:#if filesnames == above
#                     xml_path = os.path.join(directory_path, contents[ind - 1])
#                     count_pair += 1
#                     print('name matches above')
#                     CheckOutXMLTree(xml_path, name)
#                 else:
#                     print(f'Names don\'t match: {name_without_extension}...{name} and {contents[ind + 1]} ')
#                 CheckMultipleXMLFile(contents, ind)
#             except IndexError:
#                 try:
#                     if name_without_extension == contents[ind - 1][0:contents[ind - 1].rfind('.')]:
#                         count_pair += 1
#                         xml_path = os.path.join(directory_path, contents[ind - 1])
#                         print('name matches above')
#                         CheckOutXMLTree(xml_path, name)
#                 except IndexError:
#                     pass
#     print(f'Total discrepancies found and fixed: {count_error}.  File name pairs found: {count_pair} for a total of '
#           f'{count_pair * 2} files in folder')
#

#
#
# def CheckMultipleXMLFile(contentList, index):
#     if contentList[index + 2].endswith(".xml"):
#         print(f'Found extra xml file named: {contentList[index + 2]}')
#
#
#
#
#     print(label_list)

#edit_xml(path['train_images_folder'], False, False, False)
#path = {'test_images_Folder': 'C:\\Users\\odn08\\Desktop\\output_dir\\test',
        #'train_images_folder': 'C:\\Users\\odn08\\Desktop\\output_dir\\train'}

if __name__ == "__main__":  # once python script is opened in cmd prompt then __name__ variable is issued as well as it becomes __main__
    parser = argparse.ArgumentParser(description='amend xml files to match jpg info, match to input folder location')
    parser.add_argument('-d', '--directory', type=str, metavar='', help='directory location of xml files')
    parser.add_argument('-e', '--edit', action='store_true', help='edit xml for proper folder and path ')
    parser.add_argument('-l', '--label', action='store_true', help='List labels in dataset')
    parser.add_argument('-f', '--find', action='store_true', help='Find jpg with missing xml or xml with missing jpg ')
    args = parser.parse_args()

    edit_xml(args.directory, args.edit, args.label, args.find)

