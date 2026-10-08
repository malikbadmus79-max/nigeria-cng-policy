"""
export_png.py
-------------
Static PNG copies of the main charts, for the policy brief and slides.

Output: outputs/figures/png/*.png, 1200 px wide, white background.

Three charts already exist as interactive HTML (made by notebooks 01, 04 and
07). Rather than copy their code here, we read each figure back out of its HTML
file, so the PNG is exactly the chart the notebook made. The fourth chart (the
chance CNG pays at fixed daily queue times, notebook 06) had no chart of its
own, so it is built here from the same simulation runs.

Readability at small size: most charts are laid out at 800 px and exported at
scale 1.5. The result is 1200 px wide, but text is drawn 1.5x larger relative to
the image than in the 1200 px-wide layout, so labels stay legible when the
image is shrunk on a page.

Needs kaleido (plotly's image exporter), which drives a local Chrome.

Run from the project root:
    python src/export_png.py
"""

import json
import pathlib

import plotly.graph_objects as go

import monte_carlo as mc

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
PNG_DIR = FIG_DIR / "png"

LAYOUT_WIDTH = 800        # px the chart is laid out at; exported at scale 1.5 -> 1200 px
INK, INK_MUTED, GRID = "#0b0b0b", "#52514e", "#ecebe7"
BLUE, GREY = "#2a78d6", "#8a8984"


def figure_from_html(path: pathlib.Path) -> go.Figure:
    """
    Rebuild a plotly figure from an HTML file written by fig.write_html.

    The file contains a call like Plotly.newPlot("id", [data...], {layout...}, {config}).
    json.JSONDecoder.raw_decode reads one complete JSON value starting at a
    position and tells us where it ended, so we can read data, then layout.
    """
    text = path.read_text(encoding="utf-8")
    start = text.index("Plotly.newPlot(")
    pos = text.index(",", start) + 1            # skip the div id argument
    decoder = json.JSONDecoder()

    def next_value(i):
        while text[i] in " \n\r\t,":
            i += 1
        return decoder.raw_decode(text, i)

    data, pos = next_value(pos)
    layout, _ = next_value(pos)
    return go.Figure(data=data, layout=layout)


def queue_cap_figure() -> go.Figure:
    """Bar chart: probability CNG pays (market price) with daily queue fixed at 1-4 hours, plus as surveyed."""
    labels, probs = [], []
    for hours in [1, 2, 3, 4]:
        r = mc.run_simulation(conversion="market", queue_hours_fixed=hours)
        labels.append(f"{hours} hour{'s' if hours > 1 else ''}")
        probs.append((r["net_benefit"] > 0).mean())
    surveyed = mc.run_simulation(conversion="market")
    labels.append("As surveyed")
    probs.append((surveyed["net_benefit"] > 0).mean())

    fig = go.Figure(go.Bar(
        x=labels, y=probs, width=0.6,
        marker=dict(color=[BLUE] * 4 + [GREY], cornerradius=4),
        text=[f"{p:.0%}" for p in probs], textposition="outside", cliponaxis=False,
        textfont=dict(color=INK, size=14),
    ))
    fig.update_layout(
        title=dict(text="The chance CNG pays falls steeply as daily queuing grows<br>"
                        "<sup>Probability net benefit > 0 at market kit prices, daily queue time held fixed. "
                        "10,000 Monte Carlo draws each (notebook 06).</sup>", x=0, xanchor="left"),
        template="plotly_white", font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=13, color=INK),
        xaxis=dict(title="Daily queue time"),
        yaxis=dict(title="Probability CNG pays", tickformat=".0%", range=[0, 1.1], dtick=0.25, gridcolor=GRID),
        showlegend=False, width=820, height=460, margin=dict(t=100, l=70, r=30, b=60),
    )
    return fig


def export(fig: go.Figure, name: str, layout_width=LAYOUT_WIDTH, **layout_fixes) -> pathlib.Path:
    """
    Save fig as a 1200 px wide PNG.

    layout_width: px to lay the chart out at; scale = 1200 / layout_width. Charts
        designed for a wide browser window need a larger value to avoid overlaps.
    layout_fixes: extra fig.update_layout settings for the static copy only
        (e.g. a wider margin so a long label isn't cut off).
    """
    # Keep each chart's own proportions.
    width, height = fig.layout.width or 1000, fig.layout.height or 500
    fig.update_layout(
        width=layout_width, height=round(height * layout_width / width),
        paper_bgcolor="white", plot_bgcolor="white",
    )
    fig.update_layout(**layout_fixes)
    out = PNG_DIR / f"{name}.png"
    fig.write_image(out, scale=1200 / layout_width)
    return out


def main() -> None:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    saved = [
        export(queue_cap_figure(), "queue_cap"),
        export(figure_from_html(FIG_DIR / "barriers.html"), "barriers"),
        # Wider right margin: the longest bar label ("+36.4 pts") was cut off.
        export(figure_from_html(FIG_DIR / "policy_options_impact.html"), "policy_options_impact",
               margin_r=110),
        # Built for a full-width browser window: lay out wider, give the legend room
        # below the subtitle, and drop the x-axis title, which collided with the source note.
        export(figure_from_html(FIG_DIR / "petrol_vs_cng.html"), "petrol_vs_cng",
               layout_width=1000, margin_t=175, xaxis_title_text=None),
    ]
    for out in saved:
        print(f"Saved {out.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
