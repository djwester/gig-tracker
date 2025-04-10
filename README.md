# Running locally

## Pre-requisites
This project is setup to use [mise](https://mise.jdx.dev/getting-started.html) to install the necessary tools. You can install mise using brew or winget etc.

Once you have mise you can install the necessary tools by calling it:

```shell
mise install
```

If you don't have mise (or don't want to use it), you can look in the [.mise.toml](./.mise.toml) file to see what tools and versions you need to install

## Installing
You can install all necessary dependencies using poetry

```shell
poetry install
```

## Running
Before running you should activate the poetry environment
```shell
poetry env activate
```

You can then run locally with fastapi:

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
If you want to make changes to the app, you should run tailwinds to regenerate the css as you change it

```shell
tailwindcss -i ./gigtracker/static/src/tailwind.css -o ./gigtracker/static/css/main.css --watch
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

