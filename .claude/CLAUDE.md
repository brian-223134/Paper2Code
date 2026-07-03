# Claude Code 작업 가이드

이 문서는 **Paper2Code / PaperCoder** 프로젝트에서 논문의 실험을 재현(reproduce)하는 작업을
Claude Code와 함께 진행할 때의 규칙과 맥락을 정의한다.
프로젝트의 상세 설명은 [`docs/`](../docs/README.md)를 참조한다.

---

## 프로젝트 개요

**PaperCoder**는 머신러닝 논문을 입력받아 **계획 → 분석 → 코드 생성** 3단계 멀티 에이전트
파이프라인으로 재현 코드 저장소를 자동 생성하는 시스템이다.

- ⚠️ **중요**: PaperCoder는 "실행 가능한 코드 초안"까지만 자동화하며, 코드를 실제로 실행해
  논문 수치를 재현하지는 않는다. 데이터셋·미기재 하이퍼파라미터·컴퓨트·실행/디버깅 루프는
  사용자 몫이다. 자세한 내용은 [`docs/06-reproduction-gap.md`](../docs/06-reproduction-gap.md) 참조.

---

## 디렉토리 구조

```
Paper2Code/
├── .claude/
│   └── CLAUDE.md          # (이 문서) Claude Code 작업 가이드
├── README.md              # 프로젝트 소개 및 사용법(원본)
├── LICENSE
├── requirements.txt       # openai, vllm, transformers, tiktoken
├── assets/                # 문서용 이미지
├── codes/                 # 핵심 파이프라인 스크립트
│   ├── 0_pdf_process.py         # 전처리: 논문 JSON 정제
│   ├── 1_planning.py            # ① 계획 (로드맵·설계·작업목록·config)
│   ├── 1.1_extract_config.py    #    계획 결과 → config.yaml 추출
│   ├── 1.2_rag_config.py        #    (확장) RAG 기반 config
│   ├── 2_analyzing.py           # ② 분석 (파일별 로직 분석)
│   ├── 3_coding.py              # ③ 코드 생성 (파일별 코드 작성)
│   ├── 3.1_coding_sh.py         #    (확장) reproduce.sh 생성
│   ├── 4_debugging.py           #    (확장) 실행 에러 기반 디버깅
│   ├── *_llm.py                 #    위 단계들의 vLLM(오픈소스) 변형
│   ├── eval.py                  # 생성 저장소 모델 기반 평가
│   └── utils.py                 # 공통 유틸(파싱·비용 로깅·IO)
├── scripts/               # 실행 진입점 (bash)
│   ├── run.sh                   # PDF→JSON + OpenAI API (기본)
│   ├── run_latex.sh            # LaTeX + OpenAI API
│   ├── run_llm.sh              # PDF→JSON + vLLM
│   └── run_latex_llm.sh       # LaTeX + vLLM
├── data/                  # 벤치마크 데이터셋 + 평가 프롬프트
│   ├── paper2code/             # Paper2Code 논문 텍스트 벤치마크(90편)
│   └── prompts/                # ref_based.txt / ref_free.txt
├── examples/              # 예제 논문(Transformer) 입력 파일
├── docs/                  # 프로젝트 설명 문서
└── outputs/               # (실행 시 생성) 중간 산출물 + 최종 저장소
    ├── <paper>/                # planning/analyzing/coding artifacts, config, cost
    └── <paper>_repo/           # 최종 재현 코드 저장소
```

파이프라인 실행 순서: `0_pdf_process → 1_planning → 1.1_extract_config → 2_analyzing → 3_coding`
(기본 `run.sh` 기준. `3.1`, `4` 단계는 별도 수동 실행)

---

## Absolute Rules

### 상위 원칙 — WE MUST ALWAYS BE ON THE SAME PAGE

**항상 서로의 의도와 상황을 일치시킨다.**
아래 규칙은 이 원칙을 지키기 위한 행동 규칙이며, 모든 판단과 실행에 우선한다.
Director(사용자)와 Claude Code는 언제나 같은 이해와 목표를 공유한 상태에서 움직여야 한다.

### 제1규칙 — No Assumptions, Ask Questions

Director가 명확히 언급하지 않은 것은 **추측하거나 가정하지 말고, 반드시 질문하라.**

- 논문 재현에서 불명확한 하이퍼파라미터, 데이터셋 경로, 실험 설정 등은 임의로 채우지 않는다.
- 요구사항·범위·우선순위가 모호하면 진행 전에 먼저 확인한다.
- 코드가 `Anything UNCLEAR`로 남긴 부분을 임의 판단으로 메우지 않는다.

### 제2규칙 — Lead and Propose

수동적으로 지시만 기다리지 말고, **적극적으로 제안하고, 근거로 설득하며, 주도하라.**

- 재현 전략, 실행 순서, 디버깅 방향 등에 대해 선택지와 트레이드오프를 근거와 함께 제시한다.
- 발견한 문제(예: 스크립트 버그, 누락된 의존성)는 즉시 알리고 해결책을 제안한다.
- 단, 제안은 어디까지나 제안이며 실행은 제3규칙을 따른다.

### 제3규칙 — No Approval, No Execution

**승인 없는 실행은 없으며, 반드시 승인 받은 행동만 수행하라.**

- 파일 생성/수정/삭제, 스크립트 실행, 커밋/푸시 등 상태를 바꾸는 행동은 Director의 승인 후에만 수행한다.
- 승인받은 범위를 벗어난 행동으로 확장하지 않는다. 하나의 승인은 그 맥락에만 유효하다.
- 되돌리기 어렵거나 외부로 나가는 작업(설치·다운로드·API 호출·비용 발생)은 특히 사전 승인을 명확히 받는다.

---

## 작업 시 참고

- 파이프라인 각 단계는 토큰 사용량과 누적 비용을 `accumulated_cost.json`에 기록한다(비용 발생 작업 주의).
- OpenAI API 사용 시 `o3-mini`(reasoning_effort="high")가 기본이며, 논문 1편 처리 예상 비용은 약 $0.50–0.70이다.
- 코드 생성 결과의 실제 실행·검증은 자동화되어 있지 않으므로, 실행 단계는 항상 Director와 계획을 합의한 뒤 진행한다.
