# syntax=docker/dockerfile:1.7

# Autor: Filip Kwietniak
# Dockerfile dla części obowiązkowej 

# Używamy oficjalnego obrazu Pythona jako bazy do budowania i wersje slim aby zmiejszyć rozmiar obrazu
FROM python:3.12-slim AS builder

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app


# Kopiujemy NAJPIERW tylko requirements.txt
# Jeśli requirements.txt się nie zmieni,
# pip install nie będzie wykonywany ponownie przy kolejnych buildach.
COPY app/requirements.txt .

# Instalujemy zależności do osobnego katalogu /install
# --no-cache-dir    — nie zapisuje cache pip (mniejszy obraz)
# --prefix=/install — instaluje do /install zamiast globalnie
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS final

#Informacje zgodne ze standardem OCI
LABEL org.opencontainers.image.authors="Filip Kwietniak"
LABEL org.opencontainers.image.title="Weather App"
LABEL org.opencontainers.image.description="Aplikacja pogodowa  — Technologie Chmurowe Zadanie 1"
LABEL org.opencontainers.image.version="1.0.0"

# Ustawiamy zmienne środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Tworzymy niepriwilegowanego użytkownika aby zapewnic bezpieczenstwo
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Kopiujemy zainstalowane zależności z etapu builder
COPY --from=builder /install /usr/local

# Kopiujemy kod aplikacji
COPY app/ .

# Zmieniamy właściciela plików na appuser
RUN chown -R appuser:appuser /app

# Przełączamy się na niepriwilegowanego użytkownika
USER appuser

# Informujemy Docker że aplikacja nasłuchuje na porcie 8080
EXPOSE 8080


# Healthcheck — Docker co 30s sprawdza czy aplikacja żyje
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Uruchamiamy aplikację przez gunicorn
# -w 2          — 2 procesy robocze
# -b 0.0.0.0    — nasłuchuje na wszystkich interfejsach
# app:app       — moduł:obiekt Flask
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
