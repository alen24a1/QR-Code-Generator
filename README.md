# QR Code Generator

A simple Flask app that generates customizable QR codes in-browser.

## Requirements

- Python 3.8+
- `Flask`
- `qrcode[pil]`

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python index.py
```

This will start the app and open your browser automatically at `http://127.0.0.1:5000`.

## Deploy

If you deploy to a platform like Heroku, use a `Procfile` containing:

```Procfile
web: gunicorn index:app
```

Then deploy normally. Locally, do not type `web:` at the PowerShell prompt; that prefix is only valid inside a `Procfile`.

## Features

- Generate QR codes from URLs or text
- Choose foreground and background colors
- Download the generated QR code as PNG
