#!/bin/bash

# List of packages to install
packages=(
  "bcrypt==4.0.1"
  "channels==4.2.0"
  "stripe==10.8.0"
  "pytest==8.3.3"
  "django-test-plus==2.0.1"
  "django-allauth==65.2.0"
  "gunicorn==20.1.0"
  "mysqlclient==2.2.4"
  "pycountry"
  "cryptography"
)

echo "Starting installation of packages..."

# Loop through the packages and install each one
for package in "${packages[@]}"; do
  echo "Installing $package..."
  pip install "$package"
  if [ $? -eq 0 ]; then
    echo "$package installed successfully!"
  else
    echo "Error installing $package. Exiting."
    exit 1
  fi
done

echo "All packages installed successfully!"

