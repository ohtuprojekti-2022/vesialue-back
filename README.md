# vesialue-back

![GitHub Actions](https://github.com/ohtuprojekti-2022/vesialue-back/workflows/CI/badge.svg)

Vesialueen inventointi-ilmoitus backend

- Production branch: main
- Staging branch: staging

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

In virtual environment run:
```bash
flask run
```
## Heroku
- [Staging](https://vesialue-back-staging.herokuapp.com)
- [Production](https://vesialue-back.herokuapp.com)

There are GitHub Actions to build the containers and
push them to Heroku on each commit to main and staging branches

## Docker
### Building image
```docker build -t vesialue-back .```

### Running image locally
```docker run --rm -p 3000:3000 vesialue-back```
The service will be available at port 3000.

The port can be specified using the PORT environment variable
(used when running on Heroku). The default is 3000.

