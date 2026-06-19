"""
Captura frames da webcam para calibração.

Instruções de uso:
- Exiba o chessboard_pattern.png em tela cheia no celular.
- Rode este script. Uma janela com o preview da webcam vai abrir.
- Posicione o celular em diferentes ângulos/distâncias e aperte 'c' para
  capturar (tente cobrir: perto/longe, inclinado pra esquerda/direita/
  cima/baixo, em diferentes posições do quadro -- quanto mais variado,
  melhor a calibração). Capture pelo menos 15-20 imagens.
- Aperte 'q' para sair quando terminar.

As imagens vão para calibration/images/
"""

import cv2
import os

SQUARES_X = 7
SQUARES_Y = 5
PATTERN_SIZE = (SQUARES_X - 1, SQUARES_Y - 1)  # cantos internos
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images")
CAMERA_INDEX = 0  # ajuste se a C920 não for o dispositivo 0

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print(f"Não consegui abrir a câmera no índice {CAMERA_INDEX}.")
        print("Tente mudar CAMERA_INDEX para 1 ou 2 no script.")
        return

    count = len(os.listdir(OUTPUT_DIR))
    print("Pressione 'c' para capturar, 'q' para sair.")
    print(f"Já existem {count} imagens salvas.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao ler frame da câmera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)

        display = frame.copy()
        if found:
            cv2.drawChessboardCorners(display, PATTERN_SIZE, corners, found)
            cv2.putText(display, "PADRAO DETECTADO - aperte 'c'", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(display, "Padrao nao detectado", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(display, f"Capturadas: {count}", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Calibracao - captura", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') and found:
            filename = os.path.join(OUTPUT_DIR, f"img_{count:02d}.png")
            cv2.imwrite(filename, frame)
            print(f"Salvo: {filename}")
            count += 1
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nTotal de imagens capturadas: {count}")
    print("Próximo passo: rode calibrate_camera.py")

if __name__ == "__main__":
    main()
    