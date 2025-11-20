from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename
import os
import webbrowser
import threading
from werkzeug.serving import make_server
import time
from datetime import datetime
import sys

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
COMBINED_FOLDER = 'static/combined'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMBINED_FOLDER, exist_ok=True)

# Variables pour l'arrêt automatique
last_activity_time = time.time()
INACTIVITY_TIMEOUT = 300  # 5 minutes en secondes
server_instance = None

@app.before_request
def track_activity():
    """Met à jour le timestamp de la dernière activité à chaque requête"""
    global last_activity_time
    last_activity_time = time.time()
    print(f"Activité détectée à {datetime.now().strftime('%H:%M:%S')}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/combine', methods=['POST'])
def combine():
    # Nettoyer tous les uploads précédents (sauf les images combinées)
    cleanup_uploaded_images()
    
    image_files = request.files.getlist('image')
    columns = int(request.form.get('columns', 9))  # Récupère le nombre de colonnes, 9 par défaut
    image_paths = []

    for file in image_files:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        image_paths.append(save_path)

    # Limiter les colonnes au nombre d'images pour éviter les espaces vides
    num_images = len(image_paths)
    original_columns = columns
    columns = min(columns, num_images)
    
    if original_columns > num_images:
        print(f"ℹ️  Colonnes ajustées: {original_columns} → {columns} (nombre d'images: {num_images})")

    combined_image = combine_images(image_paths, columns)
    
    # Générer un nom de fichier unique avec timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    combined_image_path = os.path.join(COMBINED_FOLDER, f'combined_image_{timestamp}.png')
    combined_image.save(combined_image_path)
    
    # Nettoyer les anciennes images combinées (garder seulement les 5 dernières)
    cleanup_old_combined_images()
    
    # Ajouter un paramètre timestamp pour forcer le rechargement du navigateur
    cache_buster = int(time.time())

    return render_template('index.html', image_path=combined_image_path, cache_buster=cache_buster)


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


def cleanup_old_combined_images():
    """Nettoie les anciennes images combinées, garde seulement les 5 dernières"""
    try:
        files = []
        for filename in os.listdir(COMBINED_FOLDER):
            if filename.startswith('combined_image_') and filename.endswith('.png'):
                filepath = os.path.join(COMBINED_FOLDER, filename)
                files.append((filepath, os.path.getmtime(filepath)))
        
        # Trier par date de modification (du plus ancien au plus récent)
        files.sort(key=lambda x: x[1])
        
        # Supprimer tous sauf les 5 derniers
        for filepath, _ in files[:-5]:
            os.remove(filepath)
            print(f"🗑️  Ancienne image combinée supprimée: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Erreur lors du nettoyage des images combinées: {e}")


def cleanup_uploaded_images():
    """Nettoie toutes les images uploadées avant chaque nouvelle combinaison"""
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f"🗑️  Upload supprimé: {filename}")
    except Exception as e:
        print(f"Erreur lors du nettoyage des uploads: {e}")


# --- VERSION PRO QUI MARCHE EN EXE ---

def monitor_inactivity():
    """Surveille l'inactivité et arrête le serveur si pas d'activité pendant 5 minutes"""
    global server_instance
    print(f"🕐 Surveillance d'inactivité activée (timeout: {INACTIVITY_TIMEOUT // 60} minutes)")
    
    while True:
        time.sleep(30)  # Vérifier toutes les 30 secondes
        
        inactive_time = time.time() - last_activity_time
        
        if inactive_time > INACTIVITY_TIMEOUT:
            print(f"\n⚠️  Aucune activité depuis {int(inactive_time // 60)} minutes")
            print("🛑 Arrêt automatique du serveur...")
            
            if server_instance:
                server_instance.shutdown()
            
            # Forcer l'arrêt complet de l'application
            time.sleep(1)
            os._exit(0)

def start_server():
    global server_instance
    server_instance = make_server("127.0.0.1", 5000, app)
    print("🚀 Serveur démarré sur http://127.0.0.1:5000")
    print(f"⏱️  Arrêt automatique après {INACTIVITY_TIMEOUT // 60} minutes d'inactivité")
    server_instance.serve_forever()


def open_browser():
    time.sleep(1)       # IMPORTANT : attendre que le serveur démarre
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    threading.Thread(target=monitor_inactivity, daemon=True).start()

    # Boucle non bloquante
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel du serveur")
        if server_instance:
            server_instance.shutdown()
        pass
