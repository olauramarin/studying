import numpy as np
import os
import PIL
import matplotlib.pyplot as plt

folder = "images"
all_images = []

for cdfile_name in os.listdir(folder):
    image_path = os.path.join(folder, file_name)
    image_array = np.array(PIL.Image.open(image_path)) / 255.0
    flattened = image_array.flatten()
    all_images.append(flattened)
      
images_array = np.array(all_images)

print ("Images array:", images_array)

print ("shape:",images_array.shape)


mean_images = np.mean(images_array, axis = 0)
print ("mean images:", mean_images)


normalized_images = images_array - mean_images
print ("normalized_images array:",normalized_images)

W = np.load("coefs.npy")   
b = np.load("bias.npy")  

X = normalized_images

logit = X @ W + b

print("X:", X.shape, "W:", W.shape, "b:", b.shape)
print("B:", b)

exp_logit = np.exp(logit)
y_hat = exp_logit / np. sum(exp_logit, axis=1, keepdims=True)

print ("exp_logit:", exp_logit)
print ("y_hat:", y_hat)
print("y_hat shape:", y_hat.shape)     


y_true = np.array ([0, 0, 1, 1, 2, 2, 3, 3])

y_pred = [np.random.choice(4, p=dist) for dist in y_hat]

print ("y_pred:",y_pred)

def accuracy_score(y_true, y_pred):
    n = len(y_true)
    ret = 0
    for i in range(n):
        if y_pred[i] == y_true[i]:
            ret = ret + 1
    return ret / n
    
accuracy = accuracy_score(y_true,y_pred)

print ("Accuracy score:", accuracy)

labels = {
    0: "Cat",
    1: "Dog",
    2: "Frog",
    3: "Horse"
}

predicted_labels = [labels[pred] for pred in y_pred]
true_labels = [labels[true] for true in y_true]

print("True | Pred")
for i in range(len(y_true)):
    print(f"{true_labels[i]} | {predicted_labels[i]}")
    
    


mean_image = mean_images.reshape(64, 64, 3)
mean_image = mean_image * 255
mean_image = mean_image.astype(np.uint8)

plt.title ("Mean Image")
plt.imshow(mean_image)  
plt.axis ("off")
plt.show()
    
