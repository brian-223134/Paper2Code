# 01. 프로젝트 개요

## 무엇을 하는가

**Paper2Code**는 과학 논문(주로 머신러닝 분야)을 입력으로 받아, 논문에서 설명한 방법론과 실험을
재현할 수 있는 **코드 저장소(repository)를 자동으로 생성**하는 연구 프로젝트입니다.

논문에서 제안한 실제 시스템의 이름은 **PaperCoder**로, 여러 개의 역할이 다른 LLM 에이전트가
협력하는 **멀티 에이전트(multi-agent) 시스템**입니다.

- 저자: Minju Seo, Jinheon Baek, Seongyun Lee, Sung Ju Hwang (KAIST 등)
- 발표: ICLR 2026
- 논문: <https://arxiv.org/abs/2504.17192>

## 왜 필요한가

많은 논문이 **공식 코드를 공개하지 않아** 재현(reproduction)이 어렵습니다.
PaperCoder는 사람이 논문을 읽고 직접 구현하는 과정을 LLM으로 자동화하여,
공식 코드가 없는 논문도 재현 가능한 구현체를 만들어 냅니다.

## 핵심 아이디어: 3단계 파이프라인

사람이 논문을 코드로 옮길 때 거치는 사고 과정을 세 단계로 나누어 각기 다른 에이전트에게 맡깁니다.

```
논문(PDF/LaTeX)
   │
   ▼
① Planning (계획)   ── 전체 로드맵 + 아키텍처 설계 + 파일별 작업 목록 + config.yaml
   │
   ▼
② Analysis (분석)   ── 각 파일을 어떻게 구현할지 상세 로직 분석
   │
   ▼
③ Coding (코드 생성) ── 의존성 순서에 따라 파일별로 실제 코드 작성
   │
   ▼
재현 코드 저장소 (예: Transformer_repo/)
```

각 단계는 이전 단계의 산출물을 입력으로 이어받으며(대화 trajectory 누적),
최종적으로 실행 가능한 파이썬 프로젝트를 생성합니다.

## 지원하는 실행 방식

- **OpenAI API 사용** — 기본 모델 `o3-mini` (`reasoning_effort="high"`)
- **오픈소스 모델 사용** — vLLM 기반, 기본 모델 `deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct`

입력 논문은 두 가지 형식을 지원합니다.

- **JSON** — PDF를 [s2orc-doc2json](https://github.com/allenai/s2orc-doc2json)으로 변환한 구조화된 형식 (논문 실험에서 사용한 기본 방식)
- **LaTeX** — 논문의 LaTeX 소스를 직접 사용

## 성과

- Paper2Code 벤치마크 및 PaperBench에서 강력한 베이스라인 대비 우수한 성능
- 모델 기반 평가(o3-mini-high, 8회 샘플 평균 1~5점)에서 높은 충실도(faithfulness)의 구현 생성
