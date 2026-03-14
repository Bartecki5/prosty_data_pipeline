# 1. Bierzemy z internetu czystego, lekkiego Pythona (nasz fundament)
FROM python:3.10-slim 

# 2. Tworzymy wewnątrz kontenera folder /app i do niego wchodzimy
WORKDIR /app

# 3. Kopiujemy naszą "listę zakupów" z Twojego komputera do kontenera
COPY requirements.txt .

# 4. Uruchamiamy instalację bibliotek z listy
RUN pip install -r requirements.txt 

# 5. Kopiujemy Twój skrypt Pythona do kontenera
COPY pobierz_pogode_auto.py .

# 6. Mówimy Dockerowi: "Jak już zbudujesz pudełko i je uruchomisz, wpisz tę komendę"
CMD ["python","-u","pobierz_pogode_auto.py"]
