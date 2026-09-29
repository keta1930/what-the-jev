"""下载 Hugging Face GSM8K leaderboard 聚合结果，保存为最新快照。

数据源是 Hub 的聚合接口，由各模型仓库的 .eval_results/ 与社区 PR 汇总而成，
内容随时间变化、无法固定 revision。固定写到 leaderboard-latest.json，重跑即
覆盖，始终只保留最新一份；历史版本由 git 记录。

按 openai/gsm8k 数据集页的 leaderboard_max_params=32B 视图取数，即只收录
参数量不超过 32B 的模型，对应接口查询参数 ?max_params=32B。
"""

import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

URL = 'https://huggingface.co/api/datasets/openai/gsm8k/leaderboard?max_params=32B'
PREPARATION = Path(__file__).resolve().parents[1]
RAW_PATH = PREPARATION / 'raw/leaderboard-latest.json'
EXPECTED_FIELDS = {'modelId', 'value'}


def fetch_leaderboard() -> list[dict[str, Any]]:
    """下载 leaderboard 聚合 JSON，核对基本结构。"""
    with urlopen(URL, timeout=60) as response:
        data = json.load(response)
    if not isinstance(data, list) or not data:
        raise ValueError(f'leaderboard 响应异常：{type(data).__name__}')
    bad = [index for index, row in enumerate(data) if not EXPECTED_FIELDS <= set(row)]
    if bad:
        raise ValueError(f'第 {bad[:3]} 条记录缺少必填字段')
    return data


def write_json(path: Path, value: Any) -> None:
    """写出 JSON，保留非 ASCII 字符与键序。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as file:
        json.dump(value, file, ensure_ascii=False, indent=2, allow_nan=False)
        file.write('\n')


def main() -> None:
    """下载并覆盖写出最新快照。"""
    rows = fetch_leaderboard()
    write_json(RAW_PATH, rows)
    print(f'leaderboard {len(rows)} 条：{RAW_PATH}')


if __name__ == '__main__':
    main()
