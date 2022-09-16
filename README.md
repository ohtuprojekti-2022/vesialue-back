# vesialue-back
Vesialueen inventointi-ilmoitus backend

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

In virtual environment run:
```bash
cd src
flask run
```

## Docker
### Building image
```docker build -t vesialue-back .```

### Running image locally
```docker run --rm -p 3000:3000 vesialue-back```
The service will be available at port 3000.

The port can be specified using the PORT environment variable
(used when running on Heroku). The default is 3000.
