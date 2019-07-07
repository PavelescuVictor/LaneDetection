import numpy
import cv2
import matplotlib.pyplot as plt
from Modules.Image import Image

class Repository:

    def __init__(self):
        self.video_frames = []
        self.video_path = None
        self.image = None

    def get_video_frames(self):
        return self.video_frames

    def get_image(self):
        return self.image

    def get_video_path(self):
        return self.video_path

    def add_to_video_frames(self, image):
        self.video_frames.append(image)

    def add_image(self, image):
        self.image = image

    def read_image(self):
        path = input('Image path: ')
        img = cv2.imread(path, 1)
        image = Image()
        image.set_img(img)
        image.set_path(path)
        self.add_image(image)

    def read_video_path(self):
        self.video_path = input('Video path: ')

    def show_image(self, img):
        cv2.imshow("Results", img)
        # for videos
        cv2.waitKey(1)
        #plt.imshow(img)
        #plt.show()

    def convert_image_to_grayscale(self, image):
        grayscale = cv2.cvtColor(image.get_img(), cv2.COLOR_RGB2GRAY)
        image.set_grayscale(grayscale)

    def blur_image(self, image):
        blurredimage = cv2.GaussianBlur(image.get_grayscale(), (5,5), 0)
        image.set_blurredimage(blurredimage)

    def canny_image(self, image):
        canny = cv2.Canny(image.get_blurredimage(), 50, 150)
        image.set_cannyimage(canny)

    def region_of_interest(self, image):
        height = image.get_img().shape[0]
        polygons = numpy.array([
            [(150, height - 70), (1200, height - 70), (650, 400)]
        ])
        mask = numpy.zeros_like(image.get_cannyimage())
        cv2.fillPoly(mask, polygons, [255, 255, 255])
        image.set_mask(mask)
        masked_image = cv2.bitwise_and(image.get_cannyimage(), mask)
        image.set_masked_image(masked_image)

    def lines(self, image):
        lines = cv2.HoughLinesP(image.get_masked_image(), 2 , numpy.pi/180, 100, numpy.array([]), minLineLength=40, maxLineGap=5)
        image.set_lines(lines)

    def display_lines(self, image):
        line_image = numpy.zeros_like(image.get_img())
        if image.get_average_lines() is not None:
            for x1, y1, x2, y2 in image.get_average_lines():
                try:
                    cv2.line(line_image, (x1,y1), (x2,y2), (255, 0, 0), 10)
                except Exception as e:
                    print(e,'\n')
                    print(x1, "--", y1, "--", x2, "--", y2)
                    print('\n')
        image.set_line_image(line_image)

    def make_coordinates(self, image, line_parameters):
        slope, intercept = line_parameters
        y1 = image.shape[0]
        y2 = int(y1 * (3.2/5))
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return numpy.array([x1, y1, x2, y2])

    def average_slope_intercept(self, image):
        left_fit = []
        right_fit = []
        for line in image.get_lines():
            x1, y1, x2, y2 = line.reshape(4)
            parameters = numpy.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
        left_fit_average = numpy.average(left_fit, axis = 0)
        right_fit_average = numpy.average(right_fit, axis = 0)
        try:
            left_line = self.make_coordinates(image.get_img(), left_fit_average)
            right_line = self.make_coordinates(image.get_img(), right_fit_average)
            image.set_average_lines(numpy.array([left_line, right_line]))
        except Exception as e:
            #That error is thrown when the "line_parameters" parameter passed to the "make_coordinates" function is nan,
            # which happens when either "left_fit" or "right_fit" in "average_slope_intercept" is nan, which in turn
            # happens when the algorithm fails to detect either the left lane or the right lane in a frame.
            # One workaround is to catch the error and return None in the "average_slope_intercept" function so that
            # the program can continue running if this error occurs.
            print(e,'\n')

    def final_image(self, image):
        final_image = cv2.addWeighted(image.get_img(), 0.8, image.get_line_image(), 1, 1)
        image.set_final_image(final_image)

    def process_image(self, image):
        self.convert_image_to_grayscale(image)
        self.blur_image(image)
        self.canny_image(image)
        self.region_of_interest(image)
        self.lines(image)
        self.average_slope_intercept(image)
        self.display_lines(image)
        self.final_image(image)
        self.show_image(image.get_final_image())

if __name__ == '__main__':
    repo = Repository()
    #repo.read_image()
    #repo.process_image(repo.get_image())

    repo.read_video_path()
    capture = cv2.VideoCapture(repo.get_video_path())
    while(capture.isOpened()):
        _, frame = capture.read()
        image = Image()
        image.set_img(frame)
        image.set_path(repo.get_video_path())
        repo.process_image(image)
        #repo.get_video_frames().append(image)
    capture.release()
    cv2.destroyAllWindows()