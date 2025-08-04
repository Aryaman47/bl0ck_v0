# API calls via Powershell Terminal using curl.exe

## 1. Root Welcome 
`curl.exe https://127.0.0.1:8000/`

## 2. Get Entire Blockchain ⛓️🅱️⛓️
`curl.exe http://127.0.0.1:8000/blockchain`

## 3. Add a New Block to the Bl0ckchain 🅱️✅
`curl.exe -X POST http://127.0.0.1:8000/blockchain/add`

## 4. Get the last (latest) Bl0ck added to the system 🔗🅱️
`curl.exe -X POST http://127.0.0.1:8000/blockchin/last-block`

## 5. Enable DDM (Dynamic Difficulty Mode)
`curl.exe -X POST http://127.0.0.1:8000/difficulty/enable`

# 6. Disable DDM (Dynamic Difficulty Mode)
`curl.exe -X POST http://127.0.0.1:8000/difficulty/disable`

# 7. Set Manual Difficulty (1 - 10)
`curl.exe -X POST http://127.0.0.1:8000/difficulty/set-manual/4`

# 8. Switch to Auto Mode
`curl.exe -X POST http://127.0.0.1:8000/difficulty/switch-to-auto`

# 9. Set Mining Timeout (10 - 300 seconds)

`curl.exe -X POST http://127.0.0.1:8000/mining/set-timeout/{Replace-with-Timeout-Value-Here}`