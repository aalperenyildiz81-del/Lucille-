FROM python:3.11-bullseye

# Metadata
LABEL maintainer="Lucille Development Team"
LABEL description="Lucille - Advanced Security Reconnaissance Framework"
LABEL version="1.0.0"

# Set working directory
WORKDIR /lucille

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    dnsutils \
    whois \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY setup.py .
COPY lucille.py .
COPY README.md .
COPY USAGE.md .

# Copy source code
COPY src/ src/
COPY config/ config/
COPY data/ data/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p results logs

# Set entry point
ENTRYPOINT ["python", "lucille.py"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python lucille.py status || exit 1
