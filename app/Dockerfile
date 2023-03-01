
FROM python:3.8.12-slim
# Download Package Information
RUN apt-get update -y
# Install Tkinter
RUN apt-get install tk -y
# Copy the content of the project directory to the working directory
COPY . /app
WORKDIR /app
ENV TZ=Asia/Kolkata
RUN cp /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
# Install any dependencies
RUN pip install -r requirements.txt --no-cache-dir
