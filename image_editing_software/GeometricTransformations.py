import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np

class GeometricTransformationsOperations:
    """
    Classe que implementa operações de transformações geométricas em imagens.
    
    As transformações são realizadas por meio de mapeamento inverso: para cada pixel
    da imagem de saída, calcula-se sua coordenada correspondente na imagem original
    usando uma matriz de transformação inversa. 
    
    Interpolação utilizada: vizinho mais próximo.
    """

    def inv_rot_matrix(self, theta, center):
        """Retorna a matriz de rotação em torno do centro.
        
        Parâmetros:
        - theta: ângulo de rotação em graus (sentido anti-horário).
        - center: coordenadas (cx, cy) do centro da rotação.
        """

        cx, cy = center
        theta = np.radians(theta)

        # Matriz de translação para a origem            
        T1 = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]], dtype=np.float32)

        # Matriz de rotação inversa
        R = np.array([
            [np.cos(theta), np.sin(theta), 0],
            [-np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]])
        
        # Matriz de translação de volta ao centro
        T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]], dtype=np.float32)
        
        # Matriz final
        M = T2 @ R @ T1
        
        return M
    
    def inv_scale_matrix(self, si, sj, img_shape):
        """
        Retorna a matriz de transformação para escala.
        Permite fatores de escala positivos (redimensionamento) e negativos (espelhamento).
        
        Parâmetros:
        - si: fator de escala na direção vertical
        - sj: fator de escala na direção horizontal
        - img_shape: tupla (h, w) da imagem original
        """

        h, w = img_shape[:2]

        # Matriz de escala inversa
        S = np.array([
            [1.0 / si, 0, 0],
            [0, 1.0 / sj, 0],
            [0, 0, 1]
        ], dtype=np.float32)


        # Correção de translação para espelhamento:
        # Quando o fator é negativo, a imagem é invertida e precisa ser deslocada
        # para que a região espelhada permaneça dentro do canvas.
        tx = 0
        ty = 0

        if si < 0:
            tx = w
        if sj < 0:
            ty = h

        # Matriz de translação para valores negativos
        T = np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=np.float32)

        return T @ S
    
    def transformation(self, img, M):
        """
        Aplica uma transformação geométrica genérica usando mapeamento inverso.
        
        
        Parâmetros:
        - img: imagem de entrada
        - M: matriz 3x3 de transformação
        """

        if img.ndim == 3:
            h, w, c = img.shape
            new_img = np.zeros_like(img)
        else:
            h, w = img.shape
            new_img = np.zeros_like(img)

        # máscara de pixels válidos
        mask = np.zeros((h, w), dtype=bool)

        # Mapeamento inverso: percorre todos os pixels da imagem de saída
        for i in range(h):
            for j in range(w):
            
                p = M @ np.array([j, i, 1], dtype=np.float32)

                j_orig = int(np.round(p[0])) 
                i_orig = int(np.round(p[1])) 

                if 0 <= i_orig < h and 0 <= j_orig < w:
                    new_img[i, j] = img[i_orig, j_orig]
                    # Marca pixels válidos
                    mask[i, j] = True
       
        # Caso nenhum pixel tenha sido preenchido
        if not np.any(mask):
            print("Erro: transformação gerou imagem vazia.")
            return img

        # Encontra os índices mínimo e máximo dos pixels válidos
        coords = np.argwhere(mask)
        min_i, min_j = coords.min(axis=0)
        max_i, max_j = coords.max(axis=0)

        # Recorta a imagem na região que contém apenas os pixels válidos
        cropped = new_img[min_i:max_i+1, min_j:max_j+1]

        return cropped

    def translate(self, img, dx, dy):
        """
        Translação da imagem com expansão automática do canvas.
        Essa abordagem garante que nenhum pixel da imagem seja perdido.
        
        Parâmetros:
        - img: imagem de entrada
        - dx: deslocamento horizontal.
        - dy: deslocamento vertical.
        """

        h, w = img.shape[:2]

        new_h = h + abs(dy)
        new_w = w + abs(dx)


        # Cria a nova imagem com as dimensões expandidas
        if img.ndim == 3:
            new_img = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
        else:
            new_img = np.zeros((new_h, new_w), dtype=img.dtype)

        
        # Novo posicionamento
        off_y = max(dy, 0)
        off_x = max(dx, 0)

        # Posição onde a imagem será colocada
        start_y = off_y
        end_y = off_y + h

        start_x = off_x
        end_x = off_x + w

        # Copia a imagem original para a posição calculada
        new_img[start_y:end_y, start_x:end_x] = img

        return new_img

    def rotate(self, img, angle_deg):
        """
        Rotação da imagem em torno do centro.
        
        Parâmetros:
        - img: imagem de entrada
        - angle_deg: ângulo de rotação em graus (sentido anti-horário)
        """

        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        M = self.inv_rot_matrix(angle_deg, center)
        return self.transformation(img, M)

    def scale(self, img, sx, sy):
        """
        Escala da imagem.
        
        Parâmetros:
        - img: imagem de entrada
        - sx: fator de escala vertical.
        - sy: fator de escala horizontal.
        """
        
        M = self.inv_scale_matrix(sx, sy, img.shape)
        return self.transformation(img, M)