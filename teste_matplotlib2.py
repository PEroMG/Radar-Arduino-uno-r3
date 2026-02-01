
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import serial as pyser


MAX_DIST = 300
IMG_SIZE = 600
CENTER = IMG_SIZE // 2

radar_img = np.zeros((IMG_SIZE, IMG_SIZE))
distancias = np.full(181, MAX_DIST)



def interpretar_data(linha: str):
    # formato esperado: angulo;distancia\n
    try:
        ang, dist = linha.strip().split(';')
        return int(ang), float(dist)
    except:
        return None, None



def desenha_raio(angulo_graus, distancia):
    rad = math.radians(angulo_graus)

    for d in range(int(distancia)):
        intensidade = int(150 * (1 - d / MAX_DIST))

        x = int(CENTER + (d / MAX_DIST) * CENTER * math.cos(rad))
        y = int(CENTER - (d / MAX_DIST) * CENTER * math.sin(rad))

        if 0 <= x < IMG_SIZE and 0 <= y < IMG_SIZE:
            radar_img[y, x] = max(radar_img[y, x], intensidade)
    for d in range(int(distancia), IMG_SIZE):
        x = int(CENTER + (d / MAX_DIST) * CENTER * math.cos(rad))
        y = int(CENTER - (d / MAX_DIST) * CENTER * math.sin(rad))
        if 0 <= x < IMG_SIZE and 0 <= y < IMG_SIZE:
            radar_img[y, x] = 0




def atualiza_radar(angulo_graus, distancia):
    global radar_img, distancias

    angulo_graus = max(0, min(int(angulo_graus), 180))
    distancia = max(0, min(distancia, MAX_DIST))

    distancias[angulo_graus] = distancia


    
    desenha_raio(angulo_graus, distancias[angulo_graus])


def limpar_linha(angulo_graus):
    rad = math.radians(angulo_graus)

    for d in range(IMG_SIZE):
        x = int(CENTER + (d / MAX_DIST) * CENTER * math.cos(rad))
        y = int(CENTER - (d / MAX_DIST) * CENTER * math.sin(rad))
        if 0 <= x < IMG_SIZE and 0 <= y < IMG_SIZE:
            radar_img[y, x] = 0


def cor_linha(angulo_graus, intensidade):
    rad = math.radians(angulo_graus)

    for d in range(IMG_SIZE):

        x = int(CENTER + (d / MAX_DIST) * CENTER * math.cos(rad))
        y = int(CENTER - (d / MAX_DIST) * CENTER * math.sin(rad))
        dx = x - CENTER
        dy = y - CENTER

        if dx*dx + dy*dy <= CENTER*CENTER and 0 <= x < IMG_SIZE and 0 <= y < IMG_SIZE:
            radar_img[y, x] = intensidade



ser = pyser.Serial(port = 'COM4', baudrate = 9600, timeout = 0.05)

plt.ion()
fig, ax = plt.subplots()
img_plot = ax.imshow(radar_img, cmap="Greens", vmin=0, vmax=255)
ax.set_title("Radar")
ax.axis("off")




while True:
    ser.write(b"g\n")

    linha : str = ser.readline().decode(errors="ignore")
    if not linha:
        continue

    angulo, distancia = interpretar_data(linha)
    if angulo is None or distancia is None:
        continue


    cor_linha(angulo, 250)
    img_plot.set_data(radar_img)
    plt.pause(0.05)
    atualiza_radar(angulo, distancia)
    img_plot.set_data(radar_img)

plt.ioff()
plt.show()


