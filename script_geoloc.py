import requests
import urllib.parse

#prueba Martin Leiva

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "be2e37b6-e48a-49cf-9885-e530095da178"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data.get("hits", [])) > 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""
        
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(country) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
    return json_status, lat, lng, new_loc

while True:
    print("\n=================================================")
    loc1 = input("Origen (ingrese 's' o 'salir' para finalizar): ")
    if loc1.lower() in ["s", "salir", "quit", "q"]:
        print("¡Programa finalizado!")
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destino (ingrese 's' o 'salir' para finalizar): ")
    if loc2.lower() in ["s", "salir", "quit", "q"]:
        print("¡Programa finalizado!")
        break
    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        
        # Parámetro 'locale': 'es' para solicitar las instrucciones en español
        paths_url = route_url + urllib.parse.urlencode({"key": key, "locale": "es"}) + op + dp
        
        response_route = requests.get(paths_url)
        paths_status = response_route.status_code
        paths_data = response_route.json()
        
        print("Estado de la API de Enrutamiento: " + str(paths_status) + "\nURL de la API de Enrutamiento:\n" + paths_url)

        print("=================================================")
        print("Indicaciones de viaje desde " + orig[3] + " hasta " + dest[3])
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            # Valores formateados a dos decimales (.2f)
            print("Distancia recorrida: {0:.2f} millas / {1:.2f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            print("Narrativa del viaje (Paso a paso):")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                # Formato de distancia en paso a paso a dos decimales (.2f)
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(path, distance / 1000, (distance / 1000) / 1.61))
            print("=============================================")
        else:
            print("Error al obtener la ruta. Mensaje de la API:", paths_data.get("message", "Error desconocido"))
