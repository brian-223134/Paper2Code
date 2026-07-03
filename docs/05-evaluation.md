# 05. 생성 저장소 평가 (모델 기반)

PaperCoder가 생성한 저장소의 품질을 **LLM(o3-mini-high)** 을 심사자로 사용해 평가합니다.
모델이 핵심 구현 요소를 비평하고 심각도(severity)를 매긴 뒤, **1~5점의 정확도(correctness) 점수**를
**8회 샘플 평균**으로 산출합니다. 관련 코드는 [`codes/eval.py`](../codes/eval.py)입니다.

## 두 가지 평가 방식

| 방식 | 설명 | 필요한 것 |
|------|------|-----------|
| **Reference-free** (`ref_free`) | 논문 내용만으로 생성 저장소를 평가 | 논문 JSON + 생성 저장소 |
| **Reference-based** (`ref_based`) | 저자 공식 코드(gold)와 대조하여 평가 | 위 + gold 저장소 |

평가 프롬프트는 [`data/prompts/ref_free.txt`](../data/prompts/ref_free.txt),
[`data/prompts/ref_based.txt`](../data/prompts/ref_based.txt)에 정의되어 있습니다.

## 환경 설정

```bash
pip install tiktoken
export OPENAI_API_KEY="<OPENAI_API_KEY>"
```

## Reference-free 평가

```bash
cd codes/
python eval.py \
    --paper_name Transformer \
    --pdf_json_path ../examples/Transformer_cleaned.json \
    --data_dir ../data \
    --output_dir ../outputs/Transformer \
    --target_repo_dir ../outputs/Transformer_repo \
    --eval_result_dir ../results \
    --eval_type ref_free \
    --generated_n 8 \
    --papercoder
```

## Reference-based 평가

`--gold_repo_dir`에 저자 공식 저장소 경로를 추가로 지정합니다.

```bash
cd codes/
python eval.py \
    --paper_name Transformer \
    --pdf_json_path ../examples/Transformer_cleaned.json \
    --data_dir ../data \
    --output_dir ../outputs/Transformer \
    --target_repo_dir ../outputs/Transformer_repo \
    --gold_repo_dir ../examples/Transformer_gold_repo \
    --eval_result_dir ../results \
    --eval_type ref_based \
    --generated_n 8 \
    --papercoder
```

## 주요 인자

| 인자 | 의미 |
|------|------|
| `--target_repo_dir` | 평가 대상(생성된) 저장소 |
| `--gold_repo_dir` | 저자 공식 저장소 (ref_based 전용) |
| `--eval_type` | `ref_free` 또는 `ref_based` |
| `--generated_n` | 평가 샘플 수(기본 8, 평균 점수 산출) |
| `--papercoder` | PaperCoder 산출물(`planning_config.yaml` 등)을 함께 읽어 평가 |

## 출력 예시

```
========================================
🌟 Evaluation Summary 🌟
📄 Paper name: Transformer
🧪 Evaluation type: ref_based
📁 Target repo directory: ../outputs/Transformer_repo
📊 Evaluation result:
        📈 Score: 4.5000
        ✅ Valid: 8/8
========================================
🌟 Usage Summary 🌟
🛠️ Model: o3-mini
💵 Current total cost: $0.16451380
============================================
```

- **Score**: 1~5점 정확도 평균
- **Valid**: 유효하게 채점된 샘플 수 / 전체 샘플 수

자세한 방법론은 논문의 Section 4.3.1 (*Paper2Code Benchmark*)을 참고하세요.
