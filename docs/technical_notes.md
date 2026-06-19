# Sistema de Pouso de Precisão por Marcadores ArUco

> Estimativa de pose em tempo real para guiamento de aproximação e pouso autônomo de VTOLs, usando visão computacional monocular.

---

## 1. Visão Geral

Em sistemas de pouso autônomo de drones e VTOLs, o GPS sozinho não é preciso o suficiente para garantir um touchdown seguro em uma plataforma pequena (precisão típica de GPS civil: 2-5 metros; uma plataforma de pouso pode ter menos de 1 metro). A indústria resolve isso combinando GPS com **visão computacional**: um marcador fiducial (ArUco, AprilTag) é fixado na zona de pouso, e a câmera da aeronave estima a posição e orientação relativa a esse marcador, corrigindo a trajetória final de aproximação.

Este projeto implementa essa técnica de forma standalone, usando uma webcam comum, demonstrando o princípio físico e matemático por trás dos sistemas de pouso de precisão usados em drones comerciais e militares (DJI, sistemas de pouso em porta-aviões para UAVs, etc).

## 2. Motivação

- Conecta diretamente com o trabalho de mapeamento aéreo e VTOL desenvolvido na UFV/NERo.
- Demonstra domínio de um problema real de robótica aérea, não um exercício acadêmico genérico.
- A técnica (pose estimation com marcadores) é transferível para múltiplas aplicações: docking de robôs, calibração de braços robóticos, AR/VR, inspeção industrial.
- É visualmente muito forte em vídeo/GIF — ideal para portfólio e LinkedIn.

## 3. Objetivo Técnico

Construir um sistema que, a partir do feed de uma webcam, seja capaz de:

1. Detectar um marcador ArUco no campo de visão.
2. Estimar a pose 6DOF (posição X, Y, Z + orientação roll, pitch, yaw) do marcador relativa à câmera.
3. Calcular e exibir, em tempo real, os comandos de correção que um VTOL real enviaria aos atuadores para se alinhar ao marcador (overlay tipo HUD).
4. Simular uma "zona de tolerância" de pouso — alertando visualmente quando a aeronave (representada pela câmera) está dentro dos parâmetros seguros de touchdown.

## 4. Stack Tecnológica

| Componente | Tecnologia | Papel |
|---|---|---|
| Captura de vídeo | OpenCV (`cv2.VideoCapture`) | Captura do feed da Logitech C920 |
| Detecção de marcador | OpenCV `cv2.aruco` | Localização do marcador no frame |
| Estimativa de pose | `solvePnP` (Perspective-n-Point) | Cálculo de posição/orientação 3D relativa |
| Calibração de câmera | OpenCV `calibrateCamera` (chessboard) | Correção de distorção da lente — essencial para precisão da pose |
| Visualização / HUD | OpenCV (overlay de texto/gráficos) | Exibição dos dados de pose e zona de tolerância |
| Lógica de controle (simulada) | Python puro | Tradução da pose em "comandos de correção" (sem hardware real) |
| Versionamento/Docs | Git + GitHub, README, GIFs | Apresentação do projeto |

### Por que essa stack importa para engenharia robótica

- **`solvePnP` e pose estimation** são a base matemática de SLAM, AR/VR, calibração robô-câmera (hand-eye calibration) e qualquer sistema de navegação visual. É um dos tópicos mais cobrados em processos seletivos de robótica/visão computacional.
- **Calibração de câmera** é um passo que muita gente pula, mas é o que separa um projeto amador de um projeto que entende o problema de verdade — distorção de lente não corrigida invalida qualquer medição de distância.
- **OpenCV** é a biblioteca padrão de indústria para visão computacional aplicada a robótica (usada em ROS, em sistemas embarcados, em produção).
- Marcadores fiduciais (ArUco/AprilTag) são tecnologia real de produção, não um exercício de brinquedo — usados em warehouse robotics (Amazon), pouso de drones, e calibração de múltiplas câmeras.

## 5. Arquitetura do Sistema

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  Webcam (C920)   │────▶│  Detecção ArUco   │────▶│  solvePnP (pose)    │
└─────────────────┘     └──────────────────┘     └─────────┬──────────┘
                                                            │
                         ┌──────────────────────────────────┘
                         ▼
              ┌────────────────────┐      ┌─────────────────────┐
              │  Cálculo de erro    │────▶│  HUD / Overlay       │
              │  (offset X,Y,Z,yaw) │      │  (vídeo em tempo real)│
              └────────────────────┘      └─────────────────────┘
                         │
                         ▼
              ┌────────────────────────┐
              │  Comandos simulados de  │
              │  correção de aproximação│
              └────────────────────────┘
