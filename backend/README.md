# Project Setup (Windows)
Make sure that Python (>=3.10) is installed in the system. Otherwise install it and add it to path (environment variables). 
Create a virtual environment within the `path/to/bl0ck_v0`

    python -m venv venv_name

Enter the virtual environment using:

    venv_name/Scripts/activate


## Download Dependencies
The project uses fastAPI to make API requests and uvicorn to load the frontend in development environment, locally. Download fastAPI using:

    pip install fastapi uvicorn


## Project Launch
Once the virtual environment has been activated, execute the following commands in powershell terminal in VS Code:
    
    cd backend
    uvicorn main:app --reload

Open new terminal and execute the following: (Optional but Recommended)
   
    . ./profile-curl.ps1

Follow the list of API calls mentioned below

## API calls via Powershell Terminal using curl.exe
---

> **_NOTE_** *Execute `. ./profile-curl.ps1` to use `cl` (GET), `clPost` (POST), and `clPut` (PUT) in order to avoid typing the full API URL each time. The helper auto-prefixes endpoints with `/api/v1`. Change the port number in profile-curl.ps1 if the default is busy.*

---
### Root Welcome
    cl /status
---
    curl.exe http://127.0.0.1:8000/api/v1/status

### Get Entire Blockchain ⛓️🅱️⛓️
    cl /blockchain/display
---
    curl.exe http://127.0.0.1:8000/api/v1/blockchain/display

### Add a New Block to the Bl0ckchain 🅱️✅
    clPost /blockchain/add
---
    curl.exe -X POST http://127.0.0.1:8000/api/v1/blockchain/add

### Get the last (latest) Bl0ck added to the system 🔗🅱️
    cl /blockchain/last-block 
---
    curl.exe http://127.0.0.1:8000/api/v1/blockchain/last-block

### Get current difficulty ⛓️🔄️✅
    cl /difficulty/current
---
    curl.exe http://127.0.0.1:8000/api/v1/difficulty/current

### Enable DDM by updating the manual difficulty (1 - 10) 1️⃣-🔟
    clPut /difficulty/manual/{Value}
---
    curl.exe -X PUT http://127.0.0.1:8000/api/v1/difficulty/manual/{Value}

### Disable DDM by switching to auto mode 🔄️✅
    clPut /difficulty/auto
---
    curl.exe -X PUT http://127.0.0.1:8000/api/v1/difficulty/auto

### Set mining timeout (10 - 300 seconds) 🕛⁉️
    clPut /mining/timeout/{Value}
---
    curl.exe -X PUT http://127.0.0.1:8000/api/v1/mining/timeout/{Value}
