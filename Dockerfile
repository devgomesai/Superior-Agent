FROM python:3.12

WORKDIR /app

# Copy requirements from the correct location
COPY src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy source code and templates
COPY src/ /app/src/
COPY src/templates/ /app/templates/
COPY .env /app/.env


# Create output directory for the application
RUN mkdir -p /app/output

EXPOSE 8000

CMD ["uvicorn", "src.agent.api.api:app", "--host", "0.0.0.0", "--port", "8000"]