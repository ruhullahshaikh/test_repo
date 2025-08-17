FROM python:3.14.0rc2

# Missing specific tag for base image (uses 'latest')
RUN pip install -r requirements.txt

# Running application as root user
CMD ["python", "app.py"]
