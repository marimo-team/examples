# /// script
# requires-python = ">=3.12"
# dependencies = ["marimo==0.24.0"]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="Can these two prices be compared?")

with app.setup:
    import html
    import math

    import marimo as mo


@app.function
def synthetic_records(scenario: str, source_age: int = 1) -> tuple[dict, list[dict]]:
    """Create fictional teaching records. Minutes refer to a fictional day."""
    left = {
        "event": "North vs South, game A",
        "market": "spread",
        "outcome": "North",
        "point": -3.5,
        "period": "full game",
        "settlement": "includes overtime",
        "price": -110,
        "source_minute": 719,
        "retrieved_minute": 720,
    }
    right = {**left, "price": -105, "source_minute": 720 - source_age}
    changes = {
        "matching": {},
        "event": {"event": "North vs South, game B"},
        "market": {"market": "moneyline", "point": None},
        "outcome": {"outcome": "South", "point": 3.5},
        "point": {"point": -2.5},
        "period": {"period": "first half"},
        "settlement": {"settlement": "excludes overtime"},
        "unknown_rules": {"settlement": None},
        "unknown_time": {"source_minute": None},
        "future_time": {"source_minute": 721},
        "missing": {},
        "duplicate": {},
    }
    if scenario not in changes:
        raise ValueError("Unknown teaching scenario")
    right.update(changes[scenario])
    if scenario == "missing":
        return left, []
    if scenario == "duplicate":
        return left, [right, {**right, "price": -115}]
    return left, [right]


@app.function
def compare_records(
    left: dict,
    candidates: list[dict],
    max_age: int,
    max_time_gap: int,
    now_minute: int = 720,
) -> list[str]:
    """Explain why comparability is not established under explicit toy rules."""
    if max_age < 0 or max_time_gap < 0:
        raise ValueError("Time tolerances must be nonnegative")
    if not candidates:
        return ["The requested named outcome is missing. There is no price to compare."]
    if len(candidates) != 1:
        return [
            f"There are {len(candidates)} candidate records for B. "
            "The duplicate is unresolved; neither price is selected."
        ]
    right = candidates[0]
    reasons = []
    labels = {
        "event": "Event identity",
        "market": "Market",
        "outcome": "Named outcome",
        "period": "Period",
        "settlement": "Settlement rules",
    }
    for field, label in labels.items():
        if left.get(field) is None or right.get(field) is None:
            reasons.append(f"{label} are not fully supplied.")
        elif left[field] != right[field]:
            reasons.append(f"{label}: the records differ.")
    if left.get("market") in ("spread", "total") or right.get("market") in ("spread", "total"):
        if left.get("point") is None or right.get("point") is None:
            reasons.append("A required point/line is not supplied.")
        elif left["point"] != right["point"]:
            reasons.append("Point/line differs. Different handicaps are different contracts.")
    for label, record in (("A", left), ("B", right)):
        price = record.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or not math.isfinite(price) or abs(price) < 100:
            reasons.append(f"{label} has no valid American price in this example.")
        source = record.get("source_minute")
        fetched = record.get("retrieved_minute")
        if source is None:
            reasons.append(f"{label} has no source timestamp. Retrieval time cannot replace it.")
        elif source > now_minute:
            reasons.append(f"{label} has a future source timestamp.")
        elif now_minute - source > max_age:
            reasons.append(f"{label} is {now_minute - source} minutes old, outside your {max_age}-minute age limit.")
        if fetched is None:
            reasons.append(f"{label} has no retrieval timestamp.")
        elif fetched > now_minute or (source is not None and source > fetched):
            reasons.append(f"{label} has inconsistent source/retrieval timestamps.")
    a_time, b_time = left.get("source_minute"), right.get("source_minute")
    if a_time is not None and b_time is not None and abs(a_time - b_time) > max_time_gap:
        reasons.append(f"Source times are {abs(a_time - b_time)} minutes apart, beyond your {max_time_gap}-minute gap limit.")
    return reasons