```

## 6. Plano de Execução (Fim de Semana)

### Sábado — manhã (calibração e fundamentos)
- [ ] Imprimir um padrão de tabuleiro de xadrez (chessboard) para calibração.
- [ ] Capturar ~20 fotos do tabuleiro em ângulos variados com a C920.
- [ ] Rodar `cv2.calibrateCamera` para obter a matriz intrínseca da câmera e coeficientes de distorção.
- [ ] Salvar os parâmetros de calibração (`camera_matrix.npy`, `dist_coeffs.npy`).

### Sábado — tarde (detecção e pose)
- [ ] Gerar e imprimir um marcador ArUco (biblioteca `cv2.aruco`, dicionário `DICT_6X6_250`).
- [ ] Implementar a detecção do marcador em tempo real via webcam.
- [ ] Implementar `solvePnP` para extrair posição (X, Y, Z) e orientação (roll, pitch, yaw) do marcador relativo à câmera.
- [ ] Validar visualmente desenhando os eixos 3D sobre o marcador (`cv2.drawFrameAxes`).

### Domingo — manhã (lógica de pouso e HUD)
- [ ] Definir uma "zona de tolerância" de pouso (ex: erro lateral < 5cm, yaw < 10°).
- [ ] Implementar o HUD: overlay de texto com distância, ângulo, status (SEGURO/AJUSTANDO/FORA DE ALCANCE).
- [ ] Adicionar indicador visual (círculo/quadrado que muda de cor conforme se aproxima da tolerância).
- [ ] Testar com o marcador em diferentes distâncias e ângulos, simulando uma aproximação de pouso.

### Domingo — tarde (documentação e publicação)
- [ ] Gravar um GIF/vídeo curto do sistema funcionando (esse é o material principal para o LinkedIn).
- [ ] Escrever o README do GitHub (ver estrutura abaixo).
- [ ] Subir o repositório, organizar commits de forma legível.
- [ ] Escrever o post de LinkedIn.

## 7. Estrutura do Repositório (GitHub)

```
precision-landing-vision/
├── README.md
├── requirements.txt
├── calibration/
│   ├── calibrate_camera.py
│   ├── capture_chessboard.py
│   └── camera_params.npy
├── src/
│   ├── marker_generator.py
│   ├── pose_estimation.py
│   ├── landing_hud.py
│   └── main.py
├── assets/
│   ├── demo.gif
│   └── architecture_diagram.png
└── docs/
    └── technical_notes.md
```

## 8. Critérios de Sucesso

- Sistema detecta o marcador e estima pose com latência visualmente imperceptível (>15 FPS).
- Pose estimada é estável (sem "jitter" excessivo) a diferentes distâncias (30cm a 2m).
- HUD comunica claramente o status de alinhamento.
- README claro o suficiente para alguém reproduzir o projeto sem falar com você.

## 9. Possíveis Extensões Futuras (mencionar no README como "next steps")

- Integração com telemetria real via MQTT (conectando com seu projeto SMARTCAMP).
- Fusão com dados de IMU (filtro de Kalman) para suavizar a estimativa de pose.
- Portar a lógica para rodar embarcado (Raspberry Pi / Jetson Nano) a bordo de um VTOL real.
- Detecção de múltiplos marcadores para redundância em caso de oclusão parcial.

## 10. Rascunho de Post para LinkedIn

> 🚁 Fim de semana = projeto novo. Implementei um sistema de pouso de precisão por visão computacional, técnica usada por drones reais para corrigir a aproximação final quando o GPS não é preciso o suficiente.
>
> Usando uma webcam, marcadores ArUco e estimativa de pose (solvePnP), o sistema calcula em tempo real a posição e orientação relativas a uma zona de pouso — e exibe um HUD com o status de alinhamento, como faria o sistema de guiamento de um VTOL autônomo.
>
> Código e documentação completos no GitHub: [link]
>
> #robotics #computervision #uav #vtol #opencv #engenhariarobotica

---

*Projeto desenvolvido como parte de um portfólio de engenharia de robótica, conectado ao trabalho em VTOL e mapeamento aéreo na UFV/NERo.*
