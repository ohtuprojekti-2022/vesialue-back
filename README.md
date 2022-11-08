# vesialue-back

Vesialueen inventointi-ilmoitus backend

### Production branch: main
- ![Tests](https://github.com/ohtuprojekti-2022/vesialue-back/actions/workflows/heroku-prod.yml/badge.svg?branch=main)
- [![codecov](https://codecov.io/gh/ohtuprojekti-2022/vesialue-back/branch/main/graph/badge.svg?token=VF8NXG8KIG)](https://codecov.io/gh/ohtuprojekti-2022/vesialue-back)

### Staging branch: staging
- ![Tests](https://github.com/ohtuprojekti-2022/vesialue-back/actions/workflows/heroku-staging.yml/badge.svg?branch=staging)
- [![codecov](https://codecov.io/gh/ohtuprojekti-2022/vesialue-back/branch/staging/graph/badge.svg?token=VF8NXG8KIG)](https://codecov.io/gh/ohtuprojekti-2022/vesialue-back)


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
BIG_DATA_API_KEY<big data geo api key>
FLASK_APP=src/app.py
FLASK_ENV=development
```

In the virtual environment, start the server from the root of the project in development mode by running:
```bash
flask run
```

## Testing

Provide additional environment variables in `.env` file created before:
```bash
TEST_MONGO_URI=<MongoDB URI>
```

Run tests and collect coverage report:
```bash
FLASK_ENV=test coverage run -m pytest
```

## Docker
### Building image
```docker build -t vesialue-back .```

### Running image locally
```docker run --rm -p 3000:3000 vesialue-back```
The service will be available at port 3000.

The port can be specified using the PORT environment variable
(used when running on Heroku). The default is 3000.