@app.function
def workload(interval: int, hours: int, days: int, weight: int) -> dict:
    """Count polls at t=0, interval, ... strictly inside each active window."""
    for value, lower, upper, name in (
        (interval, 1, 1440, "interval"),
        (hours, 1, 24, "hours"),
        (days, 1, 31, "days"),
        (weight, 0, 100, "weight"),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or not lower <= value <= upper:
            raise ValueError(f"Invalid {name}")
    calls_daily = math.ceil(hours * 60 / interval)
    return {
        "calls_daily": calls_daily,
        "calls_monthly": calls_daily * days,
        "credits_monthly": calls_daily * days * weight,
        "unobserved_hours_daily": 24 - hours,
    }


@app.function
def record_table(left: dict, candidates: list[dict]) -> str:
    """Render only the synthetic input records, including unresolved duplicates."""
    records = [left, *candidates]
    names = ["Record A", *[f"Record B{n + 1}" for n in range(len(candidates))]]
    if not candidates:
        records.append({})
        names.append("Record B: missing")
    header = "".join(f"<th scope='col'>{html.escape(n)}</th>" for n in names)
    rows = []
    for key, label in (
        ("price", "American price"), ("event", "Event"), ("market", "Market"),
        ("outcome", "Named outcome"), ("point", "Point / line"),
        ("period", "Period"), ("settlement", "Settlement"),
        ("source_minute", "Source time"), ("retrieved_minute", "Retrieved at"),
    ):
        values = []
        for record in records:
            value = record.get(key)
            if value is None:
                display = "Not supplied"
            elif key.endswith("minute"):
                display = f"{value // 60:02d}:{value % 60:02d}"
            elif key == "price":
                display = f"{value:+d}"
            else:
                display = str(value)
            values.append(f"<td>{html.escape(display)}</td>")
        rows.append(f"<tr><th scope='row'>{label}</th>{''.join(values)}</tr>")
    return f"<div class='lab-scroll'><table class='lab-table'><thead><tr><th>Field</th>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


@app.function
def observation_diagram(interval: int, hours: int) -> str:
    """Draw an explicit schedule, never a claimed reconstruction of price changes."""
    active = hours / 24 * 600
    ticks = "".join(
        f"<line x1='{30 + minute * 10}' y1='127' x2='{30 + minute * 10}' y2='158' stroke='#2563eb' stroke-width='2'/>"
        for minute in range(0, 60, interval)
    )
    return f"""<svg class='lab-timeline' viewBox='0 0 660 195' role='img' aria-label='{hours} active hours and {24-hours} unobserved hours each day; one request every {interval} minutes while active'>
      <text x='30' y='22'>One fictional day: active window starts at 00:00</text>
      <rect x='30' y='38' width='600' height='30' rx='4' fill='#e2e8f0'/>
      <rect x='30' y='38' width='{active}' height='30' rx='4' fill='#2563eb'/>
      <text x='30' y='89'>00:00</text><text x='290' y='89'>12:00</text><text x='590' y='89'>24:00</text>
      <text x='30' y='119'>Zoom: scheduled requests during the first active hour</text>
      <line x1='30' y1='145' x2='630' y2='145' stroke='#cbd5e1'/>{ticks}
      <text x='30' y='183'>0 min</text><text x='292' y='183'>30 min</text><text x='586' y='183'>60 min</text>
    </svg>"""


@app.cell(hide_code=True)
def _():
    mo.Html("""<style>
    .lab-scroll { overflow-x: auto; max-width: 100%; }
    .lab-table { border-collapse: collapse; width: 100%; font-size: 13px; }
    .lab-table th, .lab-table td { padding: 9px 10px; border-bottom: 1px solid #cbd5e1; text-align: left; }
    .lab-table th { font-weight: 650; }
    .lab-table td { min-width: 105px; }
    .lab-table tbody tr:first-child td { font-size: 25px; font-weight: 750; }
    .lab-result { border-left: 5px solid #2563eb; padding: 14px 18px; background: #eff6ff; color: #172554; }
    .lab-result.warn { border-color: #b45309; background: #fffbeb; color: #78350f; }
    .lab-result ul { padding-left: 20px; margin-bottom: 0; }
    .lab-timeline { width: 100%; height: auto; background: #f8fafc; color: #0f172a; border-radius: 8px; }
    .lab-timeline text { fill: #334155; font: 12px system-ui, sans-serif; }
    .lab-kpis { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 10px; }
    .lab-kpis div { padding: 16px; border: 1px solid #cbd5e1; border-radius: 8px; }
    .lab-kpis b { display: block; font-size: clamp(20px,4vw,31px); }
    .lab-kpis span { display: block; font-size: 12px; }
    @media(max-width: 500px) { .lab-kpis { grid-template-columns: 1fr; } .lab-table th,.lab-table td { padding: 7px; } }
    </style>""")
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    # Can these two prices be compared?

    **An interactive data-quality lab. All records are synthetic.**

    A price is a number attached to a contract and a moment in time.
    Change one assumption below and watch an apparently simple comparison break.
    This lesson makes no API calls and needs no account or key.
    """)
    return


@app.cell(hide_code=True)
def _():
    scenario = mo.ui.dropdown(
        options={
            "Same contract": "matching", "Wrong event": "event",
            "Different market": "market", "Other team's outcome": "outcome",
            "Different point / line": "point", "Different period": "period",
            "Different settlement rules": "settlement", "Unknown settlement rules": "unknown_rules",
            "Missing named outcome": "missing", "Duplicate candidate records": "duplicate",
            "Missing source timestamp": "unknown_time",
            "Future source timestamp": "future_time",
        }, value="Different point / line", label="Change record B", full_width=True,
    )
    source_age = mo.ui.slider(0, 20, value=1, label="B source age (minutes)", show_value=True)
    max_age = mo.ui.slider(0, 15, value=5, label="Your maximum age (minutes)", show_value=True)
    max_gap = mo.ui.slider(0, 15, value=2, label="Your maximum time gap (minutes)", show_value=True)
    mo.vstack([scenario, mo.hstack([source_age, max_age, max_gap], wrap=True)])
    return max_age, max_gap, scenario, source_age


@app.cell(hide_code=True)
def _(max_age, max_gap, scenario, source_age):
    left_record, right_candidates = synthetic_records(scenario.value, source_age.value)
    reasons = compare_records(left_record, right_candidates, max_age.value, max_gap.value)
    _verdict = "Cannot establish comparability" if reasons else "Comparable under these teaching assumptions"
    _explanation = "".join(f"<li>{html.escape(reason)}</li>" for reason in reasons)
    if not reasons:
        _explanation = "<li>The declared fields and chosen time limits match. This is not evidence of a good bet, executable liquidity or verified real-world settlement rules.</li>"
    mo.vstack([
        mo.Html(f"<div class='lab-result {'warn' if reasons else ''}' role='status'><strong>{_verdict}</strong><ul>{_explanation}</ul></div>"),
        mo.Html(record_table(left_record, right_candidates)),
        mo.md("All times belong to one fictional day. Comparison time is **12:00**. Both records were retrieved at 12:00; a recent retrieval does not make an older source quote fresh."),
    ])
    return left_record, reasons, right_candidates


@app.cell(hide_code=True)
def _():
    mo.md("""
    ## What does a slower polling schedule give up?

    Move from comparison quality to observation design. Choose one hypothetical
    request scope, then vary when you ask for it. The blue window is the part
    of the day you observe; the short lines are requests, not price changes.
    """)
    return


@app.cell(hide_code=True)
def _():
    interval = mo.ui.dropdown(options={"1 minute": 1, "5 minutes": 5, "15 minutes": 15, "60 minutes": 60}, value="15 minutes", label="Polling interval", full_width=True)
    hours = mo.ui.slider(1, 24, value=8, label="Active hours per day", show_value=True)
    days = mo.ui.slider(1, 31, value=30, label="Days in your study", show_value=True)
    weight = mo.ui.slider(0, 10, value=3, label="Hypothetical credits per request", show_value=True)
    mo.vstack([interval, mo.hstack([hours, days, weight], wrap=True)])
    return days, hours, interval, weight


@app.cell(hide_code=True)
def _(days, hours, interval, weight):
    estimate = workload(interval.value, hours.value, days.value, weight.value)
    continuous = workload(1, 24, days.value, weight.value)
    ratio = continuous["calls_monthly"] / estimate["calls_monthly"]
    mo.vstack([
        mo.Html(f"""<div class='lab-kpis' role='status'>
        <div><b>{estimate['calls_monthly']:,}</b><span>HTTP requests per study</span></div>
        <div><b>{estimate['credits_monthly']:,}</b><span>hypothetical credits per study</span></div>
        <div><b>{estimate['unobserved_hours_daily']}</b><span>unobserved hours each day</span></div>
        </div>"""),
        mo.Html(observation_diagram(interval.value, hours.value)),
        mo.md(f"""
        **Your schedule:** {estimate['calls_daily']:,} requests/day x {days.value} days
        = **{estimate['calls_monthly']:,} requests**, each weighted at {weight.value} hypothetical credits.

        **Reference:** every minute for 24 hours over the same {days.value} days
        = **{continuous['calls_monthly']:,} requests** and **{continuous['credits_monthly']:,} hypothetical credits**.
        The reference makes **{ratio:g} times as many requests**. It has a different
        sampling interval and/or observation window whenever those controls differ.
        This is a workload comparison, not a monetary savings claim.
        """),
    ])
    return continuous, estimate, ratio


@app.cell(hide_code=True)
def _():
    mo.accordion({
        "Read the model's limits": mo.md("""
        A request occurs at the start of each active window and every interval
        thereafter, stopping before the window ends. Windows start at 00:00 on
        each fictional day. There are no retries, failures, caching, pagination,
        provider refresh delays or polling jitter in this model.

        HTTP requests are not necessarily billed credits. The credit weight is
        an input to this lesson, not a vendor price or promise about a free plan.
        Real costs depend on the provider and request scope.

        Polling more often does not guarantee new source data. Polling less often
        cannot reconstruct changes between observations. A source age threshold
        expresses an assumption, not a guarantee of quality.

        Comparability here checks declared fields only. Real settlement terms,
        limits, availability, identity mapping and timezone handling need their
        own validation. No part of this lesson recommends a wager.
        """),
        "Try three experiments": mo.md("""
        1. Select **Same contract**, then raise B's source age above your maximum.
           Notice that retrieval at 12:00 does not repair the old source time.
        2. Select **Duplicate candidate records**. Both prices remain visible;
           the notebook does not choose the newest or more favorable one.
        3. Change the polling interval to **1 minute** and active hours to **24**.
           Then change only the credit weight. Request count stays fixed.
        """),
    })
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    ### About this lesson

    Prepared by the **ParlayAPI team with AI assistance**.
    [Source and study guide](https://github.com/JacobiusMakes/parlayapi-notebooks/tree/astra/synthetic-comparability-lab-20260906/labs/odds-comparability)
    | [MIT software license](https://github.com/JacobiusMakes/parlayapi-notebooks/blob/astra/synthetic-comparability-lab-20260906/labs/odds-comparability/LICENSE).
    All examples are synthetic; no API data rights are granted.
    """)
    return


if __name__ == "__main__":
    app.run()
