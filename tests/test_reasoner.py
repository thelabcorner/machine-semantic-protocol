import pytest

from msp.reasoner import ParseError, parse_program, reason
from msp.reasoning import build_reasoning_sender_prompt


def test_forward_chain_two_hops():
    program = """
    +red(key)
    r1:red(?x)=>hot(?x)
    r2:hot(?x)=>unsafe(?x)
    """
    result = reason(program, "unsafe(key)")
    assert result.status == "TRUE"
    assert result.proof["rule"] == "r2"


def test_explicit_negation_makes_query_false():
    program = """
    +metal(rod)
    r1:metal(?x)=>conductive(?x)
    r2:conductive(?x)=>!insulating(?x)
    """
    assert reason(program, "insulating(rod)").status == "FALSE"


def test_missing_fact_is_unknown_not_false():
    program = """
    +bird(robin)
    r1:bird(?x)=>flies(?x)
    """
    assert reason(program, "blue(robin)").status == "UNKNOWN"


def test_conjunctive_join_and_binary_relation():
    program = """
    +follows(ada,bo)
    +follows(bo,cy)
    r1:follows(?x,?y)&follows(?y,?z)=>reachable(?x,?z)
    """
    assert reason(program, "reachable(ada,cy)").status == "TRUE"


def test_no_contraposition():
    program = """
    +!signed(package_p)
    r1:safe(?x)=>signed(?x)
    """
    assert reason(program, "!safe(package_p)").status == "UNKNOWN"


def test_contradiction_is_reported_as_both():
    program = """
    +ready(x)
    +!ready(x)
    """
    assert reason(program, "ready(x)").status == "BOTH"


def test_head_variables_must_be_bound():
    with pytest.raises(ParseError):
        parse_program("+seed(a)\nr1:seed(?x)=>linked(?x,?y)")


def test_sender_never_receives_query():
    prompt = build_reasoning_sender_prompt(
        "msp",
        "Every red thing is hot. The key is red.",
    )
    assert "eventual query" in prompt
    assert "Is the key hot?" not in prompt
