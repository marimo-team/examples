"""Smoke tests that check notebooks don't have syntax errors."""


def test_nlp_span_comparison() -> None:
    from nlp_span_comparison import nlp_span_comparison

    assert not nlp_span_comparison.app._unparsable
