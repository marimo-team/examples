# Live tennis dashboard

[![Open in marimo](https://marimo.io/shield.svg)](https://marimo.app/github.com/marimo-team/examples/blob/main/live_tennis_dashboard/live_tennis_dashboard.py)

**A reactive scoreboard for live tennis.** This notebook pulls live matches
and upcoming fixtures from the [Live Tennis
API](https://livetennisapi.com) — ATP, WTA, Challenger, ITF and juniors — and
renders them as filterable tables with set score, in-game points, a serving
marker and a **break-point marker derived from the raw score**. A tour
dropdown and a player-search box filter everything reactively.

**No API key is needed to try it**: without a key the notebook renders
bundled, clearly-labeled sample data (`sample_data.json`, fictional players),
so it works out of the box — including in the online playground, via a small
inline fallback.

<img src="https://raw.githubusercontent.com/livetennisapi/livetennis-marimo/main/assets/preview.png" width="700px" />

## Running this notebook

Open this notebook in [our online
playground](https://marimo.app/github.com/marimo-team/examples/blob/main/live_tennis_dashboard/live_tennis_dashboard.py)
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

## Using your own API key (live data)

1. Get a key — the [free tier](https://livetennisapi.com/subscribe/free) is
   self-serve (no card): 30 requests/minute, 100/day. Historical results and
   market prices are paid tiers; this notebook only uses FREE endpoints
   (`GET /matches?status=live`, `GET /fixtures`).
2. Set `LIVETENNIS_API_KEY` in your environment before starting marimo, or
   paste the key into the field at the top of the notebook.

The notebook is deliberately polite to that budget: refresh is manual by
default, the optional auto-refresh intervals are capped at 1 minute or
slower, and one refresh costs 2 requests.

## Adapting this notebook

- **Other match states**: point the fetch cell at `/matches?status=upcoming`
  (also FREE).
- **More filters**: `/matches` accepts `player`, `country` and `from`/`to`
  query parameters.
- **Player bios**: join `/players?search=` (FREE) on the names in the tables.
- **Break-point logic**: the marker is computed client-side in the
  `break_point` function (receiver at AD, or at 40 while the server is below
  40; tiebreaks excluded) — extend it for set/match points.
- Full API reference:
  [docs.livetennisapi.com](https://docs.livetennisapi.com)
  ([openapi.yaml](https://docs.livetennisapi.com/openapi.yaml)).
