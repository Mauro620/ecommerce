import unicodedata
import csv
from django.core.management.base import BaseCommand
from dropshipping.models import Country, State, City

# --- Normalización fuera de la clase ---
def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()

# --- Lista de países permitidos (idioma español + EEUU) ---
ALLOWED_COUNTRIES = {
    "Argentina", "Bolivia", "Chile", "Colombia", "Costa Rica", "Cuba", "Ecuador",
    "El Salvador", "España", "Guatemala", "Honduras", "México", "Nicaragua", "Panamá",
    "Paraguay", "Perú", "Puerto Rico", "República Dominicana", "Uruguay", "Venezuela",
    "Estados Unidos", "United States"
}

class Command(BaseCommand):
    help = 'Elimina y repuebla Países, Estados y Ciudades desde worldcities.csv'

    def handle(self, *args, **kwargs):
        csv_path = 'dropshipping/management/worldcities.csv'

        print("🧹 Borrando datos anteriores...")
        City.objects.all().delete()
        State.objects.all().delete()
        Country.objects.all().delete()

        print("📥 Cargando datos desde CSV...")

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                country_name = row['country'].strip()
                if country_name not in ALLOWED_COUNTRIES:
                    continue

                city_name = row['city'].strip()
                state_name = row.get('admin_name', '').strip()
                postal_code = row.get('postal', '00000').strip()
                country_code = row.get('iso2', '') or row.get('iso3', '')

                # Crear país
                country, _ = Country.objects.get_or_create(
                    name=country_name,
                    defaults={'code': country_code}
                )

                # Crear estado
                normalized_state = normalize(state_name)
                state = State.objects.filter(country=country).filter(name__iexact=state_name).first()

                if not state:
                    state = State.objects.create(
                        name=state_name or "Estado Desconocido",
                        code=normalized_state[:10].upper(),
                        country=country
                    )

                # Crear ciudad
                City.objects.get_or_create(
                    name=city_name,
                    postal_code=postal_code,
                    state=state
                )

                count += 1
                if count % 500 == 0:
                    print(f"  → {count} ciudades insertadas...")

        print(f"✅ Carga finalizada: {count} ciudades registradas.")
