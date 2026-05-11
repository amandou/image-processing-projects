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
        """Retorna a matriz inversa para rotação."""

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
        """Retorna a matriz inversa para escala."""

        h, w = img_shape[:2]

        S = np.array([
            [1.0 / si, 0, 0],
            [0, 1.0 / sj, 0],
            [0, 0, 1]
        ], dtype=np.float32)

        tx = 0
        ty = 0

        if si < 0:
            tx = w
        if sj < 0:
            ty = h

        T = np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=np.float32)

        return T @ S
    
    def transformation(self, img, M):
        """
        Aplica transformação geométrica com mapeamento inverso
        + crop automático baseado em máscara (robusto para JPEG/PNG)
        """

        if img.ndim == 3:
            h, w, c = img.shape
            new_img = np.zeros_like(img)
        else:
            h, w = img.shape
            new_img = np.zeros_like(img)

        # máscara de pixels válidos
        mask = np.zeros((h, w), dtype=bool)

        for i in range(h):
            for j in range(w):
            
                p = M @ np.array([j, i, 1], dtype=np.float32)

                j_orig = int(np.round(p[0])) 
                i_orig = int(np.round(p[1])) 

                if 0 <= i_orig < h and 0 <= j_orig < w:
                    new_img[i, j] = img[i_orig, j_orig]
                    mask[i, j] = True
       
        if not np.any(mask):
            print("Erro: transformação gerou imagem vazia.")
            return img

        coords = np.argwhere(mask)

        min_i, min_j = coords.min(axis=0)
        max_i, max_j = coords.max(axis=0)

        cropped = new_img[min_i:max_i+1, min_j:max_j+1]

        return cropped

    def translate(self, img, dx, dy):
        """
        Translação com expansão de canvas.
        dx: deslocamento horizontal (+ = direita, - = esquerda)
        dy: deslocamento vertical (+ = baixo, - = cima)
        Retorna imagem transladada sem bordas pretas.
        """
        h, w = img.shape[:2]

        new_h = h + abs(dy)
        new_w = w + abs(dx)

        if img.ndim == 3:
            new_img = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
        else:
            new_img = np.zeros((new_h, new_w), dtype=img.dtype)

        # offsets corretos
        off_y = max(dy, 0)
        off_x = max(dx, 0)

        # posição onde a imagem será colocada
        start_y = off_y
        end_y = off_y + h

        start_x = off_x
        end_x = off_x + w

        new_img[start_y:end_y, start_x:end_x] = img

        return new_img

    def rotate(self, img, angle_deg):
        """Rotação em torno do centro."""
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        M = self.inv_rot_matrix(angle_deg, center)
        return self.transformation(img, M)

    def scale(self, img, sx, sy):
        """Escala da imagem."""
        M = self.inv_scale_matrix(sx, sy, img.shape)
        return self.transformation(img, M)