# scrapy_test

This project contains a Scrapy spider used to collect information from the [Kelm Immobilien](https://kelm-immobilien.de/) website.

## Setup

To use the Scrapy Test project, follow these steps:

Navigate to the project folder
```bash
cd path/to/project/scrapy_test
```

Install a virtual environment module
```bash
python3 -m pip install virtualenv
```

Create a virtual environment
```bash
python3 -m virtualenv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Navigate to udata_test
```bash
cd udata_test
```

Install the required packages using pip
```bash
python3 -m pip install -r requirements.txt
```

## Run

To collect data from the Kelm Immobilien website, run the following command:
```bash
python3 -m scrapy runspider spiders/kelm_immobilien.py 
```

The kelm_immobilien.py script is a Scrapy spider which scrapes property information from the Kelm Immobilien website.
