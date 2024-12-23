from django.core.exceptions import ValidationError
from django.db import transaction
from main.core.logger.logger import logger
from main.models.species import Species

@transaction.atomic
def add_data(value: list[dict[str, str]]) -> None:
    objects = []
    for row in value:
        species = Species(
            latin_name=row["nom latin"],
            genus=row["genre"],
            species=row["espèce"],
            french_name=row["nom français"],
            kingdom=row["règne"],
            class_field=row["classe"],
            category=row["catégorie"],
            year=row["année"],
            day=row["jour"],
            continent=row["continent"],
            country=row["pays"],
            region=row["région"],
            place=row["lieu"],
            photo=row["photo"],
            thumbnail=row["vignette"],
            note=row["note"],
        )
        try:
            species.full_clean()  # Validation avant création
            objects.append(species)
        except ValidationError as e:
            logger.error(f"Erreur de validation pour {row['nom latin']}: {str(e)}")

    if objects:
        Species.objects.bulk_create(objects)