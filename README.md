# TradeSavvy Sandbox Starter

Учебный репозиторий для запуска торгового бота в Sandbox T-Invest.

## 2 шага для студента (Windows PowerShell)

```powershell
git clone https://github.com/DmitriiOrel/winter_school_project.git
cd .\winter_school_project
.\quickstart.ps1 -Token "t.<YOUR_API_TOKEN>" -Run
```

Что делает `quickstart.ps1`:
- создает `.venv`;
- ставит зависимости;
- создает/находит sandbox-аккаунт;
- записывает `.env` (`TOKEN`, `ACCOUNT_ID`, `SANDBOX=True`);
- при флаге `-Run` сразу запускает бота.

## Повторный запуск

```powershell
cd .\winter_school_project
.\run_sandbox.ps1
```

Остановка: `Ctrl+C`.

## Если PowerShell блокирует скрипты

```powershell
powershell -ExecutionPolicy Bypass -File .\quickstart.ps1 -Token "t.<YOUR_API_TOKEN>" -Run
```

## Что настраивается руками

Только API-токен.

## Основные файлы

- `quickstart.ps1` - one-shot установка и настройка.
- `run_sandbox.ps1` - запуск бота в sandbox.
- `app/main.py` - entrypoint.
- `instruments_config_scalpel.json` - инструмент и параметры стратегии.

## Важно

- Песочница: сделки виртуальные (`SANDBOX=True`).
- Не коммитьте `.env` и кэш.