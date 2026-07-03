"""utils.content_to_json / content_to_json4 테스트.

이 함수들은 LLM이 뱉은 `[CONTENT]...[/CONTENT]` 블록(주석·trailing comma 포함)을
관용적으로 JSON으로 파싱한다. 파이프라인 전 단계(planning/analyzing/coding)가 의존한다.
"""
import utils


def test_plain_dict_inside_content_tags():
    data = '[CONTENT]{"a": "b", "n": 1}[/CONTENT]'
    assert utils.content_to_json(data) == {"a": "b", "n": 1}


def test_inline_hash_comment_is_stripped():
    # "x", # note  ->  "x",
    data = '[CONTENT]["x", # this is a note\n"y"][/CONTENT]'
    assert utils.content_to_json(data) == ["x", "y"]


def test_trailing_comma_before_bracket_is_tolerated():
    data = '[CONTENT]["a", "b",][/CONTENT]'
    assert utils.content_to_json(data) == ["a", "b"]


def test_without_content_tags_still_parses():
    data = '{"k": [1, 2, 3]}'
    assert utils.content_to_json(data) == {"k": [1, 2, 3]}


def test_content_to_json4_extracts_logic_and_task_list():
    # 앞의 파서들이 실패했을 때 정규식으로 두 키만 구제하는 마지막 단계.
    data = (
        'garbage prefix "Logic Analysis": [["a.py", "does x"], ["b.py", "does y"]] '
        ', "Task list": ["a.py", "b.py"] garbage suffix'
    )
    result = utils.content_to_json4(data)
    assert result == {
        "Logic Analysis": [["a.py", "does x"], ["b.py", "does y"]],
        "Task list": ["a.py", "b.py"],
    }


def test_content_to_json4_returns_empty_when_no_match():
    assert utils.content_to_json4("nothing useful here") == {}
