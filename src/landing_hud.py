"""
Visual HUD overlay for landing approach status.

Takes the pose (rvec, tvec) from pose_estimation.py and displays it as a simple HUD overlay on the video feed.
Draws distance, lateral offset, yaw angle, and a color-coded landing status indicator on the video frame.
"""

import cv2
import numpy as np

# Tolerance Thresholds
LATERAL_SAFE_MM = 30.0
LATERAL_ADJUSTING_MM = 80.0
YAW_SAFE_DEG = 15.0
YAW_ADJUSTING_DEG = 30.0

def get_yaw_degrees(rvec):
    # Convert rotation vector into a yaw angle in degrees.
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    yaw_rad = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    return np.degrees(yaw_rad)

def get_landing_status(lateral_offset_mm, yaw_deg):
    # Determine if the landing is safe, adjusting or out of range based on thresholds.
    yaw_abs = abs(yaw_deg)

    if lateral_offset_mm < LATERAL_SAFE_MM and yaw_abs < YAW_SAFE_DEG:
        return "SAFE", (0, 255, 0) # Green 
    elif lateral_offset_mm < LATERAL_ADJUSTING_MM and yaw_abs < YAW_ADJUSTING_DEG:
        return "ADJUSTING", (0, 255, 255) # Yellow
    else:
        return "OUT OF RANGE", (0, 0, 255) # Red
    
def draw_landing_hud(frame, rvec, tvec):
    # Draws the landing approach HUD on top of the frame.
    x_offset, y_offset, distance_mm = tvec.flatten()
    lateral_offset = np.sqrt(x_offset**2 + y_offset**2)
    yaw_deg = get_yaw_degrees(rvec)

    status, color = get_landing_status(lateral_offset, yaw_deg)

    # Text info (top-left corner)
    cv2.putText(frame, f"Distance: {distance_mm:.0f} mm", (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.putText(frame, f"Lateral Offset: {lateral_offset:.0f} mm", (15, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.putText(frame, f"Yaw: {yaw_deg:.1f} deg", (15, 80), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Status indicator (top-right corner)
    cv2.putText(frame, status, (frame.shape[1] - 220, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.circle(frame, (frame.shape[1] - 30, 30), 12, color, -1)

    return frame