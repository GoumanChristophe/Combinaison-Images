from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/combine', methods=['POST'])
def combine():
    image_files = request.files.getlist('image')
    image_paths = []

    # Enregistrer les images téléchargées et obtenir leurs chemins d'accès
    for file in image_files:
        filename = file.filename
        file.save(filename)
        image_paths.append(filename)

    # Combiner les images
    combined_image = combine_images(image_paths)

    # Enregistrer l'image combinée
    combined_image_path = 'static/uploads/combined_image.png'
    combined_image.save(combined_image_path)

    # Afficher l'image combinée sur la page
    return render_template('index.html', image_path=combined_image_path)

def combine_images(image_paths):
    # Ouvrir la première image pour obtenir les dimensions
    first_image = Image.open(image_paths[0])
    image_width, image_height = first_image.size

    # Calculer les dimensions de l'image finale combinée
    columns = 9
    rows = -(-len(image_paths) // columns)  # Calcul de l'arrondi supérieur
    combined_width = image_width * columns
    combined_height = image_height * rows

    # Créer une nouvelle image avec les dimensions calculées et le mode RGBA
    combined_image = Image.new('RGBA', (combined_width, combined_height))

    # Parcourir les images et les copier dans l'image combinée
    for i, image_path in enumerate(image_paths):
        image = Image.open(image_path)
        # Calculer les coordonnées de l'image dans l'image combinée
        x = (i % columns) * image_width
        y = (i // columns) * image_height
        # Copier l'image dans l'image combinée
        combined_image.paste(image, (x, y))

    return combined_image

if __name__ == '__main__':
    app.run()