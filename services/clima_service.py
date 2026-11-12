
import math
import requests


class ClimaService:
    def consultar_clima(self, latitud, longitud):
        # Validar las coordenadas antes de consultar la API
        try:
            if isinstance(latitud, bool) or isinstance(longitud, bool):
                raise ValueError("Las coordenadas deben ser números.")

            latitud = float(latitud)
            longitud = float(longitud)

            if not math.isfinite(latitud) or not math.isfinite(longitud):
                raise ValueError("Las coordenadas deben ser finitas.")

            if not (-90 <= latitud <= 90):
                raise ValueError("La latitud debe estar entre -90 y 90.")

            if not (-180 <= longitud <= 180):
                raise ValueError("La longitud debe estar entre -180 y 180.")

        except (ValueError, TypeError) as error:
            print(f"[ERROR DE VALIDACIÓN] {error}")
            return None

        url = "https://api.open-meteo.com/v1/forecast"

        parametros = {
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto"
        }

        try:
            respuesta = requests.get(
                url, params=parametros, timeout=10
            )
            respuesta.raise_for_status()

            datos = respuesta.json()
            clima = datos["current"]

            return {
                "temperatura": clima["temperature_2m"],
                "humedad": clima["relative_humidity_2m"],
                "viento": clima["wind_speed_10m"]
            }

        except (requests.RequestException, ValueError, KeyError, TypeError) as error:
            print(f"Error al consultar el clima: {error}")
            return None
