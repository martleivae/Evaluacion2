# Evaluacion2 - Software de Geolocalización en Python

Este repositorio contiene un script en Python desarrollado para interactuar con la API de enrutamiento y geocodificación de **GraphHopper**.

## Descripción del Proyecto
El script `script_geoloc.py` permite al usuario ingresar una ciudad de origen y una de destino para obtener:
- Distancia total del viaje (en millas y kilómetros, con un máximo de 2 decimales).
- Tiempo estimado de duración del trayecto (`HH:MM:SS`).
- Indicaciones narradas paso a paso traducidas completamente al español.

## Requisitos
- Python 3.x
- Librería `requests` (instalable con `pip install requests`)

## Instrucciones de Ejecución
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/martleivae/Evaluacion2.git
   cd Evaluacion2
