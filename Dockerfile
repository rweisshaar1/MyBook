FROM python:latest
# Used to specify the working directory (where our COPY/ADD directives copies files when no path is specified)
WORKDIR /code
# Similar to the COPY directives (I won’t go into the details of the difference)
ADD requirements.txt requirements.txt
# Run a command during the building of the image. In this case, we install the libraries specified in requirements.txt (that has already been copied into the image working directory)
RUN pip install -r requirements.txt

# Copy the entire current directory into the Docker image
COPY . .
# Similar to the RUN directive, but this is launch only when the image is started. It is the entrypoint of the image.
CMD ["python", "-u", "app.py"]