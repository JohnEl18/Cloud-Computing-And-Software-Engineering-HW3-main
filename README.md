# Cloud-Computing-And-Software-Engineering-HW1
Assignment 1 RESTful API and Docker usage

***Build the Docker image***
docker build -t homework1 .

***Running the app with default port***
docker run -p 9000:8000 homework1


***Running the app with custom port***
To run the app with a custom port, you'll need to set the FLASK_RUN_PORT environment variable when starting the Docker container.
For example, to run the app on port 8003, use the following command:
docker run -p 9000:8003 --env FLASK_RUN_PORT=8003 homework1

Enjoy,
Yonatan Eliyahu and Moshe Azulay
