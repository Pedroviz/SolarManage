import os
import requests

# URLs de imagens públicas de usinas solares como exemplo
image_urls = [
    "https://images.unsplash.com/photo-1509391366360-2e959784a276?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
    "https://images.unsplash.com/photo-1627328561499-a3584d4ee4f7?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
    "https://images.unsplash.com/photo-1466611653911-95081537e5b7?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
    "https://plus.unsplash.com/premium_photo-1661774910035-05257f7d73a6?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200",
    "https://images.unsplash.com/photo-1595437193398-f24279553f4f?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"
]

# Pasta para salvar as imagens
save_dir = "assets/images"
os.makedirs(save_dir, exist_ok=True)

# Baixar imagens
for i, url in enumerate(image_urls):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(save_dir, f"solar_plant_{i+1}.jpg")
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Imagem {i+1} baixada: {file_path}")
        else:
            print(f"Erro ao baixar imagem {i+1}: Status code {response.status_code}")
    except Exception as e:
        print(f"Erro ao baixar imagem {i+1}: {str(e)}")

print("Download concluído!")