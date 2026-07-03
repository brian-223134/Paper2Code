"""utils.cal_cost / load_accumulated_cost / save_accumulated_cost 테스트.

토큰 사용량 → 비용 계산 및 누적 비용 저장/로드. 비용 발생 작업의 회계 로직이라
회귀 시 조용히 잘못된 금액을 기록할 수 있어 고정해 둔다.
"""
import math

import pytest

import utils


def _usage(prompt_tokens, completion_tokens, cached_tokens=0):
    return {
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "prompt_tokens_details": {"cached_tokens": cached_tokens},
        }
    }


def test_cal_cost_o3_mini_with_cached_tokens():
    # o3-mini 단가: input 1.10, cached 0.55, output 4.40 (per 1M tokens)
    res = utils.cal_cost(_usage(1000, 500, cached_tokens=200), "o3-mini")

    assert res["actual_input_tokens"] == 800   # prompt - cached
    assert res["cached_tokens"] == 200
    assert res["output_tokens"] == 500

    assert math.isclose(res["input_cost"], 800 / 1_000_000 * 1.10)
    assert math.isclose(res["cached_input_cost"], 200 / 1_000_000 * 0.55)
    assert math.isclose(res["output_cost"], 500 / 1_000_000 * 4.40)
    assert math.isclose(
        res["total_cost"],
        res["input_cost"] + res["cached_input_cost"] + res["output_cost"],
    )


def test_cal_cost_defaults_cached_to_zero_when_absent():
    res = utils.cal_cost(_usage(1000, 100), "o3-mini")
    assert res["cached_tokens"] == 0
    assert res["cached_input_cost"] == 0.0
    assert res["actual_input_tokens"] == 1000


def test_cal_cost_unknown_model_raises():
    with pytest.raises(KeyError):
        utils.cal_cost(_usage(10, 10), "made-up-model")


def test_accumulated_cost_roundtrip(tmp_path):
    f = tmp_path / "accumulated_cost.json"
    utils.save_accumulated_cost(str(f), 1.2345)
    assert math.isclose(utils.load_accumulated_cost(str(f)), 1.2345)


def test_load_accumulated_cost_missing_file_returns_zero(tmp_path):
    missing = tmp_path / "does_not_exist.json"
    assert utils.load_accumulated_cost(str(missing)) == 0.0
