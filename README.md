# Precision Landing Vision

Estimativa de pose em tempo real para guiamento de aproximação e pouso de
precisão de VTOLs/drones, usando visão computacional monocular e marcadores
fiduciais ArUco.

📄 Documentação técnica completa: [`docs/technical_notes.md`](docs/technical_notes.md)

## Status
🚧 Em desenvolvimento — projeto de fim de semana, conectado ao trabalho de
mapeamento aéreo VTOL na UFV/NERo.

## Como funciona

```
Webcam → Detecção ArUco → solvePnP (pose 3D) → HUD de aproximação
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Calibração da câmera

Como solução criativa (sem impressora), o padrão de calibração é exibido
na tela do celular em vez de impresso em papel — funciona igualmente bem.

```bash
cd calibration
python generate_chessboard_pattern.py   # gera chessboard_pattern.png
# Abra chessboard_pattern.png em tela cheia no celular, brilho máximo
# Meça com uma régua o tamanho REAL de um quadrado (em mm)

python capture_chessboard.py            # capture 15-20 fotos (tecla 'c')
# Edite SQUARE_SIZE_MM em calibrate_camera.py com o valor medido

python calibrate_camera.py              # gera camera_matrix.npy e dist_coeffs.npy
```

## Marcador ArUco

```bash
cd src
python marker_generator.py   # gera aruco_marker.png
# Exiba na tela (celular/segundo monitor) ou imprima depois
```

## Roadmap

- [x] Estrutura do projeto
- [x] Geração de padrão de calibração e marcador
- [x] Scripts de captura e calibração de câmera
- [ ] Estimativa de pose (`src/pose_estimation.py`)
- [ ] HUD de status de pouso (`src/landing_hud.py`)
- [ ] Loop principal (`src/main.py`)
- [ ] Demo gravado (GIF)

## Stack

OpenCV (contrib, módulo `aruco`) · NumPy · Python 3

## Licença

MIT
