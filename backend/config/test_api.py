import requests
import json

# URL de base de l'API
BASE_URL = "http://127.0.0.1:8000/api"

# Variables globales pour stocker les tokens
access_token = None
refresh_token = None

def test_register():
    """Test de l'inscription d'un nouvel utilisateur"""
    print("\n=== TEST: Inscription ===")
    
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "password2": "TestPassword123!"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        global access_token, refresh_token
        result = response.json()
        access_token = result['access']
        refresh_token = result['refresh']
        print(f"\n✅ Token d'accès sauvegardé")
    
    return response

def test_login():
    """Test de la connexion"""
    print("\n=== TEST: Connexion ===")
    
    url = f"{BASE_URL}/auth/login/"
    data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        global access_token, refresh_token
        result = response.json()
        access_token = result['access']
        refresh_token = result['refresh']
        print(f"\n✅ Token d'accès sauvegardé")
    
    return response

def test_profile():
    """Test de récupération du profil"""
    print("\n=== TEST: Profil utilisateur ===")
    
    url = f"{BASE_URL}/auth/profile/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response

def test_generate_json():
    """Test de génération de données en JSON"""
    print("\n=== TEST: Génération JSON ===")
    
    url = f"{BASE_URL}/generate/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "schema": {
            "nom": "name",
            "email": "email",
            "telephone": "phone_number",
            "pays": "country",
            "entreprise": "company"
        },
        "rows": 10,
        "format": "json",
        "save_schema": True,
        "schema_name": "Schéma Test Utilisateurs"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    # Pour JSON, on peut afficher le contenu
    if response.status_code == 200:
        print("✅ Fichier généré avec succès!")
        print("\nAperçu des données:")
        try:
            data = json.loads(response.text)
            for i, item in enumerate(data[:3]):  # Affiche les 3 premiers
                print(f"\nEnregistrement {i+1}:")
                print(json.dumps(item, indent=2, ensure_ascii=False))
        except:
            print(response.text[:500])  # Affiche les 500 premiers caractères
    else:
        print(f"❌ Erreur: {response.text}")
    
    return response

def test_generate_csv():
    """Test de génération de données en CSV"""
    print("\n=== TEST: Génération CSV ===")
    
    url = f"{BASE_URL}/generate/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "schema": {
            "prenom": "first_name",
            "nom": "last_name",
            "email": "email",
            "ville": "city"
        },
        "rows": 5,
        "format": "csv"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ CSV généré avec succès!")
        print("\nContenu du CSV:")
        print(response.text)
    else:
        print(f"❌ Erreur: {response.text}")
    
    return response

def test_schemas_list():
    """Test de récupération de la liste des schémas"""
    print("\n=== TEST: Liste des schémas ===")
    
    url = f"{BASE_URL}/schemas/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response

def test_history():
    """Test de récupération de l'historique"""
    print("\n=== TEST: Historique des datasets ===")
    
    url = f"{BASE_URL}/history/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response

def run_all_tests():
    """Lance tous les tests dans l'ordre"""
    print("🚀 Démarrage des tests de l'API SyntheticData")
    print("=" * 60)
    
    # Inscription (ou connexion si l'user existe déjà)
    response = test_register()
    if response.status_code != 201:
        print("\n⚠️ L'utilisateur existe déjà, tentative de connexion...")
        test_login()
    
    # Vérifie que le token est bien récupéré
    if not access_token:
        print("\n❌ Impossible de continuer sans token d'authentification")
        return
    
    # Tests des endpoints
    test_profile()
    test_generate_json()
    test_generate_csv()
    test_schemas_list()
    test_history()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés!")

if __name__ == "__main__":
    run_all_tests()