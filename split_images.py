import os
from PIL import Image


# Class for the crop image
class CropImage:
    # Init method
    def __init__(self, father, crop, mode):
        self.father = father
        self.crop = crop
        self.image_cropped = None
        self.resize_factor = 1
        # Search attributes for the crop
        self.width = crop[2] - crop[0]
        self.height = crop[3] - crop[1]
        self.father_path = father.image_path
        self.mode = mode
        self.objects_positions = []
        self.objects_names = []
        # Search which bbox is in the crop
        for f_o in range(father.num_objects):
            to_analyse = father.objects_positions[f_o].copy()
            object_out = False
            # Delimit the objects inside the crop
            if to_analyse[0] < self.crop[0]:
                to_analyse[0] = self.crop[0]
            elif to_analyse[0] > self.crop[0]:
                if to_analyse[0] > self.crop[2]:
                    object_out = True
            if to_analyse[1] < self.crop[1]:
                to_analyse[1] = self.crop[1]
            elif to_analyse[1] > self.crop[1]:
                if to_analyse[1] > self.crop[3]:
                    object_out = True
            if to_analyse[2] > self.crop[2]:
                to_analyse[2] = self.crop[2]
            elif to_analyse[2] < self.crop[2]:
                if to_analyse[2] < self.crop[0]:
                    object_out = True
            if to_analyse[3] > self.crop[3]:
                to_analyse[3] = self.crop[3]
            elif to_analyse[3] < self.crop[3]:
                if to_analyse[3] < self.crop[1]:
                    object_out = True
            # Add the object if is inside, and have more than 0.5 of the area
            if not object_out:
                percentage_within = ((to_analyse[2] - to_analyse[0]) * (to_analyse[3] - to_analyse[1])) / \
                                    (((father.objects_positions[f_o][2] - father.objects_positions[f_o][0]) *
                                      (father.objects_positions[f_o][3] - father.objects_positions[f_o][1])) * 1.0)
                if percentage_within > 0.5:
                    self.objects_positions.append(to_analyse)
                    self.objects_names.append(father.bbox_names[f_o])

    # Resize the crop with the max width and height
    def resize_crop(self):
        image_cropped = Image.open(self.father_path).crop(self.crop)
        resize_factor = 1
        # If width or height are bigger, resize
        if self.width > max_width:
            resize_factor = (self.width/max_width)
        if (self.height / resize_factor) > max_height:
            resize_factor = resize_factor * (self.height / max_height)
        self.image_cropped = image_cropped.resize((int(self.width / resize_factor), int(self.height / resize_factor)))
        self.resize_factor = resize_factor
        self.width = int(self.width / resize_factor)
        self.height = int(self.height / resize_factor)
        # Resize object positions
        for pos_obj in range(len(self.objects_positions)):
            object_to_resize = self.objects_positions.pop(0)
            x_min = int(object_to_resize[0] / resize_factor)
            y_min = int(object_to_resize[1] / resize_factor)
            x_max = int(object_to_resize[2] / resize_factor)
            y_max = int(object_to_resize[3] / resize_factor)
            new_size = [x_min, y_min, x_max, y_max]
            self.objects_positions.append(new_size)

    # Make the crop of the image
    def crop_image(self):
        # Crop the image
        if self.image_cropped is None:
            x_image = Image.open(self.father_path)
            cropped = x_image.crop(self.crop)
        else:
            cropped = self.image_cropped
        if cropped.size[0] > max_width or cropped.size[1] > max_height:
            print(self.father.image_name, cropped.size)

        save_path = str(self.father.image_name[:-4]) + "_" + str(self.mode) + "_" + str(self.crop[0]) + "_"
        save_path = save_path + str(self.crop[1]) + "_" + str(self.crop[2]) + "_" + str(self.crop[3]) + ".jpg"
        cropped.save(self.father.crop_path + save_path, quality=100)
        # Make the xml file
        xml_contend = "<annotation>\n\t<folder></folder>\n\t<filename>" + save_path + "</filename>\n\t<path></path>\n" \
                      + "\t<source><database></database></source>\n\t<size>\n\t\t<width>" + str(self.width) \
                      + "</width>\n\t\t<height>" + str(self.height) + "</height>\n\t\t<depth>3</depth>\n\t</size>\n\t" \
                      + "<segmented>0</segmented>\n"
        # Add all the objects to the xml file
        for bbox_o in range(len(self.objects_positions)):
            x_min = self.objects_positions[bbox_o][0] - int(self.crop[0]/self.resize_factor)
            y_min = self.objects_positions[bbox_o][1] - int(self.crop[1]/self.resize_factor)
            x_max = self.objects_positions[bbox_o][2] - int(self.crop[0]/self.resize_factor)
            y_max = self.objects_positions[bbox_o][3] - int(self.crop[1]/self.resize_factor)
            if x_min < 0:
                print("Warning: xmin < 0", x_min, self.father.image_name, self.mode)
                x_min = 0
            if y_min < 0:
                print("Warning: ymin < 0", y_min, self.father.image_name, self.mode)
                y_min = 0
            if x_max > self.width:
                print("Warning: xmax > width", x_max, self.width, self.father.image_name, self.mode)
                x_max = self.width
            if y_max > self.height:
                print("Warning: ymax > height", y_max, self.height, self.father.image_name, self.mode)
                y_max = self.height
            if x_min < 0 or y_min < 0:
                print("xmin or ymin < 0")
            if x_max > max_width or y_max > max_height:
                print("xmax or ymax > max_width or max_height")
            xml_contend += "\t<object>\n\t\t<name>" + self.objects_names[bbox_o] + "</name>\n"
            xml_contend += "\t\t<pose>Unspucified</pose>\n\t\t<truncated>0</truncated>\n"
            xml_contend += "\t\t<difficult>0</difficult>\n\t\t<bndbox>\n" + "\t\t\t<xmin>" + str(x_min) + "</xmin>\n"
            xml_contend += "\t\t\t<ymin>" + str(y_min) + "</ymin>\n" + "\t\t\t<xmax>" + str(x_max) + "</xmax>\n"
            xml_contend += "\t\t\t<ymax>" + str(y_max) + "</ymax>\n" + "\t\t</bndbox>\n\t</object>\n"
        xml_contend = xml_contend + "</annotation>\n"
        xml_file = open(self.father.crop_path + save_path[:-3] + "xml", 'w')
        xml_file.write(xml_contend)
        xml_file.close()

    # Print the crop attributes
    def print_crop_attribute(self):
        print("Crop")
        print(self.crop)
        print(self.width)
        print(self.height)


