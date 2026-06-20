"""
Pose estimation utilities: camera calibration loading and ArUco marker 6DOF pose estimation via solvePnP.
"""

import cv2
import numpy as np
import os

MARKER_SIZE_MM = 45.0


def load_calibration():
    calib_dir = os.path.join(os.path.dirname(__file__), "..", "calibration")
    camera_matrix = np.load(os.path.join(calib_dir, "camera_matrix.npy"))
    dist_coeffs = np.load(os.path.join(calib_dir, "dist_coeffs.npy"))
    return camera_matrix, dist_coeffs


def create_detector():
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    aruco_params = cv2.aruco.DetectorParameters()
    return cv2.aruco.ArucoDetector(aruco_dict, aruco_params)


def get_object_points():
    half = MARKER_SIZE_MM / 2.0
    return np.array([
        [-half,  half, 0],
        [ half,  half, 0],
        [ half, -half, 0],
        [-half, -half, 0]
    ], dtype=np.float32)


def estimate_pose(marker_corners, camera_matrix, dist_coeffs, object_points):
    """Returns (success, rvec, tvec) for a single detected marker."""
    return cv2.solvePnP(object_points, marker_corners, camera_matrix, dist_coeffs)