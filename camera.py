import cv2
from queue import Queue
from multiprocessing import Process,Queue


class Camera(Process):
    def __init__(self, image_buffer:Queue, cam_index=0):
        Process.__init__(self)
        self.__cam_dev = None
        self.__cam_index = cam_index
        self.__close_flag = False
        self.__frame_rate = 10
        self.images_container = image_buffer

    def run(self):
        self.__cam_dev = cv2.VideoCapture(self.__cam_index)
        self.__close_flag = False
        if not self.__cam_dev.isOpened():
            raise ValueError("can't open camera with {} index".format(self.__cam_index))
        while self.__close_flag == False:
            is_valid, image = self.__cam_dev.read()
            if is_valid==True:
                if self.images_container.full():
                    self.images_container.get()
                self.images_container.put(image)
            key =cv2.waitKey(50)
        self.__cam_dev.release()

    def get_last_image(self):
        if self.images_container.empty():
            return None
        else:
            return self.images_container.get()


    def close(self):
        self.__close_flag=True