# Function to select the corner of the crop
def select_corner(x_a, y_a, x_b, y_b, x, y, w, h, corner):
    if corner == 'l_s':
        x_b = x_b + w - x
        y_b = y_b + h - y
    elif corner == 'r_s':
        x_a = x_a - w + x
        y_b = y_b + h - y
    elif corner == 'l_i':
        x_b = x_b + w - x
        y_a = y_a - h + y
    elif corner == 'r_i':
        x_a = x_a - w + x
        y_a = y_a - h + y

    return x_a, y_a, x_b, y_b


# Adjust x and y coordinates to max dims
def check_max_dim(self, x_ini, x_fin, y_ini, y_fin, m_w, m_h):
    total_x = x_fin - x_ini
    total_y = y_fin - y_ini
    conta = 0
    if total_x < m_w:
        while total_x < m_w:
            if conta % 2 == 0:
                if x_ini > 0:
                    x_ini = x_ini - 1
            else:
                if x_fin < self.width:
                    x_fin = x_fin + 1
            total_x = x_fin - x_ini
            conta += 1
    if total_y < m_h:
        while total_y < m_h:
            if conta % 2 == 0:
                if y_ini > 0:
                    y_ini = y_ini - 1
            else:
                if y_fin < self.height:
                    y_fin = y_fin + 1
            total_y = y_fin - y_ini
            conta += 1
    return x_ini, x_fin, y_ini, y_fin


