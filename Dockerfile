FROM python:3.11-slim
FROM debian:bullseye-slim
# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY income_predictor/ income_predictor/
COPY income_predictor_api/ income_predictor_api/

COPY MANIFEST.in mypy.ini pyproject.toml setup.py ./

# Copy requirements directory first
COPY requirements/ requirements/

# Install build dependencies and all requirements
#RUN apt-get update -o Debug::Acquire::http=true
#RUN cat /etc/apt/sources.list
RUN apt-get update 

#RUN apt-get install -y --no-install-recommends gcc build-essential
RUN pip install --no-binary :all: -e ".[api]"
RUN pip install --no-cache-dir fastapi uvicorn pydantic-settings
RUN apt-get remove -y gcc build-essential
RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*



# Create VERSION file if it doesn't exist
RUN if [ ! -f income_predictor/VERSION ]; then echo "0.1.0" > income_predictor/VERSION; fi

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Expose the API port
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "income_predictor_api.app.main:app", "--host", "0.0.0.0", "--port", "8001"]