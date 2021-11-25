# Tokopedia Product Scraper

Tokopedia Product Scraper based on category

## Requirements

- Python 38+
- Chrome Web Driver


## How to run

### Setup Python Virtualenv

Create Virtual Env

```
python3 -m venv venv
```

Activate the virtualenv

```
source venv/bin/activate
```

### Install Requirements

```
pip install requirements.txt
```

### Chrome Driver

You could install the chrome driver on this link
https://chromedriver.chromium.org/downloads

We need the chrome driver becase this project using selenium

### Run

```
./run.py --category handphone-tablet/handphone --length 100 --output output
```

use ```./run.py --help``` to see the short command options

The csv file will be on the ouput directory, or if you can choose the directory do you want.

--------------------------
### Thank You
