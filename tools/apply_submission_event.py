import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


LEADERBOARD_COLUMNS = [
    "place",
    "name",
    "annual_return_pct",
    "ema_fast",
    "ema_slow",
    "bb_window",
    "bb_dev",
    "timeframe_min",
    "max_drawdown_pct",
    "trades",
    "total_return_pct",
    "days_back",
    "figi",
    "timestamp_utc",
    "run_id",
]

README_LB_START = "<!-- LEADERBOARD:START -->"
README_LB_END = "<!-- LEADERBOARD:END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply backtest submission payload and rebuild leaderboard/readme.")
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--leaderboard-path", type=Path, default=Path("reports/leaderboard.json"))
    parser.add_argument("--readme-path", type=Path, default=Path("README.md"))
    parser.add_argument("--readme-table-limit", type=int, default=20)
    return parser.parse_args()


def _to_float(v, default: float = -10_000.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def _to_int(v, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default


def ensure_columns(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        item = {}
        for col in LEADERBOARD_COLUMNS:
            item[col] = row.get(col, "")
        out.append(item)
    return out


def rank_best_only(rows: list[dict]) -> list[dict]:
    rows = ensure_columns(rows)
    for row in rows:
        row["name"] = str(row.get("name", "")).strip()
        row["annual_return_pct"] = _to_float(row.get("annual_return_pct"))
        row["max_drawdown_pct"] = _to_float(row.get("max_drawdown_pct"))
        row["trades"] = _to_int(row.get("trades"))
        row["timestamp_utc"] = str(row.get("timestamp_utc", ""))

    rows.sort(
        key=lambda r: (
            r["annual_return_pct"],
            r["max_drawdown_pct"],
            r["trades"],
            r["timestamp_utc"],
        ),
        reverse=True,
    )

    best = {}
    for row in rows:
        key = row["name"].lower()
        if key and key not in best:
            best[key] = row

    ranked = list(best.values())
    ranked.sort(
        key=lambda r: (
            r["annual_return_pct"],
            r["max_drawdown_pct"],
            r["trades"],
            r["timestamp_utc"],
        ),
        reverse=True,
    )

    for i, row in enumerate(ranked, start=1):
        row["place"] = i
    return ranked


def render_readme_leaderboard(rows: list[dict], table_limit: int, generated_utc: str) -> str:
    lines = [
        README_LB_START,
        "## Актуальный Лидерборд",
        "",
        f"Автоматически обновляется после каждого бэктеста. Последнее обновление: `{generated_utc}` UTC.",
        "",
        "| Место | Участник | CAGR % | Макс. просадка % | Сделки | EMA Fast | EMA Slow | BB Window | BB Dev | ТФ (мин) |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    top = rows[:table_limit]
    if not top:
        lines.append("| - | - | - | - | - | - | - | - | - | - |")
    else:
        for row in top:
            lines.append(
                f"| {row['place']} | {row['name']} | "
                f"{_to_float(row['annual_return_pct'], 0.0):.2f} | "
                f"{_to_float(row['max_drawdown_pct'], 0.0):.2f} | "
                f"{_to_int(row['trades'], 0)} | "
                f"{row['ema_fast']} | {row['ema_slow']} | {row['bb_window']} | {row['bb_dev']} | {row['timeframe_min']} |"
            )
    lines.append("")
    lines.append(README_LB_END)
    return "\n".join(lines)


def inject_readme_block(text: str, block: str) -> str:
    pattern = re.compile(rf"{re.escape(README_LB_START)}.*?{re.escape(README_LB_END)}", flags=re.S)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    suffix = "" if text.endswith("\n") else "\n"
    return f"{text}{suffix}\n{block}\n"


def main() -> None:
    args = parse_args()
    payload = json.loads(args.payload.read_text(encoding="utf-8-sig"))
    if "record" not in payload or not isinstance(payload["record"], dict):
        raise ValueError("Payload must contain object field 'record'")

    record = payload["record"]
    rows = []
    if args.leaderboard_path.exists():
        try:
            data = json.loads(args.leaderboard_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                rows = data
        except Exception:
            rows = []
    rows.append(record)

    ranked = rank_best_only(rows)
    args.leaderboard_path.parent.mkdir(parents=True, exist_ok=True)
    args.leaderboard_path.write_text(
        json.dumps(ensure_columns(ranked), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    generated_utc = str(record.get("timestamp_utc") or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    readme = args.readme_path.read_text(encoding="utf-8") if args.readme_path.exists() else "# MarketLab Arena\n"
    block = render_readme_leaderboard(ranked, args.readme_table_limit, generated_utc)
    updated = inject_readme_block(readme, block)
    args.readme_path.write_text(updated, encoding="utf-8")

    print(f"Leaderboard rows: {len(ranked)}")
    print(f"Updated: {args.leaderboard_path}")
    print(f"Updated: {args.readme_path}")


if __name__ == "__main__":
    main()
