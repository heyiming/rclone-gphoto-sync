FROM curlimages/curl as stage1
WORKDIR /tmp
RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
RUN unzip rclone-current-linux-amd64.zip

FROM python:3.8-slim

# rclone setup
COPY --from=stage1 /tmp/rclone-*-linux-amd64/rclone /usr/bin/
# CMD ["ls", "-l", "/usr/bin/"]
RUN chown root:root /usr/bin/rclone
RUN chmod +x /usr/bin/rclone

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN chmod +x /app/app.py
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "app.py"]
