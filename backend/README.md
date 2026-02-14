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

> **_NOTE_** *Execute `. ./profile-curl.ps1` to use `cl` and `clPost` in order to avoid using `curl.exe http://127.0.0.1:8000/` and `curl.exe -X POST http://127.0.0.1:8000/`, respectively. Change the port number in profile-curl.ps1, in case the default is busy.*

---
### Root Welcome
    cl blockchain/
---
    curl.exe http://127.0.0.1:8000/

### Get Entire Blockchain ⛓️🅱️⛓️
    clPost blockchain/display
---
    curl.exe -X POST http://127.0.0.1:8000/blockchain/display

### Add a New Block to the Bl0ckchain 🅱️✅
    clPost blockchain/add
---
    curl.exe -X POST http://127.0.0.1:8000/blockchain/add

### Get the last (latest) Bl0ck added to the system 🔗🅱️
    clPost blockchain/last-block 
---
    curl.exe -X POST http://127.0.0.1:8000/blockchain/last-block

### Enable DDM (Dynamic Difficulty Mode) ⛓️🔄️✅
    clPost difficulty/enable
---
    curl.exe -X POST http://127.0.0.1:8000/difficulty/enable

### Disable DDM (Dynamic Difficulty Mode) ⛓️🔄️❎
    clPost difficulty/disable
---
    curl.exe -X POST http://127.0.0.1:8000/difficulty/disable

### Set Manual Difficulty (1 - 10) 1️⃣-🔟
    clPost difficulty/set-manual/{Value}
---
    curl.exe -X POST http://127.0.0.1:8000/difficulty/set-manual/{Value}

### Switch to Auto Mode 🔄️✅
    clPost difficulty/switch-to-auto
---
    curl.exe -X POST http://127.0.0.1:8000/difficulty/switch-to-auto

### Set Mining Timeout (10 - 300 seconds) 🕛⁉️
    clPost mining/set-timeout/{Value}
---
    curl.exe -X POST http://127.0.0.1:8000/mining/set-timeout/{Value}

---

# Project Setup (Linux / Ubuntu)

Make sure that Python (>=3.10) is installed in the system. Otherwise install it:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
````

Create a virtual environment within the `path/to/bl0ck_v0`:

```bash
python3 -m venv venv_name
```

Activate the virtual environment:

```bash
source venv_name/bin/activate
```

---

## Download Dependencies

The project uses **FastAPI** to make API requests and **Uvicorn** to load the frontend in development environment, locally.

Install them:

```bash
pip install fastapi uvicorn
```

---

## Project Launch

Once the virtual environment has been activated, execute the following:

```bash
cd backend
uvicorn main:app --reload
```

(Optional but Recommended) – In a new terminal, enable the `cl` shortcut to avoid typing long curl commands.

Add the `cl` script to your system once:

```bash
sudo cp cl /usr/local/bin/
sudo chmod +x /usr/local/bin/cl
```

Now you can use the `cl` command globally.

---

## API calls via Terminal using `curl`

---

> ***NOTE***
> The `cl` command is a helper wrapper for `curl` defined in the repo (`scripts/cl`).
> If installed as shown above, you can use `cl blockchain ...` instead of typing `curl http://127.0.0.1:8000/...`.
> For `POST` requests, simply use `cl ...` (no separate `clPost` needed).
> Change the port number in the script if 8000 is already in use.

---

### Root Welcome

```bash
curl http://127.0.0.1:8000/
```

### Get Entire Blockchain ⛓️🅱️⛓️

```bash
cl blockchain
```

---

```bash
curl http://127.0.0.1:8000/blockchain/
```

### Add a New Block to the Bl0ckchain 🅱️✅

```bash
cl blockchain add
```

---

```bash
curl -X POST http://127.0.0.1:8000/blockchain/add
```

### Get the last (latest) Bl0ck added to the system 🔗🅱️

```bash
cl blockchain last block
```

---

```bash
curl http://127.0.0.1:8000/blockchain/last-block
```

### Enable DDM (Dynamic Difficulty Mode) ⛓️🔄️✅

```bash
cl difficulty enable
```

---

```bash
curl -X POST http://127.0.0.1:8000/difficulty/enable
```

### Disable DDM (Dynamic Difficulty Mode) ⛓️🔄️❎

```bash
cl difficulty disable
```

---

```bash
curl -X POST http://127.0.0.1:8000/difficulty/disable
```

### Set Manual Difficulty (1 - 10) 1️⃣-🔟

```bash
cl difficulty set manual {Value}
```

---

```bash
curl -X POST http://127.0.0.1:8000/difficulty/set-manual/{Value}
```

### Switch to Auto Mode 🔄️✅

```bash
cl difficulty switch to auto
```

---

```bash
curl -X POST http://127.0.0.1:8000/difficulty/switch-to-auto
```

### Set Mining Timeout (10 - 300 seconds) 🕛⁉️

```bash
cl mining set-timeout {Value}
```

---

```bash
curl -X POST http://127.0.0.1:8000/mining/set-timeout/{Value}
```