import csv
import os
import pycountry
from django.core.management.base import BaseCommand
from geonamescache import GeonamesCache
from dropshipping.models import Country, State, City

# Lista de países de habla hispana + EE.UU.
TARGET_COUNTRIES = {
    "AR", "BO", "CL", "CO", "CR", "CU", "DO", "EC", "SV",
    "GQ", "GT", "HN", "MX", "NI", "PA", "PY", "PE", "PR",
    "ES", "UY", "VE", "US"
}


class Command(BaseCommand):
    help = "Pobla la base de datos con países, estados y ciudades para países hispanohablantes y EE.UU."

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            help='Ruta al archivo CSV con ciudades (opcional). Ej: --csv worldcities.csv'
        )

    def handle(self, *args, **options):
        self.populate_countries_and_states()
        csv_path = options['csv']
        if csv_path and os.path.isfile(csv_path):
            self.populate_cities(csv_path)
        else:
            self.stdout.write(self.style.WARNING("No se insertaron ciudades. Usa --csv [ruta al archivo] si deseas cargarlas."))

    def populate_countries_and_states(self):
        self.stdout.write("Insertando países y estados...")
        for country_code in TARGET_COUNTRIES:
            country_obj = pycountry.countries.get(alpha_2=country_code)
            if not country_obj:
                continue

            country, _ = Country.objects.get_or_create(
                code=country_obj.alpha_2,
                defaults={"name": country_obj.name}
            )

            subdivisions = list(pycountry.subdivisions.get(country_code=country_code)) or []

            for subdivision in subdivisions:
                State.objects.get_or_create(
                    code=subdivision.code,
                    name=subdivision.name,
                    country=country
                )

        self.stdout.write(self.style.SUCCESS("✔ Países y estados insertados."))

    def populate_cities(self, csv_path):
        self.stdout.write(f"Insertando ciudades desde {csv_path}...")
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            inserted = 0
            for row in reader:
                if row['iso2'] not in TARGET_COUNTRIES:
                    continue

                country_code = row['iso2']
                state_name = row['admin_name']
                city_name = row['city']
                postal_code = row.get('postal', '0000')

                try:
                    country = Country.objects.get(code=country_code)
                    state = State.objects.filter(name__iexact=state_name, country=country).first()
                    if not state:
                        continue

                    City.objects.get_or_create(
                        name=city_name,
                        postal_code=postal_code or '0000',
                        state=state
                    )
                    inserted += 1
                except Country.DoesNotExist:
                    continue

        self.stdout.write(self.style.SUCCESS(f"✔ {inserted} ciudades insertadas correctamente."))
