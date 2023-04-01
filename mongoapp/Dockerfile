# Set base image (host OS)
FROM python:alpine3.8

# Copy the content of the project directory to the working directory
COPY . /mongoapp
COPY templates /mongoapp
COPY static /mongoapp
# Set the working directory in the container
WORKDIR /mongoapp
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
# Install any dependencies
RUN pip install -r requirements.txt --no-cache-dir
