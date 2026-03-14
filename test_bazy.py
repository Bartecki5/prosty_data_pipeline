import psycopg2 

polaczenie = psycopg2.connect(
    host="localhost",
    port="5433",
    database="pogoda_db",
    user="bartek",
    password="haslo"
)

kursor = polaczenie.cursor()

#piszemy zapytanie które pobiera dane
zapytanie_sql = "SELECT * FROM pomiary_pogody;"

#wykonujemy zapytanie
kursor.execute(zapytanie_sql)

#pobieramy wyniki które znalazł kursor
pobrane_dane = kursor.fetchall()

#wyświetlanie
for wiersz in pobrane_dane:

    id_pomiaru = wiersz[0]
    czas = wiersz[1]
    temp = wiersz[2]
    wiatr = wiersz[3]

    print(f"Rekord nr {id_pomiaru}: Dnia {czas} było {temp}°C, a wiatr wiał z prędkością {wiatr} km/h")

#czyszenie
kursor.close()
polaczenie.close()