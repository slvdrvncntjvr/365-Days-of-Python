from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def extract_colors(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.convert("RGB")
    image = image.resize((200, 200))
    data = np.array(image)
    data = data.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(data)
    colors = kmeans.cluster_centers_.astype(int)
    return colors.tolist()

def get_palette_image(colors, swatch_size=50):
    palette = Image.new("RGB", (swatch_size * len(colors), swatch_size))
    for i, color in enumerate(colors):
        swatch = Image.new("RGB", (swatch_size, swatch_size), tuple(color))
        palette.paste(swatch, (i * swatch_size, 0))
    return palette

def rgb_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(*color)
