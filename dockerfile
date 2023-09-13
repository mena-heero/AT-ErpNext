# Use the official ERPNext Docker image as the base image
FROM frappe/erpnext-worker:v14

# Set the working directory to the Frappe Bench directory
WORKDIR /home/frappe/frappe-bench

# Copy your custom app into the apps directory
COPY . /home/frappe/frappe-bench/apps/heero

# Expose ports if needed
EXPOSE 8000

# Start ERPNext
CMD ["bench", "start"]
