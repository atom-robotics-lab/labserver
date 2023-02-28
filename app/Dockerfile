# Set base image (host OS)
# Slim version of Python
FROM python:3.8.12-slim

# Download Package Information
RUN apt-get update -y

# Install Tkinter
RUN apt-get install tk -y
# Commands to run Tkinter application
# Copy the content of the project directory to the working directory
COPY . /app
WORKDIR /app
# RUN apk add -U tzdata
# RUN pip install tk
ENV TZ=Asia/Kolkata
RUN cp /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
# Install any dependencies
RUN pip install -r requirements.txt --no-cache-dir
