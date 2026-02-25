"""
共用測試 Fixtures 與設定。

職責：
- 註冊 @pytest.mark.slow 與 @pytest.mark.serial 標記
- 根據 .artifacts/test-durations.json 歷史耗時自動標記慢測試（無需手動標記）
- 測試完成後自動偵測慢測試候選（超過閾值）並提示
- 將測試耗時記錄至 .artifacts/test-durations.json 供追蹤

自動化流程：
  第一次執行 → 無歷史 → 全部一起跑 → 耗時記錄至 test-durations.json
  第二次起  → 讀取歷史 → 超閾值自動加 @pytest.mark.slow → code-check 分批生效
  手動標記  → @pytest.mark.slow / @pytest.mark.serial 仍然有效，且優先

測試標記指引（供 AI implement 參考）：
  @pytest.mark.slow    — 執行耗時 >SLOW_THRESHOLD_SECONDS（30s）的測試（支援自動標記）
  @pytest.mark.serial  — 使用共享資源（DB / 檔案 I/O / 網路 port）不可並行的測試
"""

import json
from pathlib import Path

import pytest

# ──────────────────────────────────────────────
# 慢測試閾值（秒）：超過此時間的測試將被自動標記為 @pytest.mark.slow
# 可在 pyproject.toml 中透過 [tool.pytest.ini_options] markers 覆寫
# ──────────────────────────────────────────────
SLOW_THRESHOLD_SECONDS = 30

# 耗時記錄檔路徑
_DURATIONS_FILE = Path(".artifacts/test-durations.json")


def pytest_configure(config):
    """註冊自訂 markers。"""
    config.addinivalue_line(
        "markers",
        "slow: 標記為慢測試（code-check 時串行執行，可用 -m 'not slow' 排除）",
    )
    config.addinivalue_line(
        "markers",
        "serial: 標記為不可並行測試（使用共享資源如 DB / 檔案 I/O / 網路 port）",
    )


def pytest_collection_modifyitems(config, items):
    """根據歷史耗時自動標記慢測試。

    讀取 .artifacts/test-durations.json（上次測試產出），
    將歷史耗時超過 SLOW_THRESHOLD_SECONDS 的測試自動加上 @pytest.mark.slow。
    已手動標記的測試不受影響。
    """
    if not _DURATIONS_FILE.exists():
        return  # 首次執行無歷史資料，全部一起跑

    try:
        historical = json.loads(_DURATIONS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return  # 檔案損壞或無法讀取，不影響測試執行

    slow_marker = pytest.mark.slow
    auto_marked_count = 0

    for item in items:
        # 已手動標記 slow 或 serial → 跳過
        if "slow" in item.keywords or "serial" in item.keywords:
            continue
        # 歷史耗時超過閾值 → 自動標記
        if item.nodeid in historical and historical[item.nodeid] >= SLOW_THRESHOLD_SECONDS:
            item.add_marker(slow_marker)
            auto_marked_count += 1

    if auto_marked_count > 0:
        # 透過 config 傳遞數量，供 terminal_summary 報告
        config._auto_marked_slow_count = auto_marked_count


@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, config):
    """測試結束後：回報自動標記統計 + 慢測試候選 + 產出耗時記錄檔。"""
    # 收集所有已完成的測試報告
    all_reports = terminalreporter.stats.get("passed", []) + terminalreporter.stats.get(
        "failed", []
    )

    # ── 0. 自動標記統計回報 ──
    auto_count = getattr(config, "_auto_marked_slow_count", 0)
    if auto_count > 0:
        terminalreporter.write_sep("=", "AUTO-MARKED SLOW TESTS")
        terminalreporter.write_line(
            f"  📌 {auto_count} test(s) auto-marked as @pytest.mark.slow "
            f"(based on historical durations >{SLOW_THRESHOLD_SECONDS}s)"
        )
        terminalreporter.write_line("")

    # ── 1. 慢測試候選回報（未被標記的新慢測試） ──
    slow_candidates = []
    for report in all_reports:
        if hasattr(report, "duration") and report.duration >= SLOW_THRESHOLD_SECONDS:
            slow_candidates.append((report.nodeid, report.duration))

    if slow_candidates:
        terminalreporter.write_sep(
            "=",
            f"SLOW TEST CANDIDATES (>{SLOW_THRESHOLD_SECONDS}s)",
        )
        for nodeid, duration in sorted(slow_candidates, key=lambda x: -x[1]):
            terminalreporter.write_line(f"  {duration:>8.2f}s  {nodeid}")
        terminalreporter.write_line("")
        terminalreporter.write_line(
            "💡 These will be auto-marked as @pytest.mark.slow on the next run"
        )
        terminalreporter.write_line(
            "   code-check will run them separately: fast tests (-n auto) → slow/serial tests (serial)"
        )

    # ── 2. 耗時記錄產出 ──
    all_durations = {}
    for report in all_reports:
        if hasattr(report, "duration"):
            all_durations[report.nodeid] = round(report.duration, 3)

    if all_durations:
        artifacts_dir = Path(".artifacts")
        artifacts_dir.mkdir(exist_ok=True)
        _DURATIONS_FILE.write_text(
            json.dumps(all_durations, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
