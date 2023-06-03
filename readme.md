## Installation

Create virtual environment and install dependencies

``` bash
python -m venv venv

# on windows
venv\Scripts\activate

# on mac/linux
source venv/bin/activate

pip install -r requirements.txt
```

If you get an error about sqlite not being found, you may need to install the sqlite3 development package. On Ubuntu, this can be done with the following command:

``` bash
sudo apt-get install sqlite3
```

## Usage

``` bash
python main.py
```