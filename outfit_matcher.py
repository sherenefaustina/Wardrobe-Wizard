import cv2
import numpy as np
from sklearn.cluster import KMeans

def analyze_clothing(image_path, k=3):
    # Load the image and convert it to RGB
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (200, 200))  # Resize for consistency

    # Reshape image to a list of pixels
    pixels = image.reshape((-1, 3))

    # Use KMeans to find dominant colors
    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(pixels)

    # Find the most dominant cluster center (color)
    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    dominant_index = np.argmax(counts)
    dominant_color = kmeans.cluster_centers_[dominant_index].astype(int)

    # Match logic
    rgb = tuple(dominant_color)
    suggestion = match_colors(rgb)

    return {
        "dominant_color": rgb,
        "style_tip": suggestion
    }
def match_colors(rgb):
    r, g, b = rgb
    if r > 200 and g > 200 and b > 200:
        return "White detected 🤍 – Pair it with bold blacks, dark denim, or vibrant accessories for a chic contrast!"
    elif r > g and r > b:
        return "Reddish tone ❤️ – Goes well with cool colors like navy, black, or even soft pinks!"
    elif g > r and g > b:
        return "Greenish shade 💚 – Match it with beige, browns, or floral prints for a calm, earthy vibe."
    elif b > r and b > g:
        return "Blue detected 💙 – Looks amazing with whites, greys, or soft yellows for a breezy look."
    else:
        return "Neutral/Mixed tone 🧥 – You can rock it with pastels or denim for a versatile style!"

