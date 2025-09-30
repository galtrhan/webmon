# WebMon - Website Monitoring Tool

A Python-based website monitoring tool that checks URL availability, logs incidents to SQLite database, and sends notifications via email and FCM push notifications.

## Quick Start

### Using Makefile (Recommended)

```bash
# Full setup (creates venv, installs dependencies, sets up config)
make setup

# Run the application
make run

# See all available commands
make help
```

### Manual Installation

Create virtual environment and install dependencies

```bash
python -m venv venv

# on windows
venv\Scripts\activate

# on mac/linux
source venv/bin/activate

pip install -r requirements.txt
```

If you get an error about sqlite not being found, you may need to install the sqlite3 development package. On Ubuntu, this can be done with the following command:

```bash
sudo apt-get install sqlite3
```

## Configuration

1. Copy the sample configuration:
   ```bash
   cp config.sample.json config.json
   ```

2. Edit `config.json` with your settings:
   - Add URLs to monitor
   - Configure SMTP settings for email notifications
   - Set up FCM for push notifications
   - Adjust refresh interval

## Usage

### Using Makefile
```bash
make run
```

### Manual execution
```bash
python main.py
```

## Available Makefile Commands

- `make setup` - Complete setup (venv + dependencies + config)
- `make install` - Create virtual environment and install dependencies
- `make dev` - Show virtual environment activation instructions
- `make run` - Run the WebMon application
- `make clean` - Remove virtual environment
- `make deps` - Show installed dependencies
- `make help` - Show all available commands

## Features

- **URL Monitoring**: Checks website availability at configurable intervals
- **Incident Logging**: Records all incidents in SQLite database
- **Email Notifications**: Sends alerts via SMTP
- **Push Notifications**: Sends alerts via Firebase Cloud Messaging (FCM)
- **Configurable**: JSON-based configuration for easy customization
- **Cross-platform**: Works on Windows, macOS, and Linux bash
python main.py
```