# Adjust border
def adjust_border(x_ini, x_fin, y_ini, y_fin, w, h):
    if x_ini < 0:
        x_ini = 0
    if y_ini < 0:
        y_ini = 0
    if x_fin > w:
        x_fin = w
    if y_fin > h:
        y_fin = h
    return x_ini, x_fin, y_ini, y_fin


# LabeledImage class
class LabeledImage:
    # Init method
    def __init__(self, xml_path, dir_images, crop_path):
        self.xml_path = xml_path
        self.dir_images = dir_images
        self.crop_path = crop_path
        self.image_path = None
        self.image_name = None
        self.width = None
        self.height = None
        self.num_objects = None
        self.bbox_names = []
        self.objects_positions = []
        self.cropped = []

    # Obtain object image name, width, height, bbox and number objects
    def analise_attributes(self):
        xml_file = open(self.xml_path, 'r')
        objects_positions = []
        for xml_line in xml_file:
            # Obtain image name
            if 'filename' in xml_line:
                image_name = xml_line.split('<filename>')[1]
                self.image_name = image_name.split('</filename>')[0]
                self.image_path = self.dir_images + self.image_name
            # Obtain width and height
            if 'width' in xml_line:
                width_character = xml_line
                while not ('0' <= width_character[0] <= '9'):
                    width_character = width_character[1:]
                while not ('0' <= width_character[-1] <= '9'):
                    width_character = width_character[:-1]
                self.width = int(width_character)
            elif 'height' in xml_line:
                height_character = xml_line
                while not ('0' <= height_character[0] <= '9'):
                    height_character = height_character[1:]
                while not ('0' <= height_character[-1] <= '9'):
                    height_character = height_character[:-1]
                self.height = int(height_character)
            # Obtain bbox name
            if '<name>' in xml_line:
                name = xml_line.split('<name>')[1]
                self.bbox_names.append(name.split('</name>')[0])
            # Obtain bbox positions
            if 'xmin' in xml_line:
                xmin = xml_line
                while not ('0' <= xmin[0] <= '9'):
                    xmin = xmin[1:]
                while not ('0' <= xmin[-1] <= '9'):
                    xmin = xmin[:-1]
                objects_positions.append(int(xmin))
            elif 'ymin' in xml_line:
                ymin = xml_line
                while not ('0' <= ymin[0] <= '9'):
                    ymin = ymin[1:]
                while not ('0' <= ymin[-1] <= '9'):
                    ymin = ymin[:-1]
                objects_positions.append(int(ymin))
            elif 'xmax' in xml_line:
                xmax = xml_line
                while not ('0' <= xmax[0] <= '9'):
                    xmax = xmax[1:]
                while not ('0' <= xmax[-1] <= '9'):
                    xmax = xmax[:-1]
                objects_positions.append(int(xmax))
            elif 'ymax' in xml_line:
                ymax = xml_line
                while not ('0' <= ymax[0] <= '9'):
                    ymax = ymax[1:]
                while not ('0' <= ymax[-1] <= '9'):
                    ymax = ymax[:-1]
                objects_positions.append(int(ymax))
        # Obtain number objects
        self.num_objects = int(len(objects_positions) / 4)
        for x_object in range(self.num_objects):
            bounding_box = []
            for i in range(4):
                bounding_box.append(objects_positions.pop(0))
            self.objects_positions.append(bounding_box)

    # Obtain centers crops on the image
    def obtain_positions_crop(self, m_w, m_h, corner):
        for box in range(self.num_objects):
            x_mi, y_mi, x_ma, y_ma = self.objects_positions[box]
            # Obtain dim of object
            x_dim = x_ma - x_mi
            y_dim = y_ma - y_mi
            # If the dim of object is larger than max dims, we need to rescale
            if x_dim > m_w or y_dim > m_h:
                factor_w = x_dim / m_w
                factor_h = y_dim / m_h
                max_factor = factor_w
                if max_factor < factor_h:
                    max_factor = factor_h
                max_factor = round(max_factor, 2)
                dim_w = int(max_factor * m_w)
                dim_h = int(max_factor * m_h)
                if dim_w > self.width:
                    dim_w = self.width
                if dim_h > self.height:
                    dim_h = self.height
                x_ini, x_fin, y_ini, y_fin = check_max_dim(self, x_mi, x_ma, y_mi, y_ma, dim_w, dim_h)
            # Else, we don't need to rescale
            else:
                if corner == 'center':
                    x_ini = x_mi - int((m_w - x_dim) / 2)
                    x_fin = int((m_w - x_dim) / 2) + x_ma
                    y_ini = y_mi - int((m_h - y_dim) / 2)
                    y_fin = int((m_h - y_dim) / 2) + y_ma
                else:
                    x_ini, y_ini, x_fin, y_fin = select_corner(x_mi, y_mi, x_ma, y_ma, x_dim, y_dim, m_w, m_h, corner)
                # Adjust border
                x_ini, x_fin, y_ini, y_fin = adjust_border(x_ini, x_fin, y_ini, y_fin, self.width, self.height)
                # Check dim
                x_ini, x_fin, y_ini, y_fin = check_max_dim(self, x_ini, x_fin, y_ini, y_fin, m_w, m_h)
                # If the crop will be minor than the bbox, select bbox
                if x_ini > x_mi:
                    print("Warning: Crop can't be minor x_ini ", x_ini, x_mi, self.image_name)
                    x_ini = x_mi
                if y_ini > y_mi:
                    print("Warning: Crop can't be minor y_ini ", y_ini, y_mi, self.image_name)
                    y_ini = y_mi
                if x_fin < x_ma:
                    print("Warning: Crop can't be minor x_fin ", x_fin, x_ma, self.image_name)
                    x_fin = x_ma
                if y_fin < y_ma:
                    print("Warning: Crop can't be minor y_fin ", y_fin, y_ma, self.image_name)
                    y_fin = y_ma
                # Check dim
                x_ini, x_fin, y_ini, y_fin = check_max_dim(self, x_ini, x_fin, y_ini, y_fin, m_w, m_h)
                # Adjust border
                x_ini, x_fin, y_ini, y_fin = adjust_border(x_ini, x_fin, y_ini, y_fin, self.width, self.height)
            # Save crop
            self.cropped.append(CropImage(self, [x_ini, y_ini, x_fin, y_fin], corner))

    # Print attributes of the object
    def print_attributes(self):
        print(self.xml_path)
        print(self.image_path)
        print(self.width)
        print(self.height)
        print(self.num_objects)
        print(self.bbox_names)
        print(self.objects_positions)
        for img_cropped in self.cropped:
            img_cropped.print_crop_attribute()


