"""
Gera uma imagem de tabuleiro de xadrez para EXIBIR NA TELA DO CELULAR
(em vez de imprimir em papel).

Por que isso funciona: o algoritmo de calibração só precisa de um padrão
plano, de alto contraste, com geometria conhecida. Uma tela funciona tão
bem quanto papel impresso -- só precisamos saber o tamanho FÍSICO real
de cada quadrado quando exibido na tela, o que vamos medir com uma régua.

Uso:
    python generate_chessboard_pattern.py

Gera: chessboard_pattern.png
"""

import cv2
import numpy as np

# Quantidade de quadrados (não de cantos internos!) -- ajuste se quiser
SQUARES_X = 7
SQUARES_Y = 5
SQUARE_SIZE_PX = 160   # tamanho de cada quadrado em pixels na imagem gerada
MARGIN_PX = 60         # margem branca ao redor (ajuda a detecção de cantos)

def generate_chessboard(squares_x, squares_y, square_size_px, margin_px):
    width = squares_x * square_size_px + 2 * margin_px
    height = squares_y * square_size_px + 2 * margin_px

    img = np.ones((height, width), dtype=np.uint8) * 255

    for row in range(squares_y):
        for col in range(squares_x):
            if (row + col) % 2 == 0:
                y0 = margin_px + row * square_size_px
                y1 = y0 + square_size_px
                x0 = margin_px + col * square_size_px
                x1 = x0 + square_size_px
                img[y0:y1, x0:x1] = 0

    return img

if __name__ == "__main__":
    pattern = generate_chessboard(SQUARES_X, SQUARES_Y, SQUARE_SIZE_PX, MARGIN_PX)
    cv2.imwrite("chessboard_pattern.png", pattern)
    print(f"Padrão gerado: chessboard_pattern.png ({SQUARES_X}x{SQUARES_Y} quadrados)")
    print(f"Cantos internos para calibração: {SQUARES_X - 1}x{SQUARES_Y - 1}")
    print()
    print(">>> PRÓXIMO PASSO <<<")
    print("1. Transfira essa imagem pro celular (ou abra direto se gerar lá).")
    print("2. Abra em modo galeria/fotos em TELA CHEIA (não no navegador, que")
    print("   pode adicionar barras e distorcer o tamanho).")
    print("3. Brilho no máximo, modo escuro/filtro de luz azul DESLIGADO.")
    print("4. Com uma régua, meça o tamanho de UM quadrado na tela em mm.")
    print("   Anote esse valor -- você vai precisar dele em calibrate_camera.py")
