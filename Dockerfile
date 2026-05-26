FROM python:3.11-slim

# Install app
COPY . /usr/app
WORKDIR /usr/app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Battlesnake
CMD [ "python", "main.py" ]
