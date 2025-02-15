import json
import os
import shutil
import tempfile

from django.http import JsonResponse

from config.settings import MEDIA_ROOT
from main.core.load_data.add_data import add_species, add_photos
from main.core.load_data.get_data import get_info, get_all_species_data
from main.core.logger.logger import logger
from main.models.photo import Photos
from main.models.species import Species

VIGNETTE_PATH = os.path.join(MEDIA_ROOT, 'main/images/vignettes')
SMALL_PATH = os.path.join(MEDIA_ROOT, 'main/images/small')

def upload_images(request):
    if request.method == "POST":
        images = []
        if "images" in request.FILES:
            images = request.FILES.getlist("images")
        image_to_delete = json.loads(request.POST.get("imageToDelete"))
        metadata = json.loads(request.POST.get("metadata"))

        results = []
        filepaths = []

        if len(metadata) > 0:
            temp_path = tempfile.mkdtemp()
            for image, meta in zip(images, metadata):
                # Ajouter le hash aux résultats
                datetime = ""
                if 'datetime' in meta:
                    datetime = meta['datetime']
                results.append({
                    "file_name": image.name,
                    "old_hash": meta['hash'],
                    "path": meta['filepath'],
                    "datetime": datetime,
                })
                filepaths.append((save_images(image, meta['filepath'], temp_path), datetime, meta['hash']))
            add_photos_in_base(filepaths, temp_path)
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)

        delete_images(image_to_delete)

        return JsonResponse({"images": results, "imageToDelete": image_to_delete})

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_latin_name(image_path):
    return " ".join(os.path.splitext(os.path.basename(image_path))[0].split(" ")[:2])


def delete_images(images_to_delete):
    for image_key in images_to_delete:
        try:
            image_path, image_hash = image_key.split(":")
            latin_name = get_latin_name(image_path)

            Photos.objects.filter(hash=image_hash).delete()
            specie_id = Species.objects.filter(latin_name=latin_name).values_list('id', flat=True).first()
            if specie_id and not Photos.objects.filter(specie_id=specie_id).exists():
                    Species.objects.filter(id=specie_id).delete()

            image_small = os.path.join(SMALL_PATH, image_path)
            image_vignette = os.path.join(VIGNETTE_PATH, image_path)
            delete_file_with_permission_check(image_small)
            delete_file_with_permission_check(image_vignette)
        except Exception as e:
            logger.error(f"Failed to delete image {image_key}")
            logger.error(e)


def delete_file_with_permission_check(file_path):
    try:
        if os.path.exists(file_path):
            if os.access(file_path, os.W_OK):
                os.remove(file_path)
                logger.info(f"Le fichier {file_path} a été supprimé avec succès.")
            else:
                logger.warning(f"Permissions insuffisantes pour supprimer le fichier {file_path}.")
        else:
            logger.warning(f"Le fichier {file_path} n'existe pas.")
    except Exception as e:
        logger.error(f"Erreur : {e}")


def save_images(image, filepath, temp_path):
    image_small = os.path.join(temp_path, filepath)
    save_image(image, image_small)
    return image_small

def create_missing_directories_in_media(filename):
    full_path = os.path.dirname(filename)
    try:
        os.makedirs(full_path, exist_ok=True)
        return full_path
    except Exception as e:
        logger.error(f"Erreur lors de la création du dossier {full_path} : {e}")
        return None

def save_image(file, filepath):
    create_missing_directories_in_media(filepath)
    with open(filepath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def add_photos_in_base(filepaths, temp_path):
    info_photo = get_dataset_from_images_path(filepaths, temp_path)
    latin_name_list = list({value['latin_name'] for value in info_photo})
    info_species = get_all_species_data(latin_name_list)
    add_species(info_species)
    add_photos(info_photo)


def get_dataset_from_images_path(images_path, path_to_remove) -> list[dict[str, str]]:
    logger.info(f"Nombre d'images {len(images_path)}")
    info_photo = []
    i = 0
    for images_data in images_path:
        (image_path, datetime, image_hash) = images_data
        try:
            photo = get_info(image_path, path_to_remove, datetime, image_hash)
            info_photo.append(photo)
        except Exception as e:
            logger.error(e)

        logger.info(f"image {i}")
        i += 1
    return info_photo
