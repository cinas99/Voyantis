# Message Queue Manager

This project implements a backend REST API and a frontend web page for managing message queues.

## Features

- Add and retrieve messages from named queues.
- View all available queues and their message counts.
- Interactive web interface styled in Voyantis' "look & feel".

![Preview image](uiPreview.png)

## Setup Instructions

#### Backend

1. Navigate to the `backend` folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Go back to the upper folder by typing `cd ..` command in the terminal 
4. Run the server: `python backend/app.py`

#### Frontend

1. Navigate to the `frontend` folder.
2. Serve the web page locally: `python -m http.server 8000`
3. Open your browser at `http://localhost:8000`.

#### Testing

Use curl or a browser to test the API endpoints and web interface.
