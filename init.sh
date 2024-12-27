# Install virtualenv
pip install virtualenv

# Check if "venv" exists, if not, create it
if [ ! -d "venv" ]; then
    echo --------------------
    echo Creating virtualenv
    echo --------------------
    virtualenv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Apply database migrations (equivalent to Flask DB commands)
echo --------------------
echo Applying database migrations
echo --------------------
python3 manage.py makemigrations
python3 manage.py migrate

# Generate test data (equivalent to test_data.py in Flask)
echo --------------------
echo Generate test data
echo --------------------
python3 manage.py shell < test_data.py

# Run the Django development server
echo --------------------
echo Running the app
echo --------------------
export DJANGO_SETTINGS_MODULE=Flirtro.settings
export DJANGO_DEBUG=1
python3 manage.py runserver
