# FastAPI Email Application

A FastAPI application for sending professional emails with dynamic content using SMTP and HTML templates.

## Features

- Send emails using Gmail SMTP.
- Render HTML email templates with Jinja2.
- Send emails asynchronously in the background.

## Setup

- Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-email.git
cd fastapi-email
```

Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate for Windows
```

Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a .env file with your Gmail SMTP credentials:

```env
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=465
    SMTP_USERNAME=your-email@gmail.com
    SMTP_PASSWORD=your-email-password
    SENDER_EMAIL=your-email@gmail.com
```

## Templates

- HTML Template: Located in templates/html_template.html

## Running the Application

Start the FastAPI Server

```bash
uvicorn main:app --reload
```

## Send a Test Email

Use the send_email_background function in main.py or integrate it into an endpoint.
