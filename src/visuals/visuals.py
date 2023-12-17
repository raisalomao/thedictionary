"""Módulo para processamentos visuais baseados nas
palavras e recursos obtidos.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

from typing import List
from pathlib import Path

from dataclasses import dataclass


def _checkfile(folder = str, filename = str) -> bool:
    """Verifica se já existe um arquivo em um diretório
    """
    if not all(isinstance(param, str) for param in (folder, filename)):
        raise ValueError('Ambos parâmetros devem ser string.')
    
    filepath = Path(folder) / filename
    return filepath.exists()

def rotate_polygon(vertices, angle):
    """Rotaciona um polígono em relação à origem (0, 0).
    """
    matrix = np.array(
        [[np.cos(angle), -np.sin(angle)],
         [np.sin(angle),  np.cos(angle)]]
    )

    polygon_matrix = np.array(vertices).T
    polygon_matrix = matrix @ polygon_matrix
    rotated_vertices = polygon_matrix.T.tolist()

    return rotated_vertices


class Images:
    """Armazena um conjunto de métodos para 
    processamento de imagens.
    """
    
    def __init__(self,
    words = str,
    objects: List[str] = [],
    watermark = "thedictionary.com.br"
    ) -> None:
        self.words = words
        self.objects = objects
        self.watermark = watermark
        self._apresentation = self._image_apresentation()

    def _image_apresentation(self, word = str, meanings = list):
        """Retorna a imagem de apresentação de
        uma palavra.
        """
        pass 


@dataclass
class Animations:
    """Processa animações 
    com base em palavras e recursos obtidos.
    """

    @staticmethod
    def analogic_sinonimos(principal = str, connected = list):
        """Cria uma representação visual, semelhante a um dicionário
        analógico. 
        Ligando a palavra `central` digitada pelo usuário aos 
        seus sinônimos.
            Faz uso da função Portuguese para garantir a lista de `sinônimos`,
        integrando seus vetores ao array principal.
        """
        assert principal is not None, "Adicione a palavra central como parâmetro."

        if _checkfile("./visuals/analogic/", f"{str(principal).lower()}.gif"):
            return

        if not connected:
            return
        else:
            fig, ax = plt.subplots()
            fig.set_size_inches(6, 6)
            ax.set_aspect('equal', 'box')
            ax.axis('off')

            radius = 0.4
            angles = np.linspace(0.01, 2 * np.pi, len(connected), endpoint=False)
            circles: List[patches.Ellipse] = []
            lines: List[plt.Line2D] = []
            words: List[plt.Text] = []

            for angle, word in zip(angles, connected):
                x1, y1 = (
                    0.5 + 0.09 * np.cos(angle), 
                    0.5 + 0.09 * np.sin(angle)
                )

                x2, y2 = (
                    0.5 + (radius - 0.08) * np.cos(angle), 
                    0.5 + (radius - 0.08) * np.sin(angle)
                )
                line, = ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.6)
                lines.append(line)

                x, y = (
                    0.1 + radius * np.cos(angle), 
                    0.1 + radius * np.sin(angle)
                )
                size = 0.20 if len(max(connected, key=len)) > 13 else 0.15
                circle = patches.Ellipse((x, y), width=size, height=0.1, color='red', alpha=0.5)
                ax.add_patch(circle)
                circles.append(circle)
                
                words.append(ax.text(x, y, word, ha='center', 
                va='center', color='black', fontfamily='Arial', fontsize=10))

            num = len(connected)
            
            polygon_size = 0.125 if len(principal) > 14 else 0.115

            if len(connected) <= 2:
                ax.add_patch(plt.Circle(
                    (0.5, 0.5), 0.09, color='orange', alpha=0.8) )

            if len(connected) == 3:
                polygon_size = 0.15
                v = [
                    (
                    0.5 + polygon_size * np.cos(2 * np.pi * i / num),
                    0.5 + polygon_size * np.sin(2 * np.pi * i / num)
                    ) for i in range(num)
                ]

                vr = rotate_polygon(v, np.radians(90))
                vr_centralize = [
                    (
                    0.5 + v[0] - np.mean([v[0] for v in vr]),
                    0.5 + v[1] - np.mean([v[1] for v in vr])
                    ) for v in vr
                ]
                ax.add_patch(plt.Polygon(vr_centralize, color='orange', alpha=0.8))
            else:

                vertices = [
                    (
                    0.5 + polygon_size * np.cos(2 * np.pi * i / num), 
                    0.5 + polygon_size * np.sin(2 * np.pi * i / num)
                    ) for i in range(num)
                ]

                ax.add_patch(plt.Polygon(vertices, color='orange', alpha=0.8))


            ax.text(0.05, 0.05, "thedictionary©", fontsize=10, fontfamily='Courier New', alpha=0.6)
            main_text = ax.text(0.5, 0.5, principal, ha='center', va='center', fontsize=11, fontfamily='Arial')

            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            def update_frames(frame):
                angle = frame / 300 * 2 * np.pi
                for i, (circle, line, word) in enumerate(zip(circles, lines, words)):
                    x, y = (
                        0.5 + radius * np.cos(angle + angles[i]), 
                        0.5 + radius * np.sin(angle + angles[i])
                    )
                    circle.center = (x, y)

                    x1, y1 = (
                        0.5 + 0.12 * np.cos(angle + angles[i]), 
                        0.5 + 0.12 * np.sin(angle + angles[i])
                    )

                    x2, y2 = (
                        0.5 + (radius - 0.08) * np.cos(angle + angles[i]), 
                        0.5 + (radius - 0.08) * np.sin(angle + angles[i])
                    )
                    line.set_data([x1, x2], [y1, y2])
                    word.set_position((x, y))

                return main_text.set_position((0.5, 0.5))

            ani = animation.FuncAnimation(fig, update_frames, frames=300, interval=300)

            fig.patch.set_facecolor('white')
            ax.set_position([0, 0, 1, 1])
            filepath = Path("./visuals/analogic") / f"{principal.lower()}.gif"

        return ani.save(filepath, writer='pillow')