import requests
 
# URL sencilla y estable

url = "https://httpbin.org/get"
 
# Hacemos la solicitud

response = requests.get(url)
 
# Validamos si la respuesta fue correcta (200 = OK)

print("Status code:", response.status_code)
 
# Mostramos el contenido en formato JSON

print("JSON de respuesta:", response.json())

 