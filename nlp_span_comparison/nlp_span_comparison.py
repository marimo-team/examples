# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.10.13"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# Span Comparison""")
    return


@app.cell
def _(textwrap, urllib):
    # Modify this function to load your own examples
    def load_examples():
        hamlet_url = "https://gist.githubusercontent.com/provpup/2fc41686eab7400b796b/raw/b575bd01a58494dfddc1d6429ef0167e709abf9b/hamlet.txt"

        with urllib.request.urlopen(hamlet_url) as f:
            HAMLET = f.read().decode("utf-8")

        return [
            textwrap.dedent(block).strip()[:1000]
            for block in HAMLET.split("\n\n")
            if block
        ]

    return (load_examples,)


@app.cell
def _(random):
    # Replace with your predictor for model A
    def model_a_predictor(text: str) -> tuple[int, int]:
        random.seed(len(text))
        start = random.randint(0, len(text) - 2)
        end = random.randint(start + 1, len(text) - 1)
        return start, end

    return (model_a_predictor,)


@app.cell
def _(random):
    # Replace with your predictor for model B
    def model_b_predictor(text: str) -> tuple[int, int]:
        random.seed(len(text) / 2)
        start = random.randint(0, len(text) - 2)
        end = random.randint(start + 1, len(text) - 1)
        return start, end

    return (model_b_predictor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        !!! tip "This notebook is best viewed as an app."
            Hit `Cmd/Ctrl+.` or click the "app view" button in the bottom right.
        """
    )
    return


@app.cell
def _(load_examples):
    EXAMPLES = load_examples()
    return (EXAMPLES,)


@app.cell
def _(NUMBER_OF_EXAMPLES, mo):
    index = mo.ui.number(
        0,
        NUMBER_OF_EXAMPLES - 1,
        value=0,
        step=1,
        debounce=True,
        label="example number",
    )
    return (index,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""_Models A and B both predict spans. Which do you prefer?_""")
    return


@app.cell
def _(NUMBER_OF_EXAMPLES, mo, num_a_preferred, num_b_preferred):
    mo.ui.table(
        [
            {"Model": "A", "Score": f"{num_a_preferred}/{NUMBER_OF_EXAMPLES}"},
            {"Model": "B", "Score": f"{num_b_preferred}/{NUMBER_OF_EXAMPLES}"},
        ],
        selection=None,
    )
    return


@app.cell
def _(get_choices, mo):
    mo.accordion({"All preferences": mo.ui.table(get_choices(), selection=None)})
    return


@app.cell
def _(index):
    index.center()
    return


@app.cell
def _(CHOICES_PATH, get_choices, index, mo, write_choices):
    def _():
        preference = get_choices()[index.value]["model"]
        mo.stop(preference is None, mo.md("**Choose the better model**.").center())

        write_choices(get_choices(), CHOICES_PATH)
        return mo.md(f"You prefer **model {preference}**.").center()

    _()
    return


@app.cell
def _(annotate, mo):
    mo.hstack(
        [
            annotate("Model A", [0, len("Model A")], "yellow"),
            annotate("Model B", [0, len("Model B")], "lightblue"),
        ],
        justify="space-around",
    )
    return


@app.cell
def _(CHOICES_PATH, EXAMPLES, load_choices, mo):
    get_choices, set_choices = mo.state(load_choices(CHOICES_PATH, len(EXAMPLES)))
    return get_choices, set_choices


@app.cell
def _(index, mo, set_choices):
    model_A = mo.ui.button(
        label="Model A",
        on_change=lambda _: set_choices(
            lambda v: v[: index.value]
            + [{"index": index.value, "model": "A"}]
            + v[index.value + 1 :]
        ),
    )

    model_B = mo.ui.button(
        label="Model B",
        on_change=lambda _: set_choices(
            lambda v: v[: index.value]
            + [{"index": index.value, "model": "B"}]
            + v[index.value + 1 :]
        ),
    )
    mo.hstack([model_A, model_B], justify="space-around")
    return model_A, model_B


@app.cell
def _(EXAMPLES, annotate, index, model_a_predictor, model_b_predictor):
    _example = EXAMPLES[index.value]

    model_A_prediction = annotate(_example, model_a_predictor(_example), color="yellow")

    model_B_prediction = annotate(
        _example, model_b_predictor(_example), color="lightblue"
    )
    return model_A_prediction, model_B_prediction


@app.cell
def _(mo, model_A_prediction, model_B_prediction):
    mo.hstack([model_A_prediction, model_B_prediction], gap=2, justify="space-around")
    return


@app.cell
def _(get_choices):
    num_a_preferred = sum(1 for c in get_choices() if c["model"] == "A")
    num_b_preferred = sum(1 for c in get_choices() if c["model"] == "B")
    return num_a_preferred, num_b_preferred


@app.cell
def _(mo):
    CHOICES_PATH = str(mo.notebook_dir() / "choices.json")
    return (CHOICES_PATH,)


@app.cell
def _(json, os):
    # This template gets and saves labels to a local JSON file, but you
    # can readily change this to point to a database or anything else.
    def load_choices(path, number_of_examples):
        if not os.path.exists(path):
            return [{"index": i, "model": None} for i in range(number_of_examples)]

        with open(path, "r") as f:
            choices = json.loads(f.read())
        assert len(choices) == number_of_examples
        return choices

    def write_choices(choices, path):
        # Trunacate notes
        with open(path, "w") as f:
            f.write(json.dumps(choices))

    return load_choices, write_choices


@app.cell
def _(mo):
    def annotate(text, span, color):
        mark_start = f"<mark style='background-color:{color}'>"
        return mo.md(
            text[: span[0]]
            + mark_start
            + text[span[0] : span[1]]
            + "</mark>"
            + text[span[1] :]
        )

    return (annotate,)


@app.cell
def _(EXAMPLES):
    NUMBER_OF_EXAMPLES = len(EXAMPLES)
    return (NUMBER_OF_EXAMPLES,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import json
    import os
    import random
    import textwrap
    import urllib

    return json, os, random, textwrap, urllib


if __name__ == "__main__":
    app.run()
