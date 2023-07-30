# Use an official Python runtime as the base image
FROM joyzoursky/python-chromedriver:3.9-selenium

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the container
COPY . .

# Run the Python script
CMD ["python", "app.py"]
