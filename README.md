# Running locally
You can run locally with fastapi:

```shell
fastapi run gigtracker/app.py
```

If you want to run in development mode and specifying a non-default port you can do that:
```shell
fastapi dev gigtracker/app.py --port 4001
```

FastAPI uses uvicorn, so if you wanted you could instead run with uvicorn:
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

