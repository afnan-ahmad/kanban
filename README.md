# Kanban App v2

Project for the Modern Application Development II course (Sep 2022 term) in the IITM BS Degree programme.

Created by: Afnan Ahmad (21F1003730@student.onlinedegree.iitm.ac.in)

## Running locally

**This app uses celery, therefore it is recommended to run it on Linux or WSL only.**

1. Ensure Python (version 3.8 or above) is installed on the system.
2. Create and activate a virtual environment, in the same directory where the app's source is placed.
3. Once the environment is activated, run `pip install -r requirements.txt` to install server-side dependencies.

### Celery Jobs

* Please ensure redis-server is installed and running on the default port (6379).
* To test email functionality, ensure MailHog is installed and running on the default port (1025).

The worker for jobs can be started by running the following command from ``src`` directory:

``celery -A kanban.jobs.worker worker --loglevel=info``

### API Server and Web UI

1. Run `python main.py` to start the backend (api) server.
2. Navigate to the `src/web` directory, and run ``npm install`` to install dependencies for the frontend.
3. Run ``npm serve`` to start the frontend server.
4. The app would be accessible at `http://localhost:8080`.