# Parameters to the maximum size of the image
max_width = 2000
max_height = 1630
Image.MAX_IMAGE_PIXELS = 933120000

# Search the xml of the images to divide
path_xml = './xmls/'
path_images = './images/'
crop_dir = './crop/'
if not os.path.exists(crop_dir):
    os.mkdir(crop_dir)
list_xml_files = os.listdir(path_xml)
list_xml_files.sort()

# First the images will be decrease by PIL library
list_file = os.listdir(path_images)
list_file.sort()

# Create labeled images objects
list_labeled_images = []
for actual_xml in list_xml_files:
    list_labeled_images.append(LabeledImage(path_xml + actual_xml, path_images, crop_dir))

# Initialize attributes of labeled objects and prepare crops
for labeled_img in list_labeled_images:
    labeled_img.analise_attributes()
    # If the images are little than max dims
    if max_width > labeled_img.width or max_height > labeled_img.height:
        max_w = labeled_img.width
        max_h = labeled_img.height
    else:
        max_w = max_width
        max_h = max_height
    # Prepare crop
    labeled_img.obtain_positions_crop(max_w, max_h, 'center')

# Make crops
for labeled_img in list_labeled_images:
    for li_crop in labeled_img.cropped:
        li_crop.resize_crop()
        li_crop.crop_image()
