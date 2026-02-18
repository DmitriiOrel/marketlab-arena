# TradeSavvy Sandbox Starter

Учебный репозиторий для запуска торгового бота в Sandbox T-Invest.

## Что внутри

- Готовая стратегия `scalpel` (EMA 20/50 + Bollinger).
- Автоматический quickstart-скрипт для Windows.
- Визуализация и бэктест: `tools/plot_scalpel_report.py`.

## Быстрый старт (Windows PowerShell)

1. Клонируй репозиторий:

```powershell
git clone <YOUR_GIT_URL>
cd .\TradeSavvyGitReady
```

2. Выполни one-shot установку (создаст `.venv`, установит зависимости, откроет/найдет sandbox-аккаунт и запишет `.env`):

```powershell
.\quickstart.ps1 -Token "t.<YOUR_API_TOKEN>"
```

3. Запусти бота:

```powershell
.\run_sandbox.ps1
```

Остановка: `Ctrl+C`.

## Что нужно заполнить руками

Ничего, кроме `TOKEN` (в параметре `-Token`).

`ACCOUNT_ID` заполняется автоматически в `.env`.

## Основные файлы

- `app/main.py` — запуск бота.
- `instruments_config_scalpel.json` — инструмент и параметры стратегии.
- `tools/get_accounts.py` — проверка sandbox-аккаунтов.
- `tools/get_figi.py` — поиск FIGI по тикеру.
- `tools/plot_scalpel_report.py` — отчеты и графики.

## Параметры стратегии

Файл: `instruments_config_scalpel.json`

- `days_back_to_consider`
- `quantity_limit`
- `check_data`

Текущая логика EMA зафиксирована в коде:

- `EMA_fast = 20`
- `EMA_slow = 50`

Файл: `app/strategies/scalpel/scalpel.py`

## Бэктест и графики

Пример отчета за 2 года:

```powershell
.\.venv\Scripts\python.exe .\tools\plot_scalpel_report.py --source api --days-back 730 --interval 5min
```

## Публикация на GitHub

```powershell
git init
git add .
git commit -m "Initial sandbox starter"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## Важно

- Этот проект только для учебных целей.
- Перед переходом в реальный счет проверь риски и лимиты.
- Не публикуй `TOKEN` и файл `.env`.
