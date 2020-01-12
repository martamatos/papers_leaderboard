This is the very beginning of our papers leaderboard.

To set it runnning:
 - create a virtual environment
 - install the requirements, using one of the following:
   - pip for requirements.txt
   - conda for requirements_conda.yml

To set up the database, i'm using a docker container at the moment.
But bottom line, make you sure have:
 - postgres up and running
 - an .env file where the following variables are defined:
   - POSTGRES_USER
   - POSTGRES_PW
   - POSTGRES_DB
   - POSTGRES_URL

Then to create the database with all the tables, on the project directory run:
 - `flask db init`, to start the DB
 - `flask db migrate -m "message"` to create the migration
 - `flask db upgrade` to actually apply the migration

To run the server:
 - on the project directory, run `flask run`;
 - open your browser and go to `localhost:5000`.

Hopefully it all worked out :).
