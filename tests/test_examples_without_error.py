"""Smoke tests that check notebooks don't have syntax errors."""


def test_nlp_span_comparison() -> None:
    from nlp_span_comparison import nlp_span_comparison

    assert not nlp_span_comparison.app._unparsable


def test_explore_high_dimensional_data() -> None:
    from explore_high_dimensional_data import explore_high_dimensional_data

    assert not explore_high_dimensional_data.app._unparsable
