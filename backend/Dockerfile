FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt flask-cors

COPY backend/ ./backend/

# Ensure uploads directory is available
RUN mkdir -p /uploads

ENV PYTHONPATH=/app
ENV FLASK_APP=backend/app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
