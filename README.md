# TradeSavvy Sandbox Starter

Minimal training project to run a trading bot in T-Invest Sandbox.

## Quick Start (Windows PowerShell)

```powershell
git clone https://github.com/DmitriiOrel/winter_school_project.git
cd .\winter_school_project
.\quickstart.ps1 -Token "t.YOUR_API_TOKEN" -Run
```

Token format: use the raw token only (`t.xxxxx`).
Do not wrap token with `< >`.

## What quickstart does

- Creates `.venv`
- Installs dependencies
- Installs T-Invest SDK (`tinkoff.invest`)
- Creates/finds sandbox account
- Writes `.env` with `TOKEN`, `ACCOUNT_ID`, `SANDBOX=True`

## Run later

```powershell
.\run_sandbox.ps1
```

Stop: `Ctrl+C`.

## If script execution is blocked

```powershell
powershell -ExecutionPolicy Bypass -File .\quickstart.ps1 -Token "t.YOUR_API_TOKEN" -Run
```

## Notes

- Sandbox only (`SANDBOX=True`): virtual trades.
- Do not commit `.env`, `stats.db`, `market_data_cache`, `reports`.