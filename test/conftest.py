"""pytest 공통 설정.

codes/ 디렉토리를 sys.path에 추가해 `import utils`가 가능하도록 한다.
(codes/의 형제 스크립트들은 `1.1_...py`처럼 숫자로 시작해 직접 import가 불가하지만,
 utils.py는 정상 모듈명이라 import 가능하다.)
"""
import os
import sys

CODES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "codes"))
if CODES_DIR not in sys.path:
    sys.path.insert(0, CODES_DIR)

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
