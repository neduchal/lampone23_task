import cv2
import matplotlib.pyplot as plt
import numpy as np
import urllib
from skimage import transform, data, io


class BaseSolution:

    def __init__(self):
        pass

    def load_frame(self):
        # Nacteni jednoho snimku ze serveru

        # Load the fisheye-distorted image
        # https://i.ibb.co/d7Wgk4B/image.png
        # https://i.ibb.co/sKp0Z6g/image.png
        image = io.imread("http://192.168.100.22/image/image.png")

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

        im_bin = cv2.cvtColor(undistorted_image, cv2.COLOR_BGR2GRAY)
        im_bin = cv2.medianBlur(im_bin, 5)
        _, im_bin = cv2.threshold(im_bin, 135, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(im_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        mask = np.zeros(undistorted_image.shape)

        cv2.drawContours(mask, sorted_contours, -1, (255, 255, 255), 1)

        rect = cv2.minAreaRect(sorted_contours[0])
        box = cv2.boxPoints(rect)

        box = np.intp(box)
        print(box)
        cv2.drawContours(mask, [box], 0, (255, 0, 0), 1)

        src_pts = np.array(box, dtype=np.float32)
        dst_pts = np.array([[0, 0], [1000, 0], [1000, 1000], [0, 1000]], dtype=np.float32)

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warp = cv2.warpPerspective(undistorted_image, M, (1000, 1000))

        f, ((ax0, ax1, ax2), (ax3, ax4, ax5)) = plt.subplots(2, 3, subplot_kw=dict(xticks=[], yticks=[]))
        ax0.imshow(image)
        ax1.imshow(im_res)
        ax2.imshow(undistorted_image)
        ax3.imshow(im_bin, cmap="binary")
        ax4.imshow(mask)
        ax5.imshow(warp)

        plt.show()
        return warp

    def detect_playground(self):
        # Detekce hriste z nacteneho snimku
        pass

    def detect_robot(self):
        # Detekce robota [ArUCo tag]
        pass

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
        self.load_frame()
        self.detect_playground()
        self.detect_robot()
        self.recognize_objects()
        self.analyze_playground()
        self.generate_path()
        self.send_solution()
        pass


if __name__ == "__main__":
    solution = BaseSolution()
    solution.solve()
