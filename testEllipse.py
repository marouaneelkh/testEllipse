import requests
import folium
from folium.plugins import MarkerCluster

# Clé API
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"
contract_name = "valence"  # Remplacez par le nom de votre contrat JCDecaux

# Static Data
def get_static_bike_data():
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des données statiques :", response.status_code)
        return None

# Dynamic data refresh every 1min
def get_dynamic_bike_data():
    url = f"https://api.jcdecaux.com/vls/v3/stations?contract={contract_name}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des données dynamiques :", response.status_code)
        return None

# Créer la carte
def create_map(static_data, dynamic_data):
    # Centre de la carte (Paris par défaut)
    center = [48.8566, 2.3522]
    # Créer la carte
    map = folium.Map(location=center, zoom_start=12)
    # Groupe de marqueurs
    marker_cluster = MarkerCluster().add_to(map)
    # Ajouter les marqueurs pour chaque station
    for station in static_data:
        name = station["name"]
        latitude = station["position"]["latitude"]
        longitude = station["position"]["longitude"]
        # Trouver les données dynamiques correspondantes
        dynamic_station = next((x for x in dynamic_data if x["number"] == station["number"]), None)
        if dynamic_station:
            bikes = dynamic_station["mainStands"]["availableBikes"]
        else:
            bikes = "N/A"
        total_stands = station["bike_stands"]
        # Informations sur la station
        popup_text = f"<b>{name}</b><br> Vélos disponibles : {bikes}/{total_stands}"
        # Ajouter le marqueur à la carte
        folium.Marker(location=[latitude, longitude], popup=popup_text).add_to(marker_cluster)
    return map

# Mettre à jour les données et la carte
def update_map():
    static_data = get_static_bike_data()
    dynamic_data = get_dynamic_bike_data()
    if static_data and dynamic_data:
        map = create_map(static_data, dynamic_data)
        map.save("bike_stations.html")
        print("Carte mise à jour avec succès.")

# Fonction principale
def main():
    update_map()

if __name__ == "__main__":
    main()
