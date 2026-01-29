# Python image use karein
FROM python:3.11

# Work directory set karein
WORKDIR /app

# Dependencies install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora code copy karein
COPY . .

# Gunicorn server ke saath Django start karein
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "motherscare_project.wsgi:application"]