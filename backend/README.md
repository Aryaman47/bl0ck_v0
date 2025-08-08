# API calls via Powershell Terminal using curl.exe

**_NOTE_** Execute ". ./profile-curl.ps1" to use cl and clPost to avoid using "curl.exe http://127.0.0.1:8000/" and "curl.exe -X POST http://127.0.0.1:8000/, respectively. Change the port number in profile-curl.ps1, in case the default is busy."


## 1. Root Welcome 
`cl = curl.exe http://127.0.0.1:8000/`

## 2. Get Entire Blockchain ⛓️🅱️⛓️
`cl blockchain/ = curl.exe http://127.0.0.1:8000/blockchain/`

## 3. Add a New Block to the Bl0ckchain 🅱️✅
`clPost blockchain/add = curl.exe -X POST http://127.0.0.1:8000/blockchain/add`

## 4. Get the last (latest) Bl0ck added to the system 🔗🅱️
`cl blockchain/last-block = curl.exe http://127.0.0.1:8000/blockchain/last-block`

## 5. Enable DDM (Dynamic Difficulty Mode)
`clPost difficulty/enable = curl.exe -X POST http://127.0.0.1:8000/difficulty/enable`

# 6. Disable DDM (Dynamic Difficulty Mode)
`clPost difficulty/disable = curl.exe -X POST http://127.0.0.1:8000/difficulty/disable`

# 7. Set Manual Difficulty (1 - 10)
`clPost difficulty/set-manual/{Value} = curl.exe -X POST http://127.0.0.1:8000/difficulty/set-manual/{Value}`

# 8. Switch to Auto Mode
`clPost difficulty/switch-to-auto = curl.exe -X POST http://127.0.0.1:8000/difficulty/switch-to-auto`

# 9. Set Mining Timeout (10 - 300 seconds)

`clPost mining/set-timeout/{Value} = curl.exe -X POST http://127.0.0.1:8000/mining/set-timeout/{Value}`