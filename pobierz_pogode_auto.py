import requests
import psycopg2
import time  

polaczenie = psycopg2.connect(
    host="moja_baza_danych",
    port="5432",
    database="pogoda_db",
    user="bartek",
    password="haslo"
)
kursor = polaczenie.cursor()


kursor.execute("""
CREATE TABLE IF NOT EXISTS pomiary_pogody (
    id SERIAL PRIMARY KEY,
    czas_pomiaru VARCHAR(50),
    temperatura FLOAT,
    wiatr FLOAT
);
""")
polaczenie.commit()

print("Rozpoczynam automatyczne pobieranie. Wciśnij Ctrl+C w terminalu, żeby zatrzymać!\n")

url = "https://api.open-meteo.com/v1/forecast?latitude=52.4069&longitude=16.9299&current_weather=true"

while True:
    try:
        
        odpowiedz = requests.get(url)
        dane = odpowiedz.json()
        
        aktualna_pogoda = dane['current_weather']
        temperatura = aktualna_pogoda['temperature']
        wiatr = aktualna_pogoda['windspeed']
        czas = aktualna_pogoda['time']
        
        
        wstawianie_danych_sql = "INSERT INTO pomiary_pogody (czas_pomiaru, temperatura, wiatr) VALUES (%s, %s, %s);"
        kursor.execute(wstawianie_danych_sql, (czas, temperatura, wiatr))
        polaczenie.commit() 
        
        print(f"[{czas}] Automatyczny zapis: Temp: {temperatura}°C | Wiatr: {wiatr}km/h")
        
        #api aktualizuje się dluzej ale dla przykladu
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\nPrzerwano działanie programu! Kończę pracę i sprzątam...")
        break 


kursor.close()
polaczenie.close()
print("Rozłączono z bazą danych.")