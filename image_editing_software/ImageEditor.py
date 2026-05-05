import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import re

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
        image_path = os.path.isfile(name)
        if (not image_path):
            print("Essa imagem não existe no diretório - Carregue outra imagem!")
            while(not image_path):
                name = input("Digite o nome e extensão da imagem (ex: nome_imagem.png): ")
                image_path = os.path.isfile(name)
            self.image_name = name
        
        self.image = iio.imread(name)
        self.image = self.image.astype(np.uint8)

        self.original_image = iio.imread(name)
        self.original_image = self.original_image.astype(np.uint8)

    def show(self):
        print("=== Mostrando imagem ===")
        plt.imshow(self.image, cmap='gray')
        plt.title("Imagem")
        plt.axis('off')
        plt.show()

    def save(self, file_name):
        folder_path = "edited_images"
        save_path = os.path.join(folder_path, file_name)

        if os.path.exists(save_path):
            print("Arquivo já existe! - Sobreescrevendo...")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if self.image is not None:
            iio.imwrite(save_path, self.image.astype(np.uint8))
            print(f"Imagem salva como {file_name}")
        else:
            print("Nenhuma imagem para salvar!")

    def reset_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            print("Imagem resetada para original!")
        else:
            print("Nenhuma imagem carregada.")

    def main_menu(self):
        while (True):
            if (image_editor.image is None):                
                image_name = input("Digite o nome e extensão da imagem (ex: nome_imagem.png): ")
                self.load_image(image_name)

            print("\n===== MENU PRINCIPAL =====")
            print("1 - Carregar nova imagem")
            print("2 - Transformações Geométricas")
            print("3 - Transformações de Intensidade")
            print("4 - Mostrar imagem")
            print("0 - Sair")

            op = input("Escolha uma opção: ")

            if op == "1":
                image_name = input("Digite o nome e extensão da imagem (ex: nome_imagem.png): ")
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
        intensity_transformations = IntensityTransformations.IntensityTransformationsOperations()
        name = re.search(r"^[^.]*", self.image_name).group()

        while True:    
            print("\n===== Menu Transformações de Intensidade =====")
            print("1 - Inversa")
            print("2 - Log")
            print("3 - Gamma")
            print("4 - Modulação de Contraste")
            print("5 - Transformação Criativa")
            print("6 - Mostrar imagem")
            print("0 - Voltar ao menu principal")
            print("9 - Sair de tudo")

            op = input("Escolha: ")
            
            if op == "1":
                self.image = intensity_transformations.inverse(self.image)
                self.save(name+"_edited_inv.png")
                self.reset_image()
            elif op == "2":
                self.image = intensity_transformations.log_transformation(self.image)
                self.save(name+"_edited_image_log.png")
                self.reset_image()
            elif op == "3":
                g = float(input("Gamma: "))
                self.image = intensity_transformations.gamma_transformation(self.image, g)
                self.save(name+"_edited_image_gamma.png")
                self.reset_image()
            elif op == "4":
                a = int(input("a: "))
                b = int(input("b: "))
                c = int(input("c: "))
                d = int(input("d: "))
                self.image = intensity_transformations.mod_transformation(self.image, a, b, c, d)
                self.save(name+"_edited_image_mod.png")
                self.reset_image()
            elif op == "5":
                self.image = intensity_transformations.creativity_transformation(self.image)
                self.save(name+"_edited_image_lim.png")
                self.reset_image()
            elif op == "6":
                if self.image is not None:
                    self.show()
                else:
                    print("Carregue uma imagem primeiro!")
            elif op == "0":
                print("\nVoltando ao menu anterior ...")
                break
            elif op == "9":
                sys.exit()

    def menu_geometric_transformations(self):
        geometric_transformations = GeometricTransformations.GeometricTransformationsOperations()
        name = re.search(r"^[^.]*", self.image_name).group()
        while True:
            print("\n===== MENU Transformações Geométricas =====")
            print("1 - Translação")
            print("2 - Rotação")
            print("3 - Escala")
            print("4 - Mostrar Imagem")
            print("5 - Resetar imagem")
            print("0 - Voltar ao menu principal")
            print("9 - Sair de tudo")

            op = input("Escolha: ")

            if op == "1":
                dx = int(input("dx : "))
                dy = int(input("dy: "))
                self.image = geometric_transformations.translate(self.image, dx, dy)
                self.save(name+f"_translacao_image_{dx}_{dy}.png")
            elif op == "2":
                theta = float(input("Ângulo: "))
                self.image = geometric_transformations.rotate(self.image, theta)
                self.save(name+f"_rotacao_image_{theta}.png")
            elif op == "3":
                si = float(input("si: "))
                sj = float(input("sj: "))
                self.image = geometric_transformations.scale(self.image, si, sj)
                self.save(name+f"_escala_image_{si}_{sj}.png")
            elif op == "4":
                if self.image is not None:
                    self.show()
                else:
                    print("Carregue uma imagem primeiro!")
            elif op == "5":
                self.reset_image()
            elif op == "0":
                print("\nVoltando ao menu anterior ...")
                break
            elif op == "9":
        
if __name__ == "__main__":
    image_editor = ImageEditor("nara.jpg")
    image_editor.main_menu()