
# Running Docker for a Fullstack App as a DockerStack
---
<br>

1. Install Docker engine from https://docs.docker.com/get-docker/

1. Within your terminal navigate to the same directory as docker-compose.yml

1. Run the command ```docker-compose up -d```

1. Open your browser and navigate to the server address, in development this is localhost:5000

---

# Other Helpful Docker Commands

---
<br>

### To Open the Postgres Container in Interactive Mode
<br>
Run:

         $ docker exec -it <container-ID> bash

**Connect to psql**

         $ psql -U postgres

**Note**

        You can use ctrl + D to quit interactive shell.

### To build only the application container:
<br>

 **Run this in the parent directory:**

            $ docker build -t <container-name> .

            $ docker run -d -p 5001:5001 <container-name>

 **Check in browser port 5001 or the port it's mapped to**