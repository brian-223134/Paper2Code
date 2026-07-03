# 04. 설치 및 실행 방법

## 1. 환경 설정

파이썬 가상환경 사용을 권장합니다. 필요에 따라 선택 설치합니다.

```bash
# OpenAI API 사용 시
pip install openai

# 오픈소스 모델(vLLM) 사용 시
pip install vllm

# 또는 전체 의존성 한 번에
pip install -r requirements.txt
```

`requirements.txt`: `openai>=1.65.4`, `vllm>=0.6.4.post1`, `transformers>=4.46.3`, `tiktoken>=0.9.0`

## 2. 빠른 시작 (예제: Transformer 논문)

### OpenAI API 사용 — 예상 비용 약 $0.50–0.70 (o3-mini)

```bash
export OPENAI_API_KEY="<OPENAI_API_KEY>"

cd scripts
bash run.sh
```

### 오픈소스 모델(vLLM) 사용 — 기본 `deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct`

```bash
cd scripts
bash run_llm.sh
```

실행이 끝나면 `outputs/Transformer_repo/`에 재현 코드 저장소가 생성됩니다.

## 3. 자신의 논문으로 실행하기

### (옵션) PDF → JSON 변환

논문 실험에서는 모든 PDF를 JSON으로 변환해 사용했습니다.
LaTeX 소스가 있다면 이 단계를 건너뛰고 LaTeX 실행 스크립트를 쓰면 됩니다.

```bash
# 1) 변환 도구 클론
git clone https://github.com/allenai/s2orc-doc2json.git

# 2) PDF 처리 서비스 실행
cd ./s2orc-doc2json/grobid-0.7.3
./gradlew run

# 3) PDF를 JSON으로 변환
mkdir -p ./s2orc-doc2json/output_dir/paper_coder
python ./s2orc-doc2json/doc2json/grobid2json/process_pdf.py \
    -i ${PDF_PATH} \
    -t ./s2orc-doc2json/temp_dir/ \
    -o ./s2orc-doc2json/output_dir/paper_coder
```

### 실행 스크립트 수정

`scripts/run.sh`(또는 다른 실행 스크립트) 상단의 환경 변수를 자신의 논문에 맞게 바꿉니다.

```bash
GPT_VERSION="o3-mini"
PAPER_NAME="MyPaper"
PDF_JSON_PATH="../examples/MyPaper.json"
PDF_JSON_CLEANED_PATH="../examples/MyPaper_cleaned.json"
OUTPUT_DIR="../outputs/MyPaper"
OUTPUT_REPO_DIR="../outputs/MyPaper_repo"
```

### 입력 형식별 스크립트 선택

| 입력 | OpenAI API | vLLM |
|------|-----------|------|
| PDF→JSON | `run.sh` | `run_llm.sh` |
| LaTeX | `run_latex.sh` | `run_latex_llm.sh` |

## 4. 참고 사항

- `o3-mini`를 쓰려면 최신 `openai` 패키지가 필요합니다.
- vLLM 설치 문제는 [공식 vLLM 저장소](https://github.com/vllm-project/vllm)를 참고하세요.
- 파이프라인은 각 단계 진행 상황과 누적 비용을 콘솔에 출력하고 `accumulated_cost.json`에 기록합니다.
