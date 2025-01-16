# Use base image
FROM ubuntu:latest

# Set working directory
WORKDIR /app

# Create a non-root user
RUN useradd -m myuser && \
    mkdir -p /app && \
    chown -R myuser:myuser /app

# Copy the script into the container
COPY print_names.sh /app/script.sh

# Ensure the script is executable and owned by the non-root user
RUN chmod +x /app/script.sh && chown myuser:myuser /app/script.sh

# Switch to the non-root user
USER myuser

# Execute the script
CMD ["/bin/bash", "/app/script.sh"]
