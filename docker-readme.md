
# To build postgresql database container:
<!-- $ cd database/
# Create the docker image
$ docker build .
# Run the docker image and connect to it
$ docker run -it <image_id> bash
# Enter to the database
psql postgres://username:secret@localhost:5432/database -->

# To build application container:
<!--
# Run this in the parent directory
$ docker build -t <container-name> -f app/Dockerfile .
$ docker run -d -p 5001:5000 <container-name>
# Check in browser port 5001 or the port it's mapped to -->