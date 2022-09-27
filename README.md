# vesialue-back

Vesialueen inventointi-ilmoitus backend

- Production branch: main ![Tests](https://github.com/ohtuprojekti-2022/vesialue-back/actions/workflows/tests.yml/badge.svg?branch=main)
- Staging branch: staging ![Tests](https://github.com/ohtuprojekti-2022/vesialue-back/actions/workflows/tests.yml/badge.svg?branch=staging)

## Heroku
- [Staging](https://vesialue-back-staging.herokuapp.com)
- [Production](https://vesialue-back.herokuapp.com)

There are GitHub Actions building and pushing the Docker containers to Heroku on each commit to main and staging branches

## Installation
Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Provide environment variables by creating an `.env` file at the root of the project:
```bash
MONGO_URI=<MongoDB URI>
SECRET_KEY=<encryption key>
```

In the virtual environment, start the server from the root of the project by running:
```bash
FLASK_APP=src/app.py flask run
```

## Docker
### Building image
```docker build -t vesialue-back .```

### Running image locally
```docker run --rm -p 3000:3000 vesialue-back```
The service will be available at port 3000.

The port can be specified using the PORT environment variable
(used when running on Heroku). The default is 3000.

