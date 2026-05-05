import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np

class IntensityTransformationsOperations:
    """
    Classe que contém operações de transformações de intensidade para imagens.
    
    Todas as funções recebem um array numpy (uint8) representando uma imagem e
    retornam um novo array transformado, também no formato uint8.
    """

    def inverse(self, z):
        """
        Transformação de intensidade inversa (negativo da imagem).
        
        Calcula o negativo de cada pixel: f(z) = 255 - z.
        """

        return 255 - z
    
    def mod_transformation(self, z, a=30, b=200, c=0, d=250):
        """
        Modulação de contraste.
        
        Mapeia o intervalo [a, b] da imagem original para o intervalo [c, d]
        na imagem de saída. Valores fora de [a, b] são truncados.
        """

        z = z.astype(float)
        z = (z-a)/(b-a)
        z = z*(d-c)+c
        z = np.clip(z, 0, 255)
        return z.astype(np.uint8) 

    def log_transformation(self, z):
        """
        Transformação logarítmica.
        
        Aplica f(z) = c * log(1 + z).
        """

        z = z.astype(float)
        c = 255/(np.log(255+1))
        z = c * np.log(1+z)
        return z.astype(np.uint8)

    def gamma_transformation(self, z, gamma=2.2):
        """
        Correção gama (transformação de potência).
        
        Aplica f(z) = 255 * (z/255)^(1/gamma) para realçar ou atenuar médios tons.
        """

        z = z.astype(float)
        z = z ** (1/gamma)
        z = z * 255/(255**(1/gamma))
        return z.astype(np.uint8)

    def creativity_transformation(self, z):
        """
        Transformação de intensidade criativa.
        
        Divide a faixa dinâmica em três regiões e aplica ganhos distintos:
        - Sombras (z < 64):  f(z) = 1.5 * z   
        - Médios (64 ≤ z < 192): f(z) = 0.5 * z
        - Altos (z ≥ 192):  f(z) = 2.0 * z     
        """

        baixo = z < 64
        medios = (z >= 64) & (z < 192)
        alto = z >= 192
        
        result = np.zeros_like(z)
        result[baixo] = 1.5 * z[baixo]
        result[medios] = 0.5 * (z[medios])
        result[alto] = 2 * (z[alto])
        
        result = np.clip(result, 0, 255).astype(np.uint8)
        return result
