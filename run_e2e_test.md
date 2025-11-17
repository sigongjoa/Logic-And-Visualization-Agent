# E2E Test Execution Guide

This guide provides the commands to start the backend and frontend servers, and then run the Playwright E2E test.

**Prerequisites:**
*   Ensure you have `python3` and `npm` installed.
*   Ensure you have created and activated the Python virtual environment and installed `requirements.txt`.
    *   `python3 -m venv .venv`
    *   `source .venv/bin/activate`
    *   `pip install -r requirements.txt`
*   Ensure you have installed Node.js dependencies in the `frontend` directory.
    *   `cd frontend`
    *   `npm install`
    *   `cd ..`
*   Ensure Playwright browsers are installed.
    *   `cd frontend`
    *   `npx playwright install`
    *   `cd ..`

---

## Step 1: Start the Backend Server

Open a new terminal, navigate to the project root directory (`/mnt/d/progress/lava/`), and run the following commands:

```bash
source .venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Leave this terminal running.

---

## Step 2: Start the Frontend Development Server

Open another new terminal, navigate to the `frontend` directory (`/mnt/d/progress/lava/frontend/`), and run the following command:

```bash
npm run dev
```

Leave this terminal running. Wait until you see output indicating the server is running (e.g., "Local: http://localhost:5173/").

---

## Step 3: Run the Playwright E2E Test

Open a third new terminal, navigate to the `frontend` directory (`/mnt/d/progress/lava/frontend/`), and run the following command:

```bash
npx playwright test frontend/e2e/assignment_review.spec.ts
```

This will run the test, navigate to `http://localhost:5173/`, and take a screenshot named `assignment_review_page.png` in the `frontend` directory.

---

## Step 4: Cleanup (Optional)

After you are done, you can stop the backend and frontend servers by pressing `Ctrl+C` in their respective terminals.

To deactivate the Python virtual environment:
```bash
deactivate
```
