from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename
import os
import webbrowser
import threading
from werkzeug.serving import make_server
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/combine', methods=['POST'])
def combine():
    image_files = request.files.getlist('image')
    columns = int(request.form.get('columns', 9))  # Récupère le nombre de colonnes, 9 par défaut
    image_paths = []

    for file in image_files:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        image_paths.append(save_path)

    combined_image = combine_images(image_paths, columns)
    combined_image_path = os.path.join(UPLOAD_FOLDER, 'combined_image.png')
    combined_image.save(combined_image_path)

    return render_template('index.html', image_path=combined_image_path)


def combine_images(image_paths, columns=9):
    first_image = Image.open(image_paths[0])
    image_width, image_height = first_image.size

    rows = -(-len(image_paths) // columns)  # Division arrondie vers le haut

    combined_width = image_width * columns
    combined_height = image_height * rows

    combined_image = Image.new('RGBA', (combined_width, combined_height))

    for i, path in enumerate(image_paths):
        img = Image.open(path).convert("RGBA")
        x = (i % columns) * image_width
        y = (i // columns) * image_height
        combined_image.paste(img, (x, y), img)

    return combined_image


# --- VERSION PRO QUI MARCHE EN EXE ---

def start_server():
    server = make_server("127.0.0.1", 5000, app)
    server.serve_forever()


def open_browser():
    time.sleep(1)       # IMPORTANT : attendre que le serveur démarre
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()

    # Boucle non bloquante
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
