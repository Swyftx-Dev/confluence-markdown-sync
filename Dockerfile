# Use a lightweight Python image
FROM python:3.10-alpine

# Set working directory
WORKDIR /action

# Install any required dependencies
RUN apk add --no-cache git bash

# Install Python dependencies from Pipfile or requirements
COPY ./Pipfile* ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy && \
    pipenv --clear

# Copy the application code
COPY ./src .

# Set the default entry point for the action
ENTRYPOINT [ "python" ]
CMD [ "/action/main.py" ]
