# Paper2Code / PaperCoder 문서

이 디렉토리는 **Paper2Code** 프로젝트(논문 → 코드 저장소 자동 생성)의 구조와 동작 방식을 정리한 문서입니다.

## 문서 목록

| 문서 | 내용 |
|------|------|
| [01-overview.md](01-overview.md) | 프로젝트 개요, 목적, 핵심 아이디어 |
| [02-architecture.md](02-architecture.md) | 3단계 멀티 에이전트 파이프라인 상세 |
| [03-directory.md](03-directory.md) | 디렉토리·파일 구조 설명 |
| [04-usage.md](04-usage.md) | 설치 및 실행 방법 |
| [05-evaluation.md](05-evaluation.md) | 생성 저장소 평가(모델 기반) 방법 |

## 한 줄 요약

**PaperCoder**는 머신러닝 논문을 입력받아 **계획(Planning) → 분석(Analysis) → 코드 생성(Code Generation)**의
3단계로 처리하여, 논문의 방법론을 재현하는 실행 가능한 코드 저장소를 자동으로 만들어내는 멀티 에이전트 LLM 시스템입니다.

- 논문: [Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning (ICLR 2026)](https://arxiv.org/abs/2504.17192)
- 원본 저장소: <https://github.com/going-doer/Paper2Code>
- 벤치마크 데이터셋: [huggingface.co/datasets/iaminju/paper2code](https://huggingface.co/datasets/iaminju/paper2code)
