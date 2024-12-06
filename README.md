# Running locally

```shell
uvicorn app:app --reload --port 4001
```

# Deploying the app


## Local Testing
To test the docker container locally run the following commands

Build the image:
```shell
docker build . -t gigtracker
```

Run the image exposing the app on localhost:4002
```shell
docker run -p4002:80 gigtracker
```

