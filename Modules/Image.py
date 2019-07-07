import cv2
import numpy

class Image:

    def __init__(self):
        self.path = ''
        self.img = None
        self.grayscale = None
        self.blurredimage = None
        self.cannyimage = None
        self.mask = None
        self.masked_image = None
        self.lines = None
        self.line_image = None
        self.average_lines = None
        self.final_image = None

    def set_img(self, img):
        self.img = img

    def set_path(self, path):
        self.path = path

    def set_grayscale(self, grayscale):
        self.grayscale = grayscale

    def set_blurredimage(self, blurredimage):
        self.blurredimage = blurredimage

    def set_cannyimage(self, canny):
        self.cannyimage = canny

    def set_mask(self, mask):
        self.mask = mask

    def set_masked_image(self, masked_image):
        self.masked_image = masked_image

    def set_lines(self, lines):
        self.lines = lines

    def set_line_image(self, line_image):
        self.line_image = line_image

    def set_average_lines(self, average_lines):
        self.average_lines = average_lines

    def set_final_image(self, final_image):
        self.final_image = final_image

    def get_img(self):
        return self.img

    def get_path(self):
        return self.path

    def get_grayscale(self):
        return self.grayscale

    def get_blurredimage(self):
        return self.blurredimage

    def get_cannyimage(self):
        return self.cannyimage

    def get_mask(self):
        return self.mask

    def get_masked_image(self):
        return self.masked_image

    def get_lines(self):
        return self.lines

    def get_line_image(self):
        return self.line_image

    def get_average_lines(self):
        return self.average_lines

    def get_final_image(self):
        return self.final_image