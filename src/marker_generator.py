"""
Gera a imagem do marcador ArUco que vai representar a "zona de pouso".

Assim como o tabuleiro de calibração, este marcador também pode ser
exibido na tela do celular (ou de um segundo monitor/notebook) em vez
de impresso -- o detector funciona igual.

Uso:
    python marker_generator.py
"""

import cv2
import numpy as np

ARUCO_DICT = cv2.aruco.DICT_6X6_250
MARKER_ID = 0
MARKER_SIZE_PX = 600

def main():
    aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    marker_img = np.zeros((MARKER_SIZE_PX, MARKER_SIZE_PX), dtype=np.uint8)
    cv2.aruco.generateImageMarker(aruco_dict, MARKER_ID, MARKER_SIZE_PX, marker_img, 1)

    # margem branca, ajuda a detecção (o ArUco precisa de borda de "respiro")
    margin = 80
    final = np.ones((MARKER_SIZE_PX + 2 * margin, MARKER_SIZE_PX + 2 * margin), dtype=np.uint8) * 255
    final[margin:margin + MARKER_SIZE_PX, margin:margin + MARKER_SIZE_PX] = marker_img

    cv2.imwrite("aruco_marker.png", final)
    print(f"Marcador gerado: aruco_marker.png (ID={MARKER_ID}, dict=DICT_6X6_250)")
    print()
    print("Lembre de medir o tamanho REAL (em mm) do marcador quando exibido")
    print("na tela ou impresso depois -- esse valor entra em pose_estimation.py")

if __name__ == "__main__":
    main()
