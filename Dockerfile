FROM python:3.6.10

# virtualenv and dependencies
RUN python3 -m venv /opt/venv
COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Program
COPY ./app /app
RUN chmod u+x /app/benford_app.py
CMD . /opt/venv/bin/activate && /app/benford_app.py