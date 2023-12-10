# Use the official Python image as the base image
FROM python:3.12

# Set the working directory in the container
RUN mkdir -p "/beetseeker"

WORKDIR ["/beetseeker"]

# Clone the GitHub repository
RUN git clone https://github.com/andrewjmetzger/beetseeker.git .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Allow the config to be mounted
VOLUME ["/beetseeker/config.py"]

COPY "./example_config.py" "./config.py"
RUN chmod +x "./config.py"

# Expose the port the app runs on
EXPOSE 8347

# Command to run the application
CMD ["python", "main.py"]