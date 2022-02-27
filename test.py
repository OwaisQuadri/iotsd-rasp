import face_recogniton as fr
import os
# get face encoding of knowns
# os.system("libcamera-still -e png -o test.png --width 200 --height 200")
image_of_known = fr.load_image_file("test.png")

known_face_encoding = fr.face_encodings(image_of_known)[0]