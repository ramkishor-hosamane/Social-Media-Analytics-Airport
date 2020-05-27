# Social media analytics
## Project overview
Airports are the gateway for a country to strengthen it's socio-economic ties with the rest of the world. Almost 3% of the country's GDP depends on the airlines industry. A large section of the Indian population uses air travel for their convenience to travel both domestically and internationally. This eventually results in a large volume of feedbacks received by the airport management. In order to keep track and analyse the public opinion. An automated feedback analysis system for sentimental analysis is required to improve the quality of the services in the airport. 

## Installation

### Prerequisites

#### 1. Install Python
Install ```python-3.7.2``` and ```python-pip```. Follow the steps from the below reference document based on your Operating System.
Reference: [https://docs.python-guide.org/starting/installation/](https://docs.python-guide.org/starting/installation/)

#### 2. Setup virtual environment
```bash
# Install virtual environment
sudo pip install virtualenv

# Make a directory
mkdir envs

# Create virtual environment
virtualenv ./envs/

# Activate virtual environment
source envs/bin/activate
```

#### 3. Clone git repository
```bash
git clone "https://github.com/dhanraj6/socail-media-analytics"
```

#### 4. Install requirements
```bash
pip install -r requirements.txt
sudo apt update
sudo apt upgrade
sudo apt install python3-bs4
python -m spacy download en_core_web_md
```

#### 5. Run the server
```bash
# Run the server
cd SMA/
python manage.py runserver
 
# your server is up now
```
Try opening [http://localhost:8000](http://localhost:8000) in the browser.
Now you are good to go.


#### 6. Demo Video link
https://drive.google.com/file/d/1wpw4_vFaHaC5ARJhGeFO7iU0qfos_P45/view?usp=sharing

#### 7. URLs and screenshots
#### Home page: [http://localhost:8000/home](http://localhost:8000/home)
![](https://i.imgur.com/yZV7741.jpg)
#### About: [http://localhost:8000/about](http://localhost:8000/about)
![](https://i.imgur.com/WdfFPEv.jpg)
#### Scrapping: [http://localhost:8000/scrapping](http://localhost:8000/scrapping)
![](https://i.imgur.com/FKYRB49.jpg)
#### Analysis: [http://localhost:8000/analysis](http://localhost:8000/analysis)
![](https://i.imgur.com/cx746KF.jpg)
