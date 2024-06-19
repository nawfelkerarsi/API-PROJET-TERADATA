# Utilisation de l'image de base Python officielle
FROM python:3.10-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'application dans le conteneur
COPY . /app

# Exposition du port utilisé par FastAPI
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
