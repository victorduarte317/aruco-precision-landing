"""
Calcula a matriz intrínseca da câmera e os coeficientes de distorção
a partir das imagens capturadas em calibration/images/.

IMPORTANTE: ajuste SQUARE_SIZE_MM para o tamanho REAL que você mediu
com a régua na tela do celular (não o tamanho em pixels do arquivo!).
Isso é o que converte as medições de pixels para milímetros reais --
sem isso, a pose estimada não bate com a distância física verdadeira.

Uso:
    python calibrate_camera.py
"""

import cv2
import numpy as np
import glob
import os

SQUARES_X = 7
SQUARES_Y = 5
PATTERN_SIZE = (SQUARES_X - 1, SQUARES_Y - 1)

SQUARE_SIZE_MM = 25.0  # <<< TROQUE pelo valor medido com a régua na tela

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

def main():
    objp = np.zeros((PATTERN_SIZE[0] * PATTERN_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)
    objp *= SQUARE_SIZE_MM

    objpoints = []
    imgpoints = []

    images = glob.glob(os.path.join(IMAGES_DIR, "*.png"))
    if len(images) < 10:
        print(f"Apenas {len(images)} imagens encontradas. Capture pelo menos 10-15.")
        return

    img_shape = None
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_shape = gray.shape[::-1]

        found, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)
        if found:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners_refined)

    print(f"Padrão detectado em {len(objpoints)}/{len(images)} imagens.")

    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_shape, None, None
    )

    print("\n=== Resultado da calibração ===")
    print(f"Erro de reprojeção (quanto menor, melhor): {ret:.4f}")
    print(f"Matriz da câmera:\n{camera_matrix}")
    print(f"Coeficientes de distorção:\n{dist_coeffs}")

    np.save(os.path.join(os.path.dirname(__file__), "camera_matrix.npy"), camera_matrix)
    np.save(os.path.join(os.path.dirname(__file__), "dist_coeffs.npy"), dist_coeffs)
    print("\nSalvo: camera_matrix.npy e dist_coeffs.npy")

    if ret > 1.0:
        print("\nAVISO: erro de reprojeção alto (>1.0). Considere capturar mais")
        print("imagens com ângulos variados, ou verificar se SQUARE_SIZE_MM está correto.")

if __name__ == "__main__":
    main()
