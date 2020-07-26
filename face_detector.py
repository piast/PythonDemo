import cv2
import os
import numpy as np

# from app_logger import get_logger



# logger = get_logger(__name__)


def detect_faces_quantity(file):
    image_np = np.asarray(bytearray(file), dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    return len(faces)


def show_dedected_face(file_path):
    imagePath = file_path
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    # logger.info(f'Found {len(faces)} Faces!')
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # status = cv2.imwrite('faces_detected.jpg', image)
    # logger.info("Image faces_detected.jpg written to filesystem: ", status)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',image)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()


# for file in os.listdir('/home/lty/Desktop/foto'):
#     file_name, file_extension = os.path.splitext(file)
#     if (file_extension in ['.png','.jpg']):
#         show_detected_face(base_dir + file)


# fd = open('/home/lty/Desktop/foto/Screenshot_2017-09-17-22-16-28-443_com.miui.gallery.png', 'br')
# img_str = fd.read()
# fd.close()

# detect_faces_quantity(img_str)