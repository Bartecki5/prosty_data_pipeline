import requests
import psycopg2 
import time


url = "https://api.open-meteo.com/v1/forecast?latitude=52.4069&longitude=16.9299&current_weather=true"

odpowiedz = requests.get(url)


dane = odpowiedz.json()


aktualna_pogoda = dane['current_weather']
temperatura = aktualna_pogoda['temperature']
wiatr = aktualna_pogoda['windspeed']
czas = aktualna_pogoda['time']

#print(f"Czas pomiaru: {czas}")
#print(f"Temperatura: {temperatura} °C")
#print(f"Prędkość wiatru: {wiatr} km/h")

#łączenie z bazą danych dockera

polaczenie = psycopg2.connect(
    host="localhost",   
    port="5433",        
    database="pogoda_db", 
    user="bartek",   
    password="haslo"   
)


kursor = polaczenie.cursor()

tworzenie_tabeli_sql="""
CREATE TABLE IF NOT EXISTS pomiary_pogody (
   id SERIAL PRIMARY KEY,
   czas_pomiaru VARCHAR(50),
   temperatura FLOAT,
   wiatr FLOAT 
);
"""

kursor.execute(tworzenie_tabeli_sql)

wstawianie_danych_sql = """ 
INSERT INTO pomiary_pogody (czas_pomiaru, temperatura, wiatr)
VALUES (%s, %s , %s); 
"""
kursor.execute(wstawianie_danych_sql,(czas,temperatura,wiatr))


polaczenie.commit()

kursor.close()
polaczenie.close()

print("Dane w bazie")
