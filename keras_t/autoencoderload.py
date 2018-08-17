from keras.layers import Dense, Input
from keras.models import Sequential, load_model, Model
from keras.datasets import mnist
from keras.utils import np_utils
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image_size=28
(x_train, y_train),(x_test,y_test) = mnist.load_data()

x_train_2D = x_train.reshape(60000, 28*28).astype('float32')
x_test_2D = x_test.reshape(10000, 28*28).astype('float32')
x_train_norm=(x_train_2D/255.0)
x_test_norm=(x_test_2D/255.0)

autoencoder = load_model('autoecd.h5')



# Predict the Autoencoder output from corrupted test images
x_decoded = autoencoder.predict(x_test_norm)
x_decoded=x_decoded.reshape(10000,28,28)
x_test_norm=x_test_norm.reshape(10000,28,28)

# Display the 1st 8 corrupted and denoised images
rows, cols = 10, 30
num = rows * cols
imgs = np.concatenate([x_test_norm[:num], x_decoded[:num]])
imgs = imgs.reshape((rows * 2, cols, image_size, image_size))
imgs = np.vstack(np.split(imgs, rows, axis=1))
imgs = imgs.reshape((rows * 2, -1, image_size, image_size))
imgs = np.vstack([np.hstack(i) for i in imgs])
imgs = (imgs * 255).astype(np.uint8)
plt.figure()
plt.axis('off')
plt.title('Original images: top rows, '
          'Corrupted Input: middle rows, '
          'Denoised Input:  third rows')
plt.imshow(imgs, interpolation='none', cmap='gray')
Image.fromarray(imgs).save('corrupted_and_denoised.png')
plt.show()