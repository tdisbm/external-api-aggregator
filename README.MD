# How to launch

### 1. Using docker compose (Recommended)

- Ensure you have `docker-compose:V2.29.7-desktop` or `docker-compose:2.34.0` installed
- Verify that `docker:27.3.1` is installed
- Open a terminal and navigate to the `hosts-api-aggregator` directory.
- Run `docker-compose up`
- Wait until all containers are running and marked green
- Check the application status on `localhost:8000`

### 2. Using host machine! Like a real hero!
Requirements
- `python 3.10` 
- `mongo 8.0` 
- `pip23.2.1`
- `virualenv` (normally comes with pip)
- Ensure python (version 3.10) is recognized as a system command on your machine 

Setting up the environment
- Open a terminal and navigate to `hosts-api-aggregator`
- Run `python -m venv venv` to create a venv
- Activate the venv by running `venv/scripts/activate` script
- Once activated run `pip install -r requirements.txt`

Start applications (2 different terminals)
- `polling-app`
  - Navigate to `hosts-api-aggregator`
  - Activate the venv `venv/scripts/activate`
  - Set the env var `PYTHONPATH=/app` (only for the current terminal session)
  - Start service with `python -m app.polling-app` command
- `fastapi-app`
  - Same as `polling-app` but the running command is `python -m app.fastapi-app`

# Extra

### 1. Visualization
To see some visuals on hosts, just access the index page `http://localhost:8000` (which is definitely not AI generated `html` & `css` & `js`). But make sure that fastapi service is running.
> **NOTE:** The visualization is somewhat slow due to the inefficient nested JSON rendering algorithm on the client side

### 2. Known issues
- (Windows related) Sometimes, polling-app closes the event loop unexpectedly. It is very annoying, but it's not affecting app's flow