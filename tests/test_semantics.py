import pytest

from msp.protocol import build_receiver_prompt, build_sender_prompt, get_condition
from msp.semantics import canonicalize, extract_json_object, semantic_equal


def test_relation_groups_are_order_insensitive():
    left = {
        "act": "command",
        "facts": [["before", "a", "b"], ["state", "x", "ready"]],
        "constraints": [],
        "post": [],
        "epistemics": [],
    }
    right = {
        "act": "command",
        "facts": [["state", "x", "ready"], ["before", "a", "b"]],
        "constraints": [],
        "post": [],
        "epistemics": [],
    }
    assert semantic_equal(left, right)


def test_relation_arguments_remain_ordered():
    a = {"facts": [["before", "a", "b"]]}
    b = {"facts": [["before", "b", "a"]]}
    assert not semantic_equal(a, b)


def test_extract_json_tolerates_code_fence():
    value = extract_json_object('```json\n{"a":1}\n```')
    assert value == {"a": 1}


def test_unknown_condition_fails_fast():
    with pytest.raises(ValueError):
        get_condition("binary-telepathy")


def test_prompts_keep_source_and_wire_separate():
    sender = build_sender_prompt("msp", "alpha before beta")
    receiver = build_receiver_prompt("msp", '3|20("alpha","beta")')
    assert "alpha before beta" in sender
    assert '3|20("alpha","beta")' in receiver
    assert canonicalize({"b": 2, "a": 1}) == {"a": 1, "b": 2}
