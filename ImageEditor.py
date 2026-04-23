import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
import os

import IntensityTransformations
import GeometricTransformations

class ImageEditor:
    def __init__(self, image_name = None):
        self.image_name = image_name
        self.original_image = None
        self.image = None
        if image_name:
            self.load_image(image_name)

    def load_image(self, name):
        self.image = iio.imread(name)
        self.image = self.image.astype(np.uint8)

        self.original_image = iio.imread(name)
        self.original_image = self.imoriginal_imageage.astype(np.uint8)

    def show(self):
        print("=== Mostrando imagem ===")
        plt.imshow(self.image, cmap='gray')
        plt.title("Imagem")
        plt.axis('off')
        plt.show()


    def save(self, filename):
        if os.path.exists(filename):
            print("Arquivo já existe! - Sobreescrevendo...")

        if self.image is not None:
            iio.imwrite(filename, self.image.astype(np.uint8))
            print(f"Imagem salva como {filename}")
        else:
            print("Nenhuma imagem para salvar!")

    def main_menu(self):
        while (True):

            if (image_editor.image is None):                
                image_name = input("Digite o nome e extensão da imagem (ex: nome_imagem.png) ")
                self.load_image(image_name)

            print("\n===== MENU PRINCIPAL =====")
            print("1 - Carregar nova imagem")
            print("2 - Transformações Geométricas")
            print("3 - Transformações de Intensidade")
            print("4 - Mostrar imagem")
            print("0 - Sair")

            op = input("Escolha uma opção: ")

            if op == "1":
                image_name = input("Digite o nome da imagem com a extensão (ex: nara.jpg): ")
                self.load_image(image_name)

            elif op == "2":
                self.menu_geometric_transformations()

            elif op == "3":
                self.menu_intensity_transformations()

            elif op == "4":
                if self.image is not None:
                    self.show()
                else:
                    print("Carregue uma imagem primeiro!")
            elif op == "0":
                print("\nSaindo ...")
                break

    def menu_intensity_transformations(self):
        pass

    def menu_geometric_transformations(self):
        pass
        
if __name__ == "__main__":
    image_editor = ImageEditor("nara.jpg")
    image_editor.main_menu()