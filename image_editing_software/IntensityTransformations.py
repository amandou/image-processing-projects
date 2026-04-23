import imageio.v3 as iio
import matplotlib.pyplot as plt
import numpy as np

class IntensityTransformations:
    def inverse(self, z):
      return 255 - z
    
    def negative(self, z):
      return  1-z
    
    def mod_transformation(self, z, a=30, b=200, c=0, d=250):
        z = z.astype(float)
        z = (z-a)*((d-c)/(b-a)) + c
        z = np.clip(z, 0, 255)
        return z.astype(np.uint8)        

    def log_transformation(self, z):
        z = z.astype(float)
        c = 255/(np.log(255+1))
        z = c * np.log(1+z)
        return z.astype(np.uint8)

    def gamma_transformation(self, z, gamma=2.2):
        z = z.astype(float)
        z = z ** gamma
        z = z * 255/(255**gamma)
        return z.astype(np.uint8)

    def limiar_transformation(self, z, L):
        z[z > L] = 255
        z[z < L] = 0
        return z

