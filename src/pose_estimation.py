import cv2
import numpy as np
import os
from landing_hud import draw_landing_hud

calib_dir = os.path.join(os.path.dirname(__file__), "..", "calibration")
camera_matrix = np.load(os.path.join(calib_dir, "camera_matrix.npy"))
dist_coeffs = np.load(os.path.join(calib_dir, "dist_coeffs.npy"))

print("Camera matrix loaded:")
print(camera_matrix)

# ArUco marker size, in mm
MARKER_SIZE_MM = 45.0

# ArUco marker dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

# 3D coordinates of the marker corners, clockwise
# (top-left, top-right, bottom-right, bottom-left)
half = MARKER_SIZE_MM / 2.0
object_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float32)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i in range(len(ids)):
            marker_corners = corners[i][0]  # 4 (x, y) points from the image

            success, rvec, tvec = cv2.solvePnP(
                object_points, marker_corners, camera_matrix, dist_coeffs
            )

            if success:
                cv2.drawFrameAxes(
                    frame, camera_matrix, dist_coeffs, rvec, tvec, MARKER_SIZE_MM / 2
                )

                # tvec = [X, Y, Z] position in mm, relative to the camera
                distance = np.linalg.norm(tvec)
                frame = draw_landing_hud(frame, rvec, tvec)
                
    cv2.imshow("Pose Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()