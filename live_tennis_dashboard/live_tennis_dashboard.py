# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "requests==2.32.4",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Live tennis dashboard

        A reactive scoreboard on the [Live Tennis API](https://livetennisapi.com):
        live matches with set score, in-game points, who is serving and a derived
        **break-point marker**, plus upcoming fixtures — across ATP, WTA,
        Challenger, ITF and juniors.

        **No key needed to look around** — without a key the notebook renders
        bundled, clearly-labeled sample data. Add a
        [free API key](https://livetennisapi.com/subscribe/free) to see the real
        live picture.
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import json
    import os
    from pathlib import Path

    import requests

    API_BASE = "https://api.livetennisapi.com/api/public/v1"
    return API_BASE, Path, json, os, requests


@app.cell
def _(mo):
    api_key_box = mo.ui.text(
        kind="password",
        label="API key (optional)",
        placeholder="paste a key here, or set LIVETENNIS_API_KEY in your environment",
        full_width=True,
    )
    api_key_box
    return (api_key_box,)


@app.cell
def _(api_key_box, os):
    api_key = api_key_box.value.strip() or os.environ.get(
        "LIVETENNIS_API_KEY", ""
    ).strip()
    return (api_key,)


@app.cell
def _(mo):
    tour_select = mo.ui.dropdown(
        options={
            "All tours": None,
            "ATP": "atp",
            "WTA": "wta",
            "Challenger": "challenger",
            "ITF": "itf",
            "Juniors": "juniors",
        },
        value="All tours",
        label="Tour",
    )
    player_search = mo.ui.text(
        label="Player search", placeholder="filter by player name"
    )
    refresher = mo.ui.refresh(
        label="Refresh", options=["1m", "5m", "10m"], default_interval=None
    )
    mo.vstack(
        [
            mo.hstack([tour_select, player_search, refresher], justify="start"),
            mo.md(
                "_Budget note: one refresh = 2 API requests (live matches +"
                " fixtures). The free tier allows 30 requests/minute and"
                " 100/day, so auto-refresh intervals here are deliberately"
                " capped at 1 minute or slower — leave it on manual unless you"
                " are watching a match._"
            ),
        ]
    )
    return player_search, refresher, tour_select


@app.cell
def _(Path, json, mo):
    def _load_sample():
        """Load bundled sample_data.json; fall back to a tiny inline sample."""
        candidates = []
        try:
            nb_dir = mo.notebook_dir()
            if nb_dir is not None:
                candidates.append(Path(nb_dir) / "sample_data.json")
        except Exception:
            pass
        candidates.append(Path("sample_data.json"))
        for candidate in candidates:
            try:
                if candidate.is_file():
                    return json.loads(candidate.read_text())
            except Exception:
                continue
        return _INLINE_SAMPLE

    # Minimal inline fallback so the notebook still renders when
    # sample_data.json is not next to it (e.g. in the online playground).
    _INLINE_SAMPLE = {
        "matches": {
            "data": [
                {
                    "id": 910001,
                    "tournament": "Sample Open",
                    "tour": "atp",
                    "surface": "hard",
                    "round": "Quarterfinal",
                    "round_code": "QF",
                    "status": "live",
                    "is_doubles": False,
                    "players": {
                        "p1": {
                            "id": 81001,
                            "name": "Daniel Okafor",
                            "country": "NG",
                            "ranking": 14,
                        },
                        "p2": {
                            "id": 81002,
                            "name": "Tomas Vanek",
                            "country": "CZ",
                            "ranking": 31,
                        },
                    },
                    "score": {
                        "sets": [1, 0],
                        "games": [[6, 4], [3, 2]],
                        "points": ["30", "40"],
                        "server": 1,
                        "is_tiebreak": False,
                    },
                },
                {
                    "id": 910002,
                    "tournament": "Riverside Classic",
                    "tour": "wta",
                    "surface": "clay",
                    "round": "Semifinal",
                    "round_code": "SF",
                    "status": "live",
                    "is_doubles": False,
                    "players": {
                        "p1": {
                            "id": 82001,
                            "name": "Sofia Marchetti",
                            "country": "IT",
                            "ranking": 8,
                        },
                        "p2": {
                            "id": 82002,
                            "name": "Hana Kobayashi",
                            "country": "JP",
                            "ranking": 22,
                        },
                    },
                    "score": {
                        "sets": [0, 1],
                        "games": [[4, 6], [6, 6]],
                        "points": ["5", "3"],
                        "server": 2,
                        "is_tiebreak": True,
                    },
                },
            ]
        },
        "fixtures": {
            "data": [
                {
                    "id": 920001,
                    "event_date": "2026-08-16",
                    "start_time": "2026-08-16T15:00:00Z",
                    "tour": "atp",
                    "tournament": "Sample Open",
                    "round": "Quarterfinal",
                    "surface": "hard",
                    "player1_name": "Andrei Popescu",
                    "player2_name": "Louis Moreau",
                    "status": "scheduled",
                },
                {
                    "id": 920002,
                    "event_date": "2026-08-16",
                    "start_time": "2026-08-16T17:30:00Z",
                    "tour": "wta",
                    "tournament": "Riverside Classic",
                    "round": "Semifinal",
                    "surface": "clay",
                    "player1_name": "Emma Lindqvist",
                    "player2_name": "Carla Duarte",
                    "status": "scheduled",
                },
            ]
        },
    }

    SAMPLE = _load_sample()
    return (SAMPLE,)


@app.cell
def _(API_BASE, SAMPLE, api_key, mo, refresher, requests, tour_select):
    refresher  # referencing the refresh element re-runs this cell on refresh

    def _get(path, params):
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            headers={"X-API-Key": api_key},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    _tour_params = {"tour": tour_select.value} if tour_select.value else {}

    if api_key:
        try:
            live_matches = _get("/matches", {"status": "live", **_tour_params})[
                "data"
            ]
            fixtures = _get("/fixtures", {"limit": 25, **_tour_params})["data"]
            is_sample = False
            data_banner = mo.callout(
                mo.md(
                    "**Live data** from api.livetennisapi.com — press Refresh"
                    " for the latest scores."
                ),
                kind="success",
            )
        except Exception as request_error:
            live_matches = SAMPLE["matches"]["data"]
            fixtures = SAMPLE["fixtures"]["data"]
            is_sample = True
            data_banner = mo.callout(
                mo.md(
                    f"API request failed (`{request_error}`) — showing"
                    " **sample data** instead."
                ),
                kind="warn",
            )
    else:
        live_matches = SAMPLE["matches"]["data"]
        fixtures = SAMPLE["fixtures"]["data"]
        is_sample = True
        data_banner = mo.callout(
            mo.md(
                "**Sample data** (fictional players, frozen scores) — no API"
                " key set. Paste a key above or set `LIVETENNIS_API_KEY` to"
                " see real live matches."
            ),
            kind="info",
        )
    data_banner
    return fixtures, is_sample, live_matches


@app.cell
def _():
    def fmt_sets(score):
        sets = (score or {}).get("sets") or []
        return f"{sets[0]}-{sets[1]}" if len(sets) == 2 else ""

    def fmt_games(score):
        games = (score or {}).get("games") or []
        if len(games) == 2 and games[0]:
            return " ".join(f"{a}-{b}" for a, b in zip(games[0], games[1]))
        return ""

    def fmt_points(score):
        points = (score or {}).get("points") or []
        if len(points) == 2 and points[0] is not None and points[1] is not None:
            text = f"{points[0]}-{points[1]}"
            return f"TB {text}" if (score or {}).get("is_tiebreak") else text
        return ""

    def server_label(score):
        return {1: "P1", 2: "P2"}.get((score or {}).get("server"), "")

    def break_point(score):
        """Derived marker: the receiver is one point from breaking serve.

        Not a field the API sends — computed from `points` + `server`:
        receiver at AD, or receiver at 40 while the server is below 40.
        Tiebreaks are excluded (no break points in a tiebreak game).
        """
        if not score or score.get("is_tiebreak"):
            return False
        server = score.get("server")
        points = score.get("points") or []
        if server not in (1, 2) or len(points) != 2 or None in points:
            return False
        receiver_points = points[2 - server]
        server_points = points[server - 1]
        return receiver_points == "AD" or (
            receiver_points == "40" and server_points in ("0", "15", "30")
        )

    def player_label(player):
        if not player:
            return ""
        label = player.get("name") or ""
        if player.get("country"):
            label += f" ({player['country']})"
        if player.get("ranking"):
            label += f" · #{player['ranking']}"
        return label

    return break_point, fmt_games, fmt_points, fmt_sets, player_label, server_label


@app.cell
def _(
    break_point,
    fmt_games,
    fmt_points,
    fmt_sets,
    live_matches,
    mo,
    player_search,
    player_label,
    server_label,
    tour_select,
):
    _query = player_search.value.strip().lower()

    def _keep(match):
        if tour_select.value and match.get("tour") != tour_select.value:
            return False
        if _query:
            players = match.get("players") or {}
            names = " ".join(
                (players.get(side) or {}).get("name") or ""
                for side in ("p1", "p2")
            ).lower()
            return _query in names
        return True

    _rows = []
    for _match in live_matches:
        if not _keep(_match):
            continue
        _score = _match.get("score")
        _players = _match.get("players") or {}
        _serving = server_label(_score)
        _bp = break_point(_score)
        _rows.append(
            {
                "Tour": (_match.get("tour") or "").upper(),
                "Tournament": _match.get("tournament") or "",
                "Round": _match.get("round") or "",
                "Player 1": player_label(_players.get("p1"))
                + (" ●" if _serving == "P1" else ""),
                "Player 2": player_label(_players.get("p2"))
                + (" ●" if _serving == "P2" else ""),
                "Sets": fmt_sets(_score),
                "Games": fmt_games(_score),
                "Points": fmt_points(_score),
                "Break point": (
                    "P2" if _serving == "P1" else "P1"
                ) if _bp else "",
            }
        )

    _live_view = (
        mo.ui.table(_rows, selection=None, pagination=False)
        if _rows
        else mo.md("_No live matches match the current filters._")
    )
    mo.vstack(
        [
            mo.md(
                f"## Live matches ({len(_rows)})\n"
                "● = serving · **Break point** names the player one point from"
                " breaking (derived from the score, tiebreaks excluded)."
            ),
            _live_view,
        ]
    )
    return


@app.cell
def _(fixtures, is_sample, mo, player_search, tour_select):
    _query = player_search.value.strip().lower()

    def _keep(fixture):
        # In live mode the API already applied the grouped ?tour= filter.
        # Sample mode approximates it: Fixture.tour is the record's own
        # granular value (e.g. "challenger_men"), so match by prefix.
        if tour_select.value and is_sample:
            if not (fixture.get("tour") or "").lower().startswith(
                tour_select.value
            ):
                return False
        if _query:
            names = (
                f"{fixture.get('player1_name') or ''}"
                f" {fixture.get('player2_name') or ''}"
            ).lower()
            return _query in names
        return True

    _rows = [
        {
            "Starts (UTC)": fixture.get("start_time")
            or fixture.get("event_date")
            or "TBD",
            "Tour": fixture.get("tour") or "",
            "Tournament": fixture.get("tournament") or "",
            "Round": fixture.get("round") or "",
            "Player 1": fixture.get("player1_name") or "",
            "Player 2": fixture.get("player2_name") or "",
        }
        for fixture in fixtures
        if _keep(fixture)
    ]

    _fixtures_view = (
        mo.ui.table(_rows, selection=None, pagination=False)
        if _rows
        else mo.md("_No upcoming fixtures match the current filters._")
    )
    mo.vstack([mo.md(f"## Upcoming fixtures ({len(_rows)})"), _fixtures_view])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        **Adapting this notebook.** Everything above runs on two FREE
        endpoints — `GET /matches?status=live` and `GET /fixtures` — of the
        [Live Tennis API](https://docs.livetennisapi.com) (free tier: 30
        requests/minute, 100/day; historical results and market prices are
        paid tiers). Ideas: point the fetch cell at
        `/matches?status=upcoming`, add a `country` filter, or join
        `/players?search=` for player bios. Full spec:
        [openapi.yaml](https://docs.livetennisapi.com/openapi.yaml).
        """
    )
    return


if __name__ == "__main__":
    app.run()
