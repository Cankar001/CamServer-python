# CamServer

The CamServer receives a video stream by raspberry pi clients and stores them into a configurable file location, on which a PHP application listens to and streams the unclosed file handles to the web client, if requested.

There will be another client type, that gets registered as a display, meaning that the server sends the frame to all clients, registered as displays.

# Getting started

## Clone the repository
```shell
git clone https://github.com/Cankar001/CamServer.git
```

## Create a environment file
You need to copy the `.env.example` file and rename it to just `.env`.

After that you need to fill in your server and port, 
in most cases you can use `0.0.0.0` as the server address, 
this means that the client can connect from any address, using the correct port. 

The port can be any port you like, as long as the client connects to the same port.

## Create a virtual environment
```shell
python -m venv venv
```

## Activate the virtual enviroment
```shell
# on windows
.\venv\Scripts\activate.bat

# on linux
source ./venv/bin/activate
```

## Check if environment has been activated
```shell
# This command should show the python path,
# pointing to your env folder
pip --version
```

## Install requirements from requirements.txt
```shell
pip install -r requirements.txt
```

## Run server
```shell
pipenv run python Server.py ./uploads
```

# Troubleshooting

I discovered, that the virtualenv doesn't seem to like the powershell, 
I couldn't get it working in it.

But using a bash on windows, using `source ./venv/Scripts/activate` worked perfectly fine.
