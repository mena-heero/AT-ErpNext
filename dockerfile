# Use the official Frappe/ERPNext image as the base image
FROM frappe/erpnext:v14.38.0

# Set the working directory
WORKDIR /home/frappe/frappe-bench/apps

# Create the 'heero' user manually
#RUN useradd -ms /bin/bash heero

# Copy your custom app into the apps directory
COPY . /home/frappe/frappe-bench/apps/heero

# Switch to the 'heero' user
#USER heero

# Run any setup or customization commands, if needed
RUN bench new-site alltargeting.com 
# For example, you might want to install your app
RUN bench --site alltargeting.com install-app heero

# Expose any ports your app uses (if applicable)
EXPOSE 80

# Start the Frappe/ERPNext application
RUN sudo bench setup production
