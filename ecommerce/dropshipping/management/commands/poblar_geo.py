import unicodedata

# --- Normalización fuera de la clase ---
def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()


from django.core.management.base import BaseCommand
import csv
from dropshipping.models import Country, State, City

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos geográficos desde un CSV'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, help='Ruta al archivo CSV con ciudades')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv']

        print("Insertando ciudades...")
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country_name = row['country'].strip()
                state_name = row['admin_name'].strip()
                city_name = row['city'].strip()

                # Obtener o crear país
                country, _ = Country.objects.get_or_create(name=country_name)

                # Normalizamos estado para buscarlo
                normalized_state_name = normalize(state_name)
                states = State.objects.filter(country=country)
                matched_states = [s for s in states if normalize(s.name) == normalized_state_name]

                if matched_states:
                    state = matched_states[0]
                else:
                    print(f"❌ No se encontró el estado '{state_name}' en el país '{country_name}'")
                    continue

                # Crear ciudad si no existe
                City.objects.get_or_create(name=city_name, state=state)
