import requests
import psycopg2 #tlumacz python - bazy danych
import time

#adres api dla pzn
url = "https://api.open-meteo.com/v1/forecast?latitude=52.4069&longitude=16.9299&current_weather=true"

#wysylamy zapytanie
odpowiedz = requests.get(url)

#zmieniamy surową odp w czytelny slownik pythona 
dane = odpowiedz.json()

#print("Dane z api: ")
#print(dane)
aktualna_pogoda = dane['current_weather']
temperatura = aktualna_pogoda['temperature']
wiatr = aktualna_pogoda['windspeed']
czas = aktualna_pogoda['time']

#print(f"Czas pomiaru: {czas}")
#print(f"Temperatura: {temperatura} °C")
#print(f"Prędkość wiatru: {wiatr} km/h")

#łączenie z bazą danych dockera

polaczenie = psycopg2.connect(
    host="localhost",   #baza jest na naszym kompie
    port="5433",        #nasz port
    database="pogoda_db", #nazwa bazy z pliku .yml
    user="bartek",  #uzytkownik 
    password="haslo"    #haslo
)

# kursor to ramie robota, które wykonuje nasze polecenia wew bazy
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

#zatwierdzenie zmian
polaczenie.commit()

#sprzatanie
kursor.close()
polaczenie.close()

print("Dane w bazie")