#Video Streamer (Flask-SocketIO)
This repo provides source code for running a python-flask based video streamer.

## Overview
The server is a Flask-SocketIO based server. It can be hosted on your 
local machine or in a cloud. 

There is an example client provided using OpenCV. We plan to add 
support for other types of clients in future.

The server can be installed on your local machine or any cloud instance. 
The client can stream video data through any headless embedded device. 
The goal of this project is to make the embedded CV application development
quicker. 

## Setup
```bash
git clone https://github.com/visionify/flask-socketio-video-streamer
cd server
pip3 install -r requirements.txt
python3 server.py
```
Open browser at http://localhost:6001 to view the server.

## Client
```bash
git clone https://github.com/visionify/flask-socketio-video-streamer
cd client
pip3 install -r requirements.txt
python3 open_cv_client.py
```
