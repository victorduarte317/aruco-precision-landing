"""
Calcula a matriz intrínseca da câmera e os coeficientes de distorção
a partir das imagens capturadas em calibration/images/.

IMPORTANTE: ajuste SQUARE_SIZE_MM para o tamanho REAL que você mediu
com a régua/trena na tela do celular.

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

SQUARE_SIZE_MM = 10.0  # <<< valor medido com a trena

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

def main():
    objp = np.zeros((PATTERN_SIZE[0] * PATTERN_SIZE[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)
    objp *= SQUARE_SIZE_MM

    objpoints = []
    imgpoints = []
    used_filenames = []

    images = sorted(glob.glob(os.path.join(IMAGES_DIR, "*.png")))
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
            used_filenames.append(fname)

    print(f"Padrão detectado em {len(objpoints)}/{len(images)} imagens.")

    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_shape, None, None
    )

    print("\n=== Resultado da calibração (todas as imagens) ===")
    print(f"Erro de reprojeção geral: {ret:.4f}")

    # --- NOVO: calcula o erro POR IMAGEM, pra identificar as piores ---
    print("\n=== Erro individual por imagem ===")
    per_image_errors = []
    for i in range(len(objpoints)):
        imgpoints_reproj, _ = cv2.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs
        )
        error = cv2.norm(imgpoints[i], imgpoints_reproj, cv2.NORM_L2) / len(imgpoints_reproj)
        per_image_errors.append((os.path.basename(used_filenames[i]), error))

    per_image_errors.sort(key=lambda x: x[1], reverse=True)
    for fname, err in per_image_errors:
        flag = "  <-- candidata a remover" if err > ret * 1.5 else ""
        print(f"  {fname}: {err:.4f}{flag}")

    print(f"\nMatriz da câmera:\n{camera_matrix}")
    print(f"Coeficientes de distorção:\n{dist_coeffs}")

    np.save(os.path.join(os.path.dirname(__file__), "camera_matrix.npy"), camera_matrix)
    np.save(os.path.join(os.path.dirname(__file__), "dist_coeffs.npy"), dist_coeffs)
    print("\nSalvo: camera_matrix.npy e dist_coeffs.npy")

    if ret > 1.0:
        print("\nAVISO: erro de reprojeção alto (>1.0). Veja a lista acima --")
        print("remova as imagens com erro mais alto e rode de novo.")

if __name__ == "__main__":
    main()