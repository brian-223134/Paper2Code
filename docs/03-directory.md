# 03. 디렉토리 및 파일 구조

## 최상위 구조

```
Paper2Code/
├── README.md              # 프로젝트 소개 및 사용법(원본)
├── LICENSE
├── requirements.txt       # openai, vllm, transformers, tiktoken
├── assets/                # 문서용 이미지 (papercoder_overview.png)
├── codes/                 # 핵심 파이프라인 스크립트
├── scripts/               # 실행 진입점 (bash)
├── data/                  # 벤치마크 데이터셋 + 평가 프롬프트
├── examples/              # 예제 논문(Transformer) 입력 파일
└── docs/                  # (이 문서 디렉토리)
```

## `codes/` — 파이프라인 스크립트

| 파일 | 역할 |
|------|------|
| [`0_pdf_process.py`](../codes/0_pdf_process.py) | 논문 JSON 전처리(정제) |
| [`1_planning.py`](../codes/1_planning.py) | ① 계획: 로드맵·설계·작업목록·config 생성 |
| [`1.1_extract_config.py`](../codes/1.1_extract_config.py) | 계획 결과에서 `config.yaml` 추출 + 아티팩트 저장 |
| [`1.2_rag_config.py`](../codes/1.2_rag_config.py) | (확장) RAG 기반 config 처리 |
| [`2_analyzing.py`](../codes/2_analyzing.py) | ② 분석: 파일별 상세 로직 분석 |
| [`3_coding.py`](../codes/3_coding.py) | ③ 코드 생성: 파일별 코드 작성 |
| [`3.1_coding_sh.py`](../codes/3.1_coding_sh.py) | (확장) 코딩 보조 스크립트 |
| [`4_debugging.py`](../codes/4_debugging.py) | (확장) 생성 코드 디버깅 단계 |
| [`*_llm.py`](../codes) | 위 단계들의 vLLM(오픈소스 모델) 변형 |
| [`eval.py`](../codes/eval.py) | 생성 저장소의 모델 기반 평가 |
| [`utils.py`](../codes/utils.py) | 공통 유틸(파싱, 비용 로깅, 파일 IO 등) |

## `scripts/` — 실행 진입점

| 스크립트 | 입력 형식 | 모델 |
|----------|-----------|------|
| [`run.sh`](../scripts/run.sh) | PDF→JSON | OpenAI API (o3-mini) |
| [`run_latex.sh`](../scripts/run_latex.sh) | LaTeX | OpenAI API |
| [`run_llm.sh`](../scripts/run_llm.sh) | PDF→JSON | vLLM (DeepSeek-Coder) |
| [`run_latex_llm.sh`](../scripts/run_latex_llm.sh) | LaTeX | vLLM |

각 스크립트 상단에서 `PAPER_NAME`, `PDF_JSON_PATH`, `OUTPUT_DIR` 등의 환경 변수를
설정한 뒤 `0 → 1 → 1.1 → 2 → 3` 순으로 파이썬 스크립트를 호출합니다.

## `data/`

```
data/
├── paper2code/            # Paper2Code 벤치마크 데이터셋
│   ├── README.md
│   ├── dataset_info.json
│   └── paper2code_data.zip
└── prompts/               # 평가용 프롬프트
    ├── ref_based.txt      # 참조 기반(gold 코드 대조) 평가 프롬프트
    └── ref_free.txt       # 참조 없는(논문만으로) 평가 프롬프트
```

## `examples/` — 예제 논문 (Attention Is All You Need)

```
examples/
├── Transformer.pdf            # 원본 PDF
├── Transformer.json           # s2orc-doc2json 변환 결과
├── Transformer_cleaned.json   # 전처리(정제)된 JSON  ← 파이프라인 입력
└── Transformer_cleaned.tex    # LaTeX 소스 입력용
```

## 실행 시 생성되는 출력 구조

파이프라인을 실행하면 `outputs/` 아래에 다음이 만들어집니다.

```
outputs/
├── Transformer/                   # 중간 산출물(OUTPUT_DIR)
│   ├── planning_artifacts/        #  ① 계획 결과(사람이 읽는 형태)
│   ├── analyzing_artifacts/       #  ② 파일별 분석
│   ├── coding_artifacts/          #  ③ 파일별 코딩 로그
│   ├── planning_config.yaml       #  추출된 설정
│   ├── planning_trajectories.json #  계획 단계 전체 대화
│   └── accumulated_cost.json      #  누적 비용
└── Transformer_repo/              # 최종 재현 코드 저장소(OUTPUT_REPO_DIR)
    ├── config.yaml
    └── ... (생성된 소스 파일들)
```
