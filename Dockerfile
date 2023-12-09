# Use the official Python image as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/andrewjmetzger/slskd-betanin-connector.git .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8347

# Command to run the application
CMD ["python", "main.py"]
