# From python 3.7 docker images
FROM python:3.7-slim

# Application directory
WORKDIR .

COPY ./model_building/requirements.txt ./requirements.txt

# Install dependencies
RUN apt-get update -y \
&& pip install --upgrade pip \
&& pip install -r ./requirements.txt

# Create a volume
VOLUME /Models

# Copy app fodler
COPY ./model_building ./model_building
COPY ./data ./data

# Run the application
ENTRYPOINT ["python"]
CMD ["./model_building/model_building_script.py"]
