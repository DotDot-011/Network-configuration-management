FROM python:3.9-bullseye

WORKDIR /usr/src/app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]