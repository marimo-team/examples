# NLP Span Comparison

[![Open in marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/marimo-team/examples/blob/main/nlp_span_comparison/nlp_span_comparison.py)

This notebook can be used as a template for comparing NLP models that predict
spans. Given two models and a sequence of text examples from which to extract
spans, the notebook presents the model predictions on each example and
lets you indicate which model yielded the better prediction.

## Running this notebook

Open this notebook in [our online
playground](https://marimo.app/github.com/marimo-team/examples/blob/main/examples/nlp_span_comparison/nlp_span_comparison.py)
or run it locally.

### Running locally

The requirements of each notebook are serialized in them as a top-level
comment. Here are the steps to run the notebook:

1. [Install `uv`](https://github.com/astral-sh/uv/?tab=readme-ov-file#installation)
2. Open an example with `uvx marimo edit --sandbox <notebook-url>`

> [!TIP]
> The [`--sandbox`
> flag](https://docs.marimo.io/guides/package_reproducibility/) opens the
> notebook in an isolated virtual environment, automatically installing the
> notebook's dependencies 📦

You can also open notebooks without `uv`, in which case you'll need to
manually [install marimo](https://docs.marimo.io/getting_started/index.html#installation)
first. Then run `marimo edit <notebook-url>`; however, you'll also need to
install the requirements yourself.
