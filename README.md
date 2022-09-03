# Benford's Law Web App

Built with Flask, designed to extract data from a flat file and used to determine if dataset fits to Benford's law

## Instructions:
1. Clone the repo
2. Commence virtual environment with `python -m venv venv`
3. Activate venv with `source venv/bin/activate`
4. update pip with `pip install --upgrade pip`
5. Install requirements with `python3 -m pip install -r requirements.txt`
6. Run web app locally with `python benford_app.py`
7. View site on `http://127.0.0.1:5000/` with port 5000 open
8. Enjoy!

## Instructions (Docker):
1. Pull the Docker image with `docker push jguiel/benford_app:tagname:latest`
2. Run docker container with `docker run -p 5000:5000 -d benford_app`
3. Either:
   - `docker logs <sha256hash>` command+click `http://0.0.0.0:5000`
   - Enter `http://0.0.0.0:5000` into browser
4. Enjoy!
