# YouTube View Bot

This is a tool to boost viewer count on a YouTube video. This is not intended for malicious purposes or monetization strategies. This was intended for personal use and testing purposes.

# Installation

### Python Version
Download the latest [Python](https://www.python.org/downloads/) release.

This program was built in Python 3.9.0, but should work in Python 3.9.0+

### Downloading the GitHub repository
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the repository.

```bash
pip install https://github.com/gavintranquilino/YouTube-view-bot.git
```

Alternatively, download this project as a **.zip** file, and extract into your device.

### Downloading the dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies listed in **requirements.txt**.

```bash
pip install -r requirements.txt
```

# Configuration

### config.json
1. Enter the required settings into the *config.json* file

```json
{
    "website": "YOUR VIDEO", 
    "tab_amount": 3,
    "watch_time": 35,
    "view_cycles": 5,
    "browser": "firefox"
}
```

# Usage

### How do I run this program?
If you have completed the setup and configuration listed above, open a terminal in this directory and run using this command.

```bash
python main.py
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

See [CONTRIBUTING.md](https://github.com/gavintranquilino/YouTube-view-bot/blob/master/CONTRIBUTING.md) file.

## License
See [LICENSE](https://github.com/gavintranquilino/YouTube-view-bot/blob/master/LICENSE) file.

