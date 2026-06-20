"""
Main loop: captures webcam frames, detects ArUco markers, estimates
their pose and draws the landing approach HUD.
"""

import cv2
from pose_estimation import load_calibration, create_detector, get_object_points, estimate_pose
from landing_hud import draw_landing_hud


def main():
    camera_matrix, dist_coeffs = load_calibration()
    detector = create_detector()
    object_points = get_object_points()

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
                marker_corners = corners[i][0]
                success, rvec, tvec = estimate_pose(
                    marker_corners, camera_matrix, dist_coeffs, object_points
                )

                if success:
                    cv2.drawFrameAxes(
                        frame, camera_matrix, dist_coeffs, rvec, tvec, 22.5
                    )
                    frame = draw_landing_hud(frame, rvec, tvec)

        cv2.imshow("Pose Estimation", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()