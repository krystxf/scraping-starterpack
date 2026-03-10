# Captcha Endpoint

## Setup

1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the API server:
```bash
python app.py
```

API available at `http://localhost:3100`

## Endpoints

- `POST /extract-text` - Extract text from image
  ```bash
  curl -X POST http://localhost:3100/extract-text -F "image=@image.png"
  ```
