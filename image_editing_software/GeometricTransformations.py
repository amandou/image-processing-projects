import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np

class GeometricTransformationsOperations:
    def inv_rot_matrix(theta):
        return np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]])
    
    def inv_scale_matrix(si, sj):
        return np.array([
            [1.0 / si, 0, 0],
            [0, 1.0 / sj, 0],
            [0, 0, 1]])
    
    def inv_translation_matrix(ti, tj):
        return np.array([
            [1, 0, -ti],
            [0, 1, -tj],
            [0, 0, 1]])
    

    def transformation(self, img, operation):
        nimg = np.zeros_like(img)
        h, w, _ = img.shape
        
        M = operation
    
        for i in range(h):
            for j in range(w):
                p_linha = np.array([i, j, 1])
                p = M @ p_linha

                i_p = int(np.round(p[0]))
                j_p = int(np.round(p[1]))

                if(i_p < h and i_p >= 0 and j_p < w and j_p >= 0):
                    new_img[i,j] = img[i_p, j_p]

        return new_img   
    
    def translate(self, img, dx, dy):
        """Translação da imagem."""
        M = self.inv_translation_matrix(dx, dy)
        return self.transformation2(img, M)

    def rotate(self, img, angle_deg):
        """Rotação em torno do centro."""
        h, w = img.shape[:2]
        center = (h // 2, w // 2)
        M = self.inv_rot_matrix(angle_deg, center)
        return self.transformation2(img, M)

    def scale(self, img, sx, sy):
        """Escala da imagem."""
        M = self.inv_scale_matrix(sx, sy)
        return self.transformation2(img, M)