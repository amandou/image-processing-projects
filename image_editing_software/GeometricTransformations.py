import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np

class GeometricTransformations:
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
                    nimg[i,j] = img[i_p, j_p]

        return nimg