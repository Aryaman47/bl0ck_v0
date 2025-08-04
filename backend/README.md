# API calls via Powershell Terminal using curl.exe

## Root Welcome 
`curl.exe https://127.0.0.1:8000/`

## Get Entire Blockchain ⛓️🅱️⛓️
### All Existing Bl0cks generated
`curl.exe http://127.0.0.1:8000/blockchain`

## Add a New Block to the Bl0ckchain 🅱️✅
`curl.exe -X POST http://127.0.0.1:8000/blockchain/add`

## Get the last (latest) Bl0ck added to the system 🔗🅱️
`curl.exe -X POST http://127.0.0.1:8000/blockchin/last-block`

## Enable DDM (Dynamic Difficulty Mode)
`curl.exe -X POST http://127.0.0.1:8000/difficulty/enable`

# Disable DDM (Dynamic Difficulty Mode)
`curl.exe -X POST http://127.0.0.1:8000/difficulty/disable`

# Set Manual Difficulty (1 - 10)
`curl.exe -X POST http://127.0.0.1:8000/difficulty/set-manual/4`

# Switch to Auto Mode
`curl.exe -X POST http://127.0.0.1:8000/difficulty/switch-to-auto`

# Set Mining Timeout (10 - 300 seconds)

`curl.exe -X POST http://127.0.0.1:8000/mining/set-timeout/{Replace-with-Timeout-Value-Here}`