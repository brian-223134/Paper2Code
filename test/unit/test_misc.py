"""utils.format_json_data / extract_planning / get_now_str 테스트."""
import os
import re

import utils
from conftest import FIXTURES_DIR


def test_format_json_data_renders_keys_and_list_items():
    data = {"files": ["a.py", "b.py"], "note": "hello"}
    out = utils.format_json_data(data)
    assert "[files]" in out
    assert "- a.py" in out
    assert "- b.py" in out
    assert "[note]" in out
    assert "hello" in out


def test_extract_planning_takes_first_three_assistant_turns_and_strips_think():
    path = os.path.join(FIXTURES_DIR, "planning_trajectories.json")
    ctx = utils.extract_planning(path)

    assert len(ctx) == 3                      # [:3] — 4번째 assistant 턴은 버려짐
    assert ctx[0] == "OVERALL PLAN TEXT"      # <think>...</think> 제거됨
    assert ctx[1] == "ARCH DESIGN TEXT"
    assert ctx[2] == "LOGIC DESIGN TEXT"


def test_get_now_str_format():
    now = utils.get_now_str()
    # 예: 20250427_205124
    assert re.fullmatch(r"\d{8}_\d{6}", now)
