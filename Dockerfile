# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

ENV PYTHONPATH=/app/src
ENV APP_MODE=direct
ENV PORT=10000

# Copy project files
COPY . .

# Install uv
RUN pip install uv

# Install dependencies
RUN uv sync

# Expose port
#EXPOSE 8000
EXPOSE 10000

# Run FastAPI app
#CMD ["uv", "run", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["uv", "run", "streamlit", "run", "ui/streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "10000"]
CMD ["sh", "-c", "uv run streamlit run ui/streamlit_app.py --server.address 0.0.0.0 --server.port ${PORT:-10000} --server.headless true --server.enableCORS false --server.enableXsrfProtection false --server.fileWatcherType none --browser.gatherUsageStats false"]