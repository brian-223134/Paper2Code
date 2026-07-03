# test/ — 유닛 테스트

`codes/utils.py`의 **순수 함수**(외부 API·GPU 불필요, 결정적)에 대한 회귀 안전망.
[docs/06-reproduction-gap.md](../docs/06-reproduction-gap.md)의 gap ①(실행·디버깅 루프) 정비에
앞서, 파이프라인 전 단계가 공통 의존하는 유틸부터 테스트로 고정한다.

## 실행 방법

```bash
pip install -r test/requirements-test.txt
pytest test/            # 저장소 루트에서
```

## 구조

```
test/
├── conftest.py              # codes/ 를 sys.path 에 추가
├── requirements-test.txt    # pytest
├── fixtures/                # 샘플 입력 (planning_trajectories.json 등)
├── unit/                    # utils.py 순수 함수 테스트
│   ├── test_json_parsing.py     # content_to_json / content_to_json4
│   ├── test_extract_code.py     # extract_code_from_content*, extract_json_from_string
│   ├── test_cost.py             # cal_cost, load/save_accumulated_cost
│   └── test_misc.py             # format_json_data, extract_planning, get_now_str
└── integration/            # (추후) 파이프라인 단계 스모크 테스트 자리
```

## 범위 밖 (아직 미포함)

- `4_debugging.py:138` 의 `--output_repo_dir` 인자 누락 버그 수정
- 실제 데이터셋 / 하이퍼파라미터 / GPU (논문별·외부 리소스 필요)
