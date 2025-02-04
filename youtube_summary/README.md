# Youtube Summary

This notebook can be used as a template to summarise YouTube videos. It was originally
used to fetch summaries for some [keyboard reviews](https://www.youtube.com/playlist?list=PLGj5nRqy15j93TD0iReqfLL9lU1lZFEs6) but the notebook itself can be adapted
for many other use-cases too. 

![](/assets/youtube_summary.png)

## Running this notebook

The only want to run this notebook is to run it locally. This demo uses Claude as
an LLM backend which requires a `ANTHROPIC_API_KEY` set in a `.env` file. Finally, 
this notebook also assumes that `ffmpeg` is available on your system ([details](https://github.com/openai/whisper/blob/main/README.md#setup)). 

Once that's taken care of you can run this notebook in a sandbox. The requirements of each notebook are serialized in them as a top-level
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
