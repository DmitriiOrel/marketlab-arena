# TradeSavvy Sandbox Starter

Учебный репозиторий для запуска торгового бота в песочнице T-Invest, проведения бэктестов и ведения лидерборда на GitHub.

<!-- LEADERBOARD:START -->
## Актуальный Лидерборд

Автоматически обновляется после каждого бэктеста. Последнее обновление: `20260219T113648Z` UTC.

| Место | Участник | CAGR % | Макс. просадка % | Сделки | EMA Fast | EMA Slow | BB Window | BB Dev | ТФ (мин) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | dmitrii | 39.50 | -11.83 | 81 | 30 | 40 | 20 | 1.0 | 60 |

<!-- LEADERBOARD:END -->

## Быстрый Старт (Windows PowerShell)

```powershell
git clone https://github.com/DmitriiOrel/winter_school_project.git
cd .\winter_school_project
.\quickstart.ps1 -Token "t.ВАШ_API_ТОКЕН"
```

Токен указывается в сыром виде: `t.xxxxx` (без `< >` и без пробелов).

## Единый Сценарий Запуска

В проекте используется один основной скрипт: `run_backtest_manual.ps1`.

Скрипт выполняет полный цикл:
1. ручной бэктест за 3 года;
2. обновление лидерборда в GitHub (режим `best-only`: сохраняется только лучший результат участника);
3. обновление таблицы лидерборда в `README.md`;
4. сохранение артефактов trial в `reports/<user>/trial_<run_id>`;
5. обязательный запуск sandbox-бота.

### Команда запуска

```powershell
$env:GITHUB_TOKEN="github_pat_ВАШ_PAT"
.\run_backtest_manual.ps1 20 50 20 2.0 60 -Name dmitrii
```

## Структура Артефактов

### Лидерборд

- Основной файл лидерборда в GitHub: `reports/leaderboard.json`.
- Формат: JSON-массив записей.
- Логика отбора: `best-only` по полю участника `name`.

### Артефакты участника

Для каждого участника формируется папка:
- `reports/<user>/trials_index.json` - индекс запусков, отсортированный по доходности;
- `reports/<user>/trial_<run_id>/summary.json` - параметры и метрики стратегии;
- `reports/<user>/trial_<run_id>/backtest.png` - график бэктеста;
- `reports/<user>/trial_<run_id>/trades.csv` - журнал сделок.
