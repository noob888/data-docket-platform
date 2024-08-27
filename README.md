# about Datadocket
- This is a student software engineering project intended to build a functioning website prototype for a client.
- The client requested a website with very similar functionality, look, and feel to Kaggle.com.
- This code was built with Python Django in Winter 2023 for Mohawk College's software engineering course.
- The team involved is Aakif Lokhandwala, Matt Pluim, Krysto Ayala, and John Benjamin

# running the project for the first time
- download or clone the project from Github
- from the root directory (the one containing manage.py) run the following in a terminal to start a virtual environment:
    source env/bin/activate
- ensure Django is installed:
    pip install django
- ensure Azure tools are installed (applies to development phase only):
    pip install azure-storage-blob
- start the development server (you may need to replace python3 with python or py):
    python3 manage.py runserver
- in a browser, open the server address provided in the terminal

# connecting to the database server
- in a terminal, run the command:
    psql "host=datadocket-dev.postgres.database.azure.com port=5432 dbname=postgres user=<obtain username from team> password=<obtain password from team> sslmode=require"
- try some of the following commands to explore the data:
    \dt
    \d backend_competition
    TABLE backend_competition;
    SELECT * FROM backend_competition;
