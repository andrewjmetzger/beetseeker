# Use the official Python image as the base image
FROM python:3.12

# Clone the GitHub repository
RUN git clone https://github.com/andrewjmetzger/beetseeker.git

# Set the working directory in the container
WORKDIR ["/beetseeker"]

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY "./example_config.py" "./config.py"
RUN chmod +x "./config.py"

# Allow the config to be mounted
VOLUME ["/beetseeker/config.py"]


# Expose the port the app runs on
EXPOSE 8347

# Command to run the application
ENTRYPOINT ["python", "main.py"]