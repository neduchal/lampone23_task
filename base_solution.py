import cv2
import matplotlib.pyplot as plt
import numpy as np
import urllib
from skimage import transform, data, io
import math

class BaseSolution:

    def __init__(self):
        pass

    def load_frame(self):
        # Nacteni jednoho snimku ze serveru

        # Load the fisheye-distorted image
        # https://i.ibb.co/d7Wgk4B/image.png
        # https://i.ibb.co/sKp0Z6g/image.png
        while True:
            try:
                image = io.imread("http://192.168.100.22/image/image.png")

                break  # Only triggered if input is valid...
            except ValueError as error:
                print(error)

        im_res = cv2.resize(image, (1920, 1440))

        # Define the distortion coefficients for experimentation
        k1 = -0.013  # Radial distortion coefficient
        k2 = 0.00014  # Radial distortion coefficient
        p1 = -0.0025  # Tangential distortion coefficient
        p2 = 0.0015  # Tangential distortion coefficient

        # Define the parameters for manual correction
        fov = 160  # Field of view (in degrees)
        dst_size = im_res.shape[:2][::-1]  # Destination image size (width, height)

        # Calculate the focal length based on the field of view
        focal_length = dst_size[0] / (2 * np.tan(np.radians(fov) / 2))

        # Generate a simple perspective transformation matrix
        K = np.array([[focal_length, 0, dst_size[0] / 2],
                      [0, focal_length, dst_size[1] / 2],
                      [0, 0, 1]])
        dist_coefs = np.array([k1, k2, p1, p2])

        # Undistort the image using the specified coefficients
        undistorted_image = cv2.undistort(im_res, K, dist_coefs)

        return undistorted_image


    def detect_playground(self, image):
        # Detekce hriste z nacteneho snimku

        im_bin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_bin = cv2.medianBlur(im_bin, 5)
        _, im_bin = cv2.threshold(im_bin, 135, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(im_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        rect = cv2.minAreaRect(sorted_contours[0])
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        # print(box)

        # mask = np.zeros(image.shape)
        # cv2.drawContours(mask, sorted_contours, -1, (255, 255, 255), 1)
        # cv2.drawContours(mask, [box], 0, (255, 0, 0), 1)

        src_pts = np.array(box, dtype=np.float32)
        dst_pts = np.array([[0, 0], [1000, 0], [1000, 1000], [0, 1000]], dtype=np.float32)

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warp = cv2.warpPerspective(image, M, (1000, 1000))

        centers = np.zeros((8,8))
        for i, x in enumerate(range(100, 900, 100)):
            for j, y in enumerate(range(100, 900, 100)):
                centers[i,j] = (x, y)

        print(centers)

        return warp

    def detect_robot(self, image):
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters =  cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(dictionary, parameters) # Prepare the CV2 aruco detector object

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert a color image to grayscale

        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image_gray) # Detect the aruco markers from the grayscale image
        
        corners = np.array(markerCorners, np.int32) # Convert markerCorners to a numpy array with type np.int32

        orientation = None # N = 0, E = 1, S = 2, W = 3
        if markerCorners != []: # If there are any corners make a bounding polygon
            front = corners[0][0]
            cv2.polylines(image,corners,True,(255,0,0),2)
            vector = [front[0][0]-front[1][0], front[0][1]-front[1][1]]
            vector_perpendicular = [-vector[1],vector[0]]
            angle = (math.atan2(vector_perpendicular[0],vector_perpendicular[1]) * 180 / math.pi) + 180
            #orientation = round((angle) / 90)
            orientation = int((angle + 45) % 360 // 90) # CHATGPT CAME TO THE RESCUE
            print(f"Vector: {vector}, Perpendicular: {vector_perpendicular}, Angle: {angle}, Orientation {orientation}")
            cv2.line(image, front[0], front[0]-vector, (0,255,0), 10)
            cv2.line(image, front[0], front[0]-vector_perpendicular, (0,0,255), 10)
            image = cv2.putText(image, f"Angle:{str(round(angle))}, Ori: {orientation}", front[0], cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0), 1, cv2.LINE_AA)


        #print(f"Corners: {corners}, IDs: {markerIds}, Main line: {front}") # Was for debug, best to keep it here

        imgplot = plt.imshow(image)

        plt.show()
        
        return corners, orientation, image

    def recognize_objects(self):
        # Rozpoznani objektu na hristi - cil, body, prekazky
        pass

    def analyze_playground(self):
        # Analyza dat vytezenych ze snimku
        pass

    def generate_path(self):
        # Vygenerovani cesty [L, F, R, B] -- pripadne dalsi kody pro slozitejsi ulohy
        pass

    def send_solution(self):
        # Poslani reseni na server pomoci UTP spojeni.
        pass

    def solve(self):
        image = self.load_frame()
        fixed_image = self.detect_playground(image)
        self.detect_robot(fixed_image)
        self.recognize_objects()
        self.analyze_playground()
        self.generate_path()
        self.send_solution()
        pass


if __name__ == "__main__":
    solution = BaseSolution()
    solution.solve()
