# 02. 아키텍처: 3단계 멀티 에이전트 파이프라인

PaperCoder는 전처리(0단계) 후, 핵심 3단계(Planning → Analysis → Coding)를 거칩니다.
각 단계의 코드는 [`codes/`](../codes) 아래에 있으며, `..._llm.py`는 오픈소스(vLLM) 모델용 변형입니다.

전체 실행 순서는 [`scripts/run.sh`](../scripts/run.sh)에 정의되어 있습니다.

```
0_pdf_process.py         # 전처리: 논문 JSON 정제
        │
1_planning.py            # ① 계획 (4개 하위 단계)
1.1_extract_config.py    #    planning 결과에서 config.yaml 추출
        │
2_analyzing.py           # ② 분석 (파일별 로직 분석)
        │
3_coding.py              # ③ 코드 생성 (파일별 코드 작성)
```

> 참고: [`4_debugging.py`](../codes/4_debugging.py), [`3.1_coding_sh.py`](../codes/3.1_coding_sh.py),
> [`1.2_rag_config.py`](../codes/1.2_rag_config.py)는 기본 `run.sh` 파이프라인에는 포함되지 않은
> 확장/보조 스크립트입니다.

---

## 0단계: 전처리 ([`0_pdf_process.py`](../codes/0_pdf_process.py))

s2orc-doc2json으로 변환한 논문 JSON에서 불필요한 부분을 제거해 정제된
`*_cleaned.json`을 만듭니다. 이후 모든 단계는 이 정제된 논문 내용을 컨텍스트로 사용합니다.

---

## ① Planning 단계 ([`1_planning.py`](../codes/1_planning.py))

하나의 대화 세션 안에서 네 개의 프롬프트를 **순차적으로 누적(trajectory)** 하며 진행합니다.
각 응답이 다음 프롬프트의 컨텍스트가 되어, 점점 구체적인 설계로 좁혀 갑니다.

| 하위 단계 | 프롬프트 역할 | 산출물 |
|-----------|---------------|--------|
| 1. Overall plan | 논문 방법론·실험을 재현하기 위한 전체 로드맵 작성 | 자연어 계획 |
| 2. Architecture design | 파일 목록, 클래스 다이어그램(mermaid), 호출 흐름 설계 | JSON 설계 (`File list` 등) |
| 3. Logic design | 작업(task) 목록과 파일 간 의존성·로직 분석 | JSON (`Task list`, `Logic Analysis`, `Required packages`) |
| 4. Config generation | 논문에서 학습 하이퍼파라미터 등을 추출해 `config.yaml` 작성 | `config.yaml` (YAML) |

- 시스템 프롬프트는 "재현성에 정통한 전문 연구자이자 전략 기획자" 역할을 부여합니다.
- 설계·작업 목록은 정해진 `[CONTENT]...[/CONTENT]` JSON 포맷으로 강제하여 후속 파싱을 쉽게 합니다.
- 설정 생성 시 **"논문에 없는 값을 지어내지 말 것(DO NOT FABRICATE)"** 을 명시합니다.
- 결과는 `planning_response.json`(응답)과 `planning_trajectories.json`(전체 대화)으로 저장됩니다.

### 1.1 Config 추출 ([`1.1_extract_config.py`](../codes/1.1_extract_config.py))

`planning_trajectories.json`의 마지막 turn(설정 생성 응답)에서 ` ```yaml ... ``` ` 블록을
정규식으로 추출하여 `planning_config.yaml`로 저장합니다. 또한 계획 산출물을
읽기 좋은 텍스트로 정리해 `planning_artifacts/`에 남깁니다(전체 계획, 아키텍처 설계, 로직 설계, config).

이렇게 만들어진 `planning_config.yaml`은 최종 저장소의 `config.yaml`로 복사되어,
이후 분석·코딩 단계가 **모든 설정값을 이 파일에서만 참조**하도록 합니다.

---

## ② Analysis 단계 ([`2_analyzing.py`](../codes/2_analyzing.py))

Planning에서 만든 **작업 목록(Task list)의 각 파일**에 대해, 코드를 쓰기 전에
"이 파일을 어떻게 구현할지"에 대한 **상세 로직 분석**을 개별적으로 생성합니다.

- 입력 컨텍스트: 논문 + 전체 계획 + 아키텍처 설계 + 작업 목록 + `config.yaml`
- 각 파일마다 독립된 대화로 분석을 수행(파일별로 trajectory를 복사해 사용).
- 제약: **설계(Data structures and interfaces)를 절대 변경하지 말 것**, **`config.yaml`의 설정만 사용할 것**.
- 산출물:
  - `analyzing_artifacts/<파일>_simple_analysis.txt` (사람이 읽는 용)
  - `<파일>_simple_analysis_response.json` / `_trajectories.json` (다음 단계 입력용)

---

## ③ Coding 단계 ([`3_coding.py`](../codes/3_coding.py))

작업 목록의 파일들을 **의존성 순서대로** 하나씩 실제 코드로 작성합니다.

- 입력 컨텍스트: 논문 + 계획 + 설계 + 작업 목록 + `config.yaml` +
  **이미 작성 완료된 파일들의 코드** + 해당 파일의 상세 로직 분석(②의 결과).
- 즉, 앞서 만든 파일 코드를 계속 컨텍스트에 넣어 **일관성 있는 프로젝트**를 구성합니다.
- 코드 작성 규칙(프롬프트에 명시):
  1. 한 번에 **한 파일만** 완전히 구현
  2. TODO 없이 **완결된 코드** 작성
  3. 설계를 벗어나지 말고, 존재하지 않는 메서드 사용 금지
  4. 설정값은 반드시 `config.yaml`에서 참조(임의 값 금지)
- 응답에서 ` ```python ``` ` 코드 블록을 추출(`extract_code_from_content`)해
  `output_repo_dir`(예: `Transformer_repo/`)의 해당 경로에 파일로 저장합니다.
- 산출물: 최종 저장소의 소스 파일들 + `coding_artifacts/<파일>_coding.txt`

---

## 비용 추적

모든 단계는 `utils.py`의 `print_log_cost` / `load_accumulated_cost` /
`save_accumulated_cost`를 사용해 토큰 사용량과 누적 비용을 `accumulated_cost.json`에 기록합니다.
(o3-mini 기준 논문 1편 처리 예상 비용 약 $0.50–0.70)

---

## 오픈소스(vLLM) 변형

`1_planning_llm.py`, `2_analyzing_llm.py`, `3_coding_llm.py`는 위와 동일한 파이프라인을
OpenAI API 대신 vLLM 로컬 추론으로 실행하는 버전입니다. 프롬프트 구성과 산출물 형식은 동일합니다.
