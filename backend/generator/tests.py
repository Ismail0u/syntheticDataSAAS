from services.data_generator import DataGenerator
from services.file_exporter import FileExporter

# Test de génération
generator = DataGenerator(locale='pt_BR')

schema = {
    "nom": "name",
    "email": "email",
    "pays": "country",
    "telephone": "phone_number",
    "entreprise": "company"
}

# Génère 5 lignes
data = generator.generate_dataset(schema, 5)

print("=== Données générées ===")
for item in data:
    print(item)

print("\n=== Export JSON ===")
print(FileExporter.to_json(data))

print("\n=== Export CSV ===")
print(FileExporter.to_csv(data))


print("\n=== Export SQL ===")
print(FileExporter.to_sql(data))

