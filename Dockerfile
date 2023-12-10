# Use the official Python image as the base image
FROM python:3.12
# Set the working directory in the container
RUN mkdir -p "/beetseeker"
WORKDIR ["/beetseeker"]


ADD . /beetseeker

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Allow the config to be mounted
VOLUME ["/beetseeker/config.py"]


# Expose the port the app runs on
EXPOSE 8347

# Command to run the application
ENTRYPOINT ["python", "main.py"]