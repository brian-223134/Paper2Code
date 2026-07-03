"""utils.extract_code_from_content / extract_code_from_content2 / extract_json_from_string 테스트.

coding 단계(3_coding.py)가 LLM 응답에서 코드 펜스를 뽑아내는 데 사용한다.
"""
import utils


def test_extract_code_from_content_basic():
    content = "```python\nprint(1)\n```"
    assert utils.extract_code_from_content(content) == "print(1)\n"


def test_extract_code_from_content_no_language_tag():
    content = "```\nx = 1\n```"
    assert utils.extract_code_from_content(content) == "x = 1\n"


def test_extract_code_from_content_returns_empty_when_no_fence():
    assert utils.extract_code_from_content("no code here") == ""


def test_extract_code_from_content2_basic():
    content = "설명\n```python\nprint(2)\n```\n끝"
    assert utils.extract_code_from_content2(content) == "print(2)"


def test_extract_code_from_content2_returns_empty_when_no_python_fence():
    assert utils.extract_code_from_content2("plain text") == ""


def test_extract_json_from_string_basic():
    text = "before\n```json\n{\"a\": 1}\n```\nafter"
    assert utils.extract_json_from_string(text) == '{"a": 1}'


def test_extract_json_from_string_returns_empty_when_missing():
    assert utils.extract_json_from_string("no json fence") == ""
