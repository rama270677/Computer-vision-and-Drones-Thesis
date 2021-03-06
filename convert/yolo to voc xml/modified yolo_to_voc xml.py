from pascal_voc_io import XML_EXT
from pascal_voc_io import PascalVocWriter
from yolo_io import YoloReader
import os.path
import sys

try:
    from PyQt5.QtGui import QImage
except ImportError:
    from PyQt4.QtGui import QImage

 
def convert(image_path,annotation_path,save_path):
   
    
    for file in os.listdir(annotation_path):
        if file.endswith(".txt") and file != "classes.txt":
            #print("Convert", file)

            annotation_no_txt = os.path.splitext(file)[0]

            
            imagePath = image_path + "/" + annotation_no_txt + ".jpg"

            image = QImage()
            image.load(imagePath)
            imageShape = [image.height(), image.width(), 1 if image.isGrayscale() else 3]
            imgFolderName = os.path.basename(annotation_path)
            imgFileName = os.path.basename(imagePath)

            writer = PascalVocWriter(imgFolderName, imgFileName, imageShape, localImgPath=imagePath)


            # Read YOLO file
            txtPath = annotation_path + "/" + file
            tYoloParseReader = YoloReader(txtPath, image)
            shapes = tYoloParseReader.getShapes()
            num_of_box = len(shapes)

            for i in range(num_of_box):
                label = shapes[i][0]
                xmin = shapes[i][1][0][0]
                ymin = shapes[i][1][0][1]
                x_max = shapes[i][1][2][0]
                y_max = shapes[i][1][2][1]

                writer.addBndBox(xmin, ymin, x_max, y_max, label, 0)


            writer.save(targetFile=save_path  + "/" + annotation_no_txt + ".xml")


if __name__=="__main__":
    annotation_path = "C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Augmentation 3\\train_annotations_yolo" # should include the classes as well.
    image_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Augmentation 3\\train_images"
    save_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\final-dataset\\main\\Augmentation 3\\train_annotations_xml"

    convert(image_path,annotation_path,save_path)