# Explore high dimensional data

[![Open in marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/marimo-team/examples/blob/main/explore_high_dimensional_data/explore_high_dimensional_data.py)

**This template lets you visualize and interactively explore high dimensional
data.** The starter code uses PCA to embed and plot numerical digits, seeing
how they cluster together — when you select points in the plot, the notebook
shows you the underlying images!

To use this notebook on your own data, just replace the implementations
of the following four functions:

* `load_data`
* `embed_data`
* `scatter_data`
* `show_selection`

<img src="https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/embedding.gif" width="700px" />

## Running this notebook

Open this notebook in [our online
playground](https://marimo.app/github.com/marimo-team/examples/blob/main/explore_high_dimensional_data/explore_high_dimensional_data.py)
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
