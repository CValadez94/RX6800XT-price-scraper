A web scraper to track prices of RX 6800XT GPUs.

- [X] Microcenter prices
- [X] Flask server

##How to install
To install, you should create a virtual environment and install the dependencies
### Linux:
In the project directory run:
```sehll
mkdir venv
python -m venv venv/
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows:
In the project directory run:
```shell
mkdir venv
python -m venv venv/
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```


##How to run
To run, you'll need to activate the virtual environment first
### Linux:
```shell
source venv/bin/activate
python main.py
```

### Windows
```
venv\Scripts\activate.bat
python main.py
```

**Note**: To deactivate the virtual environment, you just need to run the command `deactivate`