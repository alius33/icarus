"""
Generate a Moody's-branded PDF: CS Gen AI Programme — Strategic Scorecard Alignment.
McKinsey-level strategic briefing with industry benchmarks, financial quantification,
corporate alignment, new AI project proposals, and resource model.
"""
import os, sys, textwrap, tempfile
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from fpdf import FPDF

# ── Moody's brand palette ───────────────────────────────────────────
NAVY   = (9, 17, 100)
BLUE   = (0, 94, 255)
WHITE  = (255, 255, 255)
LGRAY  = (242, 244, 248)
MGRAY  = (107, 114, 128)
DARK   = (31, 41, 55)
RED    = (220, 53, 69)
GREEN  = (16, 185, 129)
AMBER  = (245, 158, 11)

# matplotlib-friendly versions (0-1 range)
mNAVY  = tuple(c/255 for c in NAVY)
mBLUE  = tuple(c/255 for c in BLUE)
mLGRAY = tuple(c/255 for c in LGRAY)
mDARK  = tuple(c/255 for c in DARK)
mRED   = tuple(c/255 for c in RED)
mGREEN = tuple(c/255 for c in GREEN)
mAMBER = tuple(c/255 for c in AMBER)
mWHITE = (1, 1, 1)

DOC_DATE = "14 March 2026"


# ── Chart generation ────────────────────────────────────────────────

def _save_fig(fig, tmpdir, name):
    p = os.path.join(tmpdir, name)
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p


# ────────────────────────────────────────────────────────────────────
# CHART 1: Correlation heatmap
# ────────────────────────────────────────────────────────────────────
def gen_heatmap(tmpdir):
    """Correlation heatmap: projects (rows) x scorecard pillars (cols)."""
    projects = [
        "CLARA",
        "Build in Five",
        "Training &\nEnablement",
        "Navigator L1\nAutomation",
        "App Factory",
        "Cross-OU\nCollaboration",
        "Friday",
        "CS Agent",
        "TSR\nEnhancements",
    ]
    pillars = [
        "IRP\nMigrations",
        "GNB\nGrowth",
        "Customer\nSuccess",
        "AI\nAdoption",
        "Efficiency /\nCost",
        "Agentic\nWorkflows",
        "Risk &\nSecurity",
        "People &\nCulture",
    ]

    # Score 0-3: 0=none, 1=indirect, 2=strong, 3=direct hit
    data = np.array([
        [3, 2, 3, 1, 1, 0, 0, 0],  # CLARA
        [1, 3, 1, 2, 1, 3, 0, 0],  # Build in Five
        [0, 0, 1, 3, 2, 0, 0, 3],  # Training
        [1, 1, 3, 3, 2, 1, 0, 0],  # Navigator
        [0, 1, 1, 2, 3, 3, 1, 0],  # App Factory
        [0, 2, 2, 1, 0, 0, 0, 2],  # Cross-OU
        [0, 0, 1, 2, 2, 1, 0, 1],  # Friday
        [0, 0, 2, 2, 1, 2, 0, 0],  # CS Agent
        [0, 0, 1, 2, 3, 1, 1, 0],  # TSR Enhancements
    ])

    fig, ax = plt.subplots(figsize=(10, 6.5))
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("moody",
        [(1,1,1), (0.78, 0.85, 1.0), mBLUE, mNAVY])

    im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=3)

    ax.set_xticks(range(len(pillars)))
    ax.set_xticklabels(pillars, fontsize=8, ha="center")
    ax.set_yticks(range(len(projects)))
    ax.set_yticklabels(projects, fontsize=9)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False,
                   length=0)

    labels = {0: "", 1: "Indirect", 2: "Strong", 3: "Direct\nHit"}
    for i in range(len(projects)):
        for j in range(len(pillars)):
            v = data[i, j]
            c = "white" if v >= 2 else mDARK
            ax.text(j, i, labels[v], ha="center", va="center",
                    fontsize=7, color=c, fontweight="bold" if v == 3 else "normal")

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=cmap(0.0), edgecolor=mDARK, label="No link"),
        Patch(facecolor=cmap(0.33), edgecolor=mDARK, label="Indirect"),
        Patch(facecolor=cmap(0.66), edgecolor=mDARK, label="Strong"),
        Patch(facecolor=cmap(1.0), edgecolor=mDARK, label="Direct Hit"),
    ]
    ax.legend(handles=legend_elements, loc="upper left",
              bbox_to_anchor=(1.02, 1), fontsize=8, frameon=True)

    ax.set_title("Programme-Scorecard Correlation Matrix",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=50)

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    return _save_fig(fig, tmpdir, "heatmap.png")


# ────────────────────────────────────────────────────────────────────
# CHART 2: Quick-wins quadrant
# ────────────────────────────────────────────────────────────────────
def gen_quadrant(tmpdir):
    """Impact vs Effort quadrant for quick-win identification."""
    items = [
        # (name, effort 0-10, impact 0-10, color)
        ("Navigator L1\n(WS5)", 2, 9, mBLUE),
        ("Training &\nEnablement (WS1)", 3, 8, mGREEN),
        ("Build in Five\nSales Enablement", 3, 9, mNAVY),
        ("Gainsight\nTransition", 4, 7, mBLUE),
        ("AS Agentic\nWorkflows", 5, 9, mAMBER),
        ("Cross-OU\nScaling", 6, 7, mAMBER),
        ("CLARA (already\ndelivering)", 1, 10, mGREEN),
        ("Friday PM\nApp", 5, 4, mDARK),
        ("CS Agent\n(WS3)", 4, 6, mAMBER),
        ("TSR\nEnhancements", 3, 5, mBLUE),
    ]

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 10.5)

    ax.axhline(y=5, color=mLGRAY, linewidth=1.5, linestyle="--")
    ax.axvline(x=5, color=mLGRAY, linewidth=1.5, linestyle="--")

    ax.text(2.5, 8, "QUICK WINS", ha="center", va="center",
            fontsize=18, color=(*mGREEN, 0.15), fontweight="bold")
    ax.text(7.5, 8, "STRATEGIC\nINVESTMENTS", ha="center", va="center",
            fontsize=14, color=(*mBLUE, 0.15), fontweight="bold")
    ax.text(2.5, 2.5, "EASY FILLS", ha="center", va="center",
            fontsize=14, color=(*mLGRAY, 0.6), fontweight="bold")
    ax.text(7.5, 2.5, "RECONSIDER", ha="center", va="center",
            fontsize=14, color=(*mRED, 0.12), fontweight="bold")

    for name, effort, impact, color in items:
        ax.scatter(effort, impact, s=350, c=[color], edgecolors="white",
                   linewidth=2, zorder=5)
        ax.annotate(name, (effort, impact), fontsize=7.5, ha="center",
                    va="bottom", xytext=(0, 14), textcoords="offset points",
                    fontweight="bold", color=mDARK,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white",
                              ec=(*color, 0.3), alpha=0.9))

    ax.set_xlabel("Effort Required  -->", fontsize=11, color=mDARK, fontweight="bold")
    ax.set_ylabel("<-- Scorecard Impact", fontsize=11, color=mDARK, fontweight="bold")
    ax.set_title("Quick Wins: Scorecard Impact vs Effort",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=15)
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_color(mLGRAY)
    ax.tick_params(colors=mDARK)

    fig.tight_layout()
    return _save_fig(fig, tmpdir, "quadrant.png")


# ────────────────────────────────────────────────────────────────────
# CHART 3: Coverage radar
# ────────────────────────────────────────────────────────────────────
def gen_coverage_wheel(tmpdir):
    """Radar / spider chart of scorecard coverage by the programme."""
    categories = [
        "IRP Migrations", "GNB Growth", "Customer Success",
        "AI Adoption", "Efficiency", "Agentic Workflows",
        "Risk & Security", "People & Culture"
    ]
    scores = [95, 65, 85, 90, 70, 75, 15, 75]

    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    scores_plot = scores + [scores[0]]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    ax.fill(angles, scores_plot, color=(*mBLUE, 0.15))
    ax.plot(angles, scores_plot, color=mBLUE, linewidth=2.5)
    ax.scatter(angles[:-1], scores, s=80, color=mNAVY, zorder=5)

    for angle, score, cat in zip(angles[:-1], scores, categories):
        ax.annotate(f"{score}%", (angle, score), fontsize=9,
                    fontweight="bold", ha="center", va="bottom",
                    xytext=(0, 8), textcoords="offset points", color=mNAVY)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, color=mDARK, fontweight="bold")
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=7, color=mDARK)
    ax.yaxis.grid(True, color=mLGRAY, linewidth=0.5)
    ax.xaxis.grid(True, color=mLGRAY, linewidth=0.5)
    ax.spines["polar"].set_color(mLGRAY)

    ax.set_title("Programme Coverage of Scorecard Pillars",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=25)

    fig.tight_layout()
    return _save_fig(fig, tmpdir, "coverage.png")


# ────────────────────────────────────────────────────────────────────
# CHART 4: Flow diagram
# ────────────────────────────────────────────────────────────────────
def gen_flow_diagram(tmpdir):
    """Flow diagram: Programme projects -> Scorecard targets -> Business outcomes."""
    fig, ax = plt.subplots(figsize=(12, 8.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    ax.set_facecolor("white")

    for x, label in [(1.3, "YOUR PROJECTS"), (5.5, "SCORECARD TARGETS"), (9.5, "BUSINESS OUTCOMES")]:
        ax.text(x, 9.2, label, ha="center", va="center", fontsize=10,
                fontweight="bold", color=mNAVY)

    projects = [
        ("CLARA", 8.4, mNAVY),
        ("Build in Five", 7.5, mBLUE),
        ("Training (WS1)", 6.6, mGREEN),
        ("Navigator (WS5)", 5.7, mBLUE),
        ("App Factory", 4.8, mAMBER),
        ("Cross-OU", 3.9, mDARK),
        ("Friday", 3.0, mDARK),
        ("CS Agent (WS3)", 2.1, mAMBER),
        ("TSR Enhance.", 1.2, mBLUE),
    ]
    for name, y, color in projects:
        box = FancyBboxPatch((0.2, y - 0.3), 2.2, 0.6,
                             boxstyle="round,pad=0.1", fc=(*color, 0.12),
                             ec=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(1.3, y, name, ha="center", va="center", fontsize=7.5,
                fontweight="bold", color=color)

    targets = [
        ("32 IRP Migrations", 8.4),
        ("$111M GNB / 8.4% ARR", 7.3),
        ("25% Navigator\nAdoption", 6.2),
        ("90% AI Tool\nUsage", 5.1),
        ("$150K AS Cost\nSaving", 4.0),
        ("Gainsight Q2\nTransition", 2.9),
        ("Tiered CS\nModel", 1.8),
    ]
    for name, y in targets:
        box = FancyBboxPatch((4.2, y - 0.35), 2.6, 0.7,
                             boxstyle="round,pad=0.1", fc=(*mBLUE, 0.08),
                             ec=mBLUE, linewidth=1.2)
        ax.add_patch(box)
        ax.text(5.5, y, name, ha="center", va="center", fontsize=7,
                fontweight="bold", color=mNAVY)

    outcomes = [
        ("Retain $896M\nARR Base", 7.8, mGREEN),
        ("Revenue\nGrowth", 6.0, mBLUE),
        ("Operational\nEfficiency", 4.2, mAMBER),
        ("Agentic\nWorld Ready", 2.4, mNAVY),
    ]
    for name, y, color in outcomes:
        box = FancyBboxPatch((8.5, y - 0.35), 2.0, 0.7,
                             boxstyle="round,pad=0.1", fc=(*color, 0.15),
                             ec=color, linewidth=1.8)
        ax.add_patch(box)
        ax.text(9.5, y, name, ha="center", va="center", fontsize=8,
                fontweight="bold", color=color)

    arrow_kw = dict(arrowstyle="->,head_width=0.15,head_length=0.1",
                    color=(*mBLUE, 0.35), linewidth=1.0,
                    connectionstyle="arc3,rad=0.05")
    arrows = [
        ((2.4, 8.4), (4.2, 8.4)),
        ((2.4, 8.2), (4.2, 7.4)),
        ((2.4, 8.1), (4.2, 3.0)),
        ((2.4, 8.1), (4.2, 1.9)),
        ((2.4, 7.5), (4.2, 7.3)),
        ((2.4, 7.3), (4.2, 6.3)),
        ((2.4, 6.6), (4.2, 5.1)),
        ((2.4, 5.7), (4.2, 6.2)),
        ((2.4, 5.9), (4.2, 5.2)),
        ((2.4, 4.8), (4.2, 4.0)),
        ((2.4, 5.0), (4.2, 5.0)),
        ((2.4, 4.1), (4.2, 7.2)),
        ((2.4, 3.0), (4.2, 1.8)),
        ((2.4, 3.2), (4.2, 3.9)),
        ((2.4, 2.1), (4.2, 1.8)),
        ((2.4, 2.3), (4.2, 4.9)),
        ((2.4, 1.2), (4.2, 3.8)),
    ]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=arrow_kw)

    arrow_kw2 = dict(arrowstyle="->,head_width=0.15,head_length=0.1",
                     color=(*mNAVY, 0.3), linewidth=1.0,
                     connectionstyle="arc3,rad=0.05")
    arrows2 = [
        ((6.8, 8.4), (8.5, 7.9)),
        ((6.8, 7.3), (8.5, 7.7)),
        ((6.8, 7.3), (8.5, 6.1)),
        ((6.8, 6.2), (8.5, 5.9)),
        ((6.8, 5.1), (8.5, 2.5)),
        ((6.8, 4.0), (8.5, 4.3)),
        ((6.8, 2.9), (8.5, 4.1)),
        ((6.8, 1.8), (8.5, 7.7)),
    ]
    for start, end in arrows2:
        ax.annotate("", xy=end, xytext=start, arrowprops=arrow_kw2)

    ax.set_title("How the Programme Delivers Scorecard Outcomes",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=10)
    fig.tight_layout()
    return _save_fig(fig, tmpdir, "flow.png")


# ────────────────────────────────────────────────────────────────────
# CHART 5: Gaps bar chart
# ────────────────────────────────────────────────────────────────────
def gen_gaps_chart(tmpdir):
    """Horizontal bar chart showing gaps / vulnerabilities."""
    gaps = [
        ("WS1 Training -- no deliverables yet", 85, mRED),
        ("WS5 Navigator -- no CS ownership", 75, mRED),
        ("WS3 CS Agent -- unconnected prototype", 70, mAMBER),
        ("Cost management -- zero attribution", 70, mAMBER),
        ("Kathryn Palkovics COE overlap", 65, mAMBER),
        ("Cross-OU demand unfunded", 60, mAMBER),
    ]
    names = [g[0] for g in gaps]
    scores = [g[1] for g in gaps]
    colors = [g[2] for g in gaps]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    y_pos = range(len(names))
    bars = ax.barh(y_pos, scores, color=colors, edgecolor="white", height=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9, color=mDARK)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Risk / Exposure Level", fontsize=10, color=mDARK, fontweight="bold")
    ax.invert_yaxis()

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{score}%", ha="left", va="center", fontsize=9,
                fontweight="bold", color=mDARK)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(mLGRAY)
    ax.spines["left"].set_color(mLGRAY)

    ax.set_title("Gaps & Vulnerabilities to Address",
                 fontsize=12, fontweight="bold", color=mNAVY, pad=12)
    fig.tight_layout()
    return _save_fig(fig, tmpdir, "gaps.png")


# ────────────────────────────────────────────────────────────────────
# CHART 6: Three-Horizon Roadmap (NEW)
# ────────────────────────────────────────────────────────────────────
def gen_three_horizon(tmpdir):
    """Three-horizon strategic roadmap visualisation."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor("white")

    # Three horizon bands
    horizons = [
        (0.3, 3.8, "HORIZON 1: Delivering Now", "Q1 2026",
         mGREEN, (*mGREEN, 0.08),
         [("CLARA", "31 migration accounts tracked, Portfolio Reviews live"),
          ("Build in Five", "Sales demo ready, MCP integration in weeks"),
          ("Training", "Cross-OU sessions delivered, Cursor adoption spreading"),
          ("TSR Enhancements", "Cat bond automation scoped, Idris building")]),
        (4.2, 7.8, "HORIZON 2: Scaling the Platform", "Q2-Q3 2026",
         mBLUE, (*mBLUE, 0.06),
         [("Navigator L1", "Champion adoption, measure support case reduction"),
          ("Gainsight", "Bi-directional CLARA integration, CS transition"),
          ("AS Agentic", "75% of accounts on agentic workflows by Q3"),
          ("Cross-OU", "Scale CLARA template to Banking & Life")]),
        (8.2, 11.8, "HORIZON 3: Strategic Bets", "Q4 2026+",
         mNAVY, (*mNAVY, 0.06),
         [("CS Agent", "Unified agentic CS across divisions"),
          ("KYC/Compliance", "Insurance-specific agentic solution"),
          ("Risk Dashboards", "Automated Tier 1&2 product dashboards"),
          ("NatCat Full AI", "100% agentic NatCat modelling")]),
    ]

    for x_start, x_end, title, period, color, bg_color, items in horizons:
        w = x_end - x_start
        # Background band
        rect = FancyBboxPatch((x_start, 0.3), w, 7.2,
                              boxstyle="round,pad=0.15", fc=bg_color,
                              ec=color, linewidth=2)
        ax.add_patch(rect)
        # Title
        ax.text(x_start + w/2, 7.0, title, ha="center", va="center",
                fontsize=9, fontweight="bold", color=color)
        ax.text(x_start + w/2, 6.5, period, ha="center", va="center",
                fontsize=8, color=(*color, 0.7))
        # Items
        for i, (name, desc) in enumerate(items):
            y = 5.5 - i * 1.3
            # Item box
            item_box = FancyBboxPatch((x_start + 0.15, y - 0.35), w - 0.3, 0.9,
                                      boxstyle="round,pad=0.08", fc="white",
                                      ec=(*color, 0.4), linewidth=1)
            ax.add_patch(item_box)
            ax.text(x_start + 0.35, y + 0.1, name, fontsize=8,
                    fontweight="bold", color=color, va="center")
            ax.text(x_start + 0.35, y - 0.15, desc, fontsize=6.5,
                    color=mDARK, va="center", wrap=True)

    # Arrows between horizons
    for x in [3.9, 8.1]:
        ax.annotate("", xy=(x + 0.2, 3.8), xytext=(x - 0.1, 3.8),
                    arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.15",
                                   color=mNAVY, linewidth=2))

    ax.set_title("Three-Horizon Strategic Roadmap",
                 fontsize=14, fontweight="bold", color=mNAVY, pad=15)
    fig.tight_layout()
    return _save_fig(fig, tmpdir, "three_horizon.png")


# ────────────────────────────────────────────────────────────────────
# CHART 7: Quarterly roadmap vs scorecard gates (NEW)
# ────────────────────────────────────────────────────────────────────
def gen_quarterly_roadmap(tmpdir):
    """Gantt-style chart: project milestones vs scorecard deadlines."""
    fig, ax = plt.subplots(figsize=(13, 7.5))

    quarters = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    projects = [
        "CLARA",
        "Build in Five",
        "Training",
        "Navigator L1",
        "App Factory",
        "Cross-OU",
        "Friday",
        "CS Agent",
        "TSR Enhancements",
    ]

    # Gantt bars: (project_idx, start_month, end_month, color, label)
    bars = [
        (0, 0, 11, mNAVY, "Live -- continuous IRP tracking"),
        (1, 0, 4, mBLUE, "Sales demo + MCP integration"),
        (2, 0, 11, mGREEN, "Rolling enablement programme"),
        (3, 2, 8, mBLUE, "Champion adoption + measure"),
        (4, 0, 11, mAMBER, "MCP platform + AS deployment"),
        (5, 1, 9, mDARK, "Banking + Life scaling"),
        (6, 1, 5, mDARK, "PM app build + approval"),
        (7, 4, 11, mAMBER, "Unify prototypes + deploy"),
        (8, 2, 7, mBLUE, "Cat bond automation build"),
    ]

    for proj_idx, start, end, color, label in bars:
        ax.barh(proj_idx, end - start + 0.8, left=start, height=0.5,
                color=(*color, 0.25), edgecolor=color, linewidth=1.5)
        ax.text(start + 0.1, proj_idx, label, fontsize=7, color=color,
                va="center", fontweight="bold")

    # Scorecard deadlines (vertical lines)
    deadlines = [
        (2, "Q1: Sales\nEnablement", mGREEN),
        (5, "Q2: Gainsight\nTransition", mBLUE),
        (5, "Q2: AS Quick Start\n& CatMoSAI", mAMBER),
        (8, "Q3: 75% AS\nAgentic AI", mRED),
        (11, "Q4: NatCat\n100% Agentic", mNAVY),
    ]
    for month, label, color in deadlines:
        ax.axvline(x=month, color=color, linewidth=1.5, linestyle="--", alpha=0.6)
        # Offset labels to avoid overlap
        y_offset = 9.5 if month <= 5 else 9.5
        ax.text(month + 0.1, -1.2, label, fontsize=7, color=color,
                fontweight="bold", rotation=0, va="top", ha="left")

    ax.set_yticks(range(len(projects)))
    ax.set_yticklabels(projects, fontsize=9, color=mDARK, fontweight="bold")
    ax.set_xticks(range(12))
    ax.set_xticklabels(quarters, fontsize=9, color=mDARK)
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-2.5, len(projects) - 0.3)
    ax.invert_yaxis()

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(mLGRAY)
    ax.spines["left"].set_color(mLGRAY)

    # Q1-Q4 band labels at top
    for q, (start, end, label) in enumerate([(0, 2, "Q1"), (3, 5, "Q2"),
                                              (6, 8, "Q3"), (9, 11, "Q4")]):
        mid = (start + end) / 2
        ax.text(mid, -0.7, label, ha="center", va="center", fontsize=10,
                fontweight="bold", color=mNAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc=(*mBLUE, 0.08),
                          ec=mBLUE, linewidth=1))

    ax.set_title("2026 Delivery Timeline vs Scorecard Deadlines",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=20)
    fig.tight_layout()
    return _save_fig(fig, tmpdir, "quarterly.png")


# ────────────────────────────────────────────────────────────────────
# CHART 8: Value driver tree (NEW)
# ────────────────────────────────────────────────────────────────────
def gen_value_driver_tree(tmpdir):
    """Value driver tree: activities -> metrics -> financial impact."""
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_facecolor("white")

    # Column headers
    headers = [
        (1.5, "PROGRAMME\nACTIVITIES"),
        (5.0, "OPERATING\nMETRICS"),
        (8.5, "SCORECARD\nKPIs"),
        (11.5, "FINANCIAL\nIMPACT"),
    ]
    for x, label in headers:
        ax.text(x, 9.5, label, ha="center", va="center", fontsize=9,
                fontweight="bold", color=mNAVY)

    # Activities (left column)
    activities = [
        ("CLARA Portfolio\nReviews", 8.0, mNAVY),
        ("Build in Five\nSales Demos", 6.5, mBLUE),
        ("Cursor/Claude\nTraining", 5.0, mGREEN),
        ("App Factory\nMCP Deployment", 3.5, mAMBER),
        ("Navigator L1\nAutomation", 2.0, mBLUE),
    ]
    for name, y, color in activities:
        box = FancyBboxPatch((0.3, y - 0.35), 2.4, 0.7,
                             boxstyle="round,pad=0.1", fc=(*color, 0.12),
                             ec=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(1.5, y, name, ha="center", va="center", fontsize=7,
                fontweight="bold", color=color)

    # Operating metrics (middle-left)
    metrics = [
        ("Migration velocity\n+40% QoQ", 8.0),
        ("IRP demo\nconversion +25%", 6.5),
        ("AI tool adoption\n90% weekly", 5.0),
        ("AS process time\n-60%", 3.5),
        ("L1 ticket volume\n-30%", 2.0),
    ]
    for name, y in metrics:
        box = FancyBboxPatch((3.8, y - 0.35), 2.4, 0.7,
                             boxstyle="round,pad=0.1", fc=(*mBLUE, 0.08),
                             ec=mBLUE, linewidth=1.2)
        ax.add_patch(box)
        ax.text(5.0, y, name, ha="center", va="center", fontsize=7,
                fontweight="bold", color=mNAVY)

    # Scorecard KPIs (middle-right)
    kpis = [
        ("32 migrations\ncompleted", 7.5),
        ("$111M GNB\n8.4% ARR growth", 6.0),
        ("$150K AS saving\n20 staff redeployed", 4.0),
        ("25% Navigator\nadoption", 2.5),
    ]
    for name, y in kpis:
        box = FancyBboxPatch((7.3, y - 0.35), 2.4, 0.7,
                             boxstyle="round,pad=0.1", fc=(*mGREEN, 0.08),
                             ec=mGREEN, linewidth=1.2)
        ax.add_patch(box)
        ax.text(8.5, y, name, ha="center", va="center", fontsize=7,
                fontweight="bold", color=mDARK)

    # Financial impact (right column)
    impacts = [
        ("Protect\n$896M ARR", 7.2, mGREEN),
        ("Drive $69M\nnet ARR growth", 5.5, mBLUE),
        ("$150K direct\ncost saving", 3.8, mAMBER),
        ("Reduce support\ncost by ~$200K", 2.2, mAMBER),
    ]
    for name, y, color in impacts:
        box = FancyBboxPatch((10.3, y - 0.35), 2.4, 0.7,
                             boxstyle="round,pad=0.1", fc=(*color, 0.15),
                             ec=color, linewidth=1.8)
        ax.add_patch(box)
        ax.text(11.5, y, name, ha="center", va="center", fontsize=8,
                fontweight="bold", color=color)

    # Connecting arrows (activity -> metric -> KPI -> impact)
    arrow_kw = dict(arrowstyle="->,head_width=0.12,head_length=0.08",
                    color=(*mBLUE, 0.3), linewidth=1.0,
                    connectionstyle="arc3,rad=0.05")
    # Activity -> Metric connections
    for y in [8.0, 6.5, 5.0, 3.5, 2.0]:
        ax.annotate("", xy=(3.8, y), xytext=(2.7, y), arrowprops=arrow_kw)
    # Metric -> KPI connections
    connections_mk = [
        ((6.2, 8.0), (7.3, 7.5)),
        ((6.2, 6.5), (7.3, 6.0)),
        ((6.2, 5.0), (7.3, 6.0)),
        ((6.2, 3.5), (7.3, 4.0)),
        ((6.2, 2.0), (7.3, 2.5)),
    ]
    for start, end in connections_mk:
        ax.annotate("", xy=end, xytext=start, arrowprops=arrow_kw)
    # KPI -> Impact connections
    connections_ki = [
        ((9.7, 7.5), (10.3, 7.2)),
        ((9.7, 6.0), (10.3, 5.5)),
        ((9.7, 4.0), (10.3, 3.8)),
        ((9.7, 2.5), (10.3, 2.2)),
    ]
    arrow_kw2 = dict(arrowstyle="->,head_width=0.12,head_length=0.08",
                     color=(*mNAVY, 0.3), linewidth=1.0,
                     connectionstyle="arc3,rad=0.05")
    for start, end in connections_ki:
        ax.annotate("", xy=end, xytext=start, arrowprops=arrow_kw2)

    # Total box at bottom right
    total_box = FancyBboxPatch((10.0, 0.5), 2.8, 0.9,
                                boxstyle="round,pad=0.12", fc=(*mNAVY, 0.1),
                                ec=mNAVY, linewidth=2)
    ax.add_patch(total_box)
    ax.text(11.4, 0.95, "Total Addressable Value", ha="center", va="center",
            fontsize=8, fontweight="bold", color=mNAVY)
    ax.text(11.4, 0.65, "$896M+ ARR protected + $1.2M efficiency gains",
            ha="center", va="center", fontsize=7, color=mDARK)

    ax.set_title("Value Driver Tree: Activities to Financial Impact",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=10)
    fig.tight_layout()
    return _save_fig(fig, tmpdir, "value_tree.png")


# ────────────────────────────────────────────────────────────────────
# CHART 9: Resource model (NEW)
# ────────────────────────────────────────────────────────────────────
def gen_resource_chart(tmpdir):
    """Stacked bar chart: current team vs needed team."""
    fig, ax = plt.subplots(figsize=(10, 5.5))

    categories = ["Current State", "Minimum Viable", "Target State"]
    roles = {
        "Programme Lead": [1, 1, 1],
        "Developer / Builder": [2, 3, 4],
        "PM / Analyst": [1, 2, 2],
        "Enablement / Training": [0, 1, 2],
        "Infrastructure / DevOps": [1, 1, 1],
        "Part-time Contributors": [2, 2, 3],
    }

    x = np.arange(len(categories))
    width = 0.5
    colors = [mNAVY, mBLUE, mAMBER, mGREEN, mDARK, (*mBLUE, 0.4)]

    bottom = np.zeros(len(categories))
    for i, (role, counts) in enumerate(roles.items()):
        bars = ax.bar(x, counts, width, bottom=bottom, label=role,
                      color=colors[i], edgecolor="white", linewidth=1)
        # Add count labels in bars if > 0
        for j, (count, b) in enumerate(zip(counts, bottom)):
            if count > 0:
                ax.text(j, b + count/2, str(count), ha="center", va="center",
                        fontsize=8, fontweight="bold", color="white")
        bottom += np.array(counts)

    # Total labels on top
    totals = [sum(v[i] for v in roles.values()) for i in range(len(categories))]
    for j, total in enumerate(totals):
        ax.text(j, total + 0.3, f"Total: {total}", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=mNAVY)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11, fontweight="bold", color=mDARK)
    ax.set_ylabel("Headcount", fontsize=10, color=mDARK, fontweight="bold")
    ax.set_ylim(0, max(totals) + 2)

    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8, frameon=True)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(mLGRAY)
    ax.spines["left"].set_color(mLGRAY)

    ax.set_title("Resource Model: Current vs Required",
                 fontsize=13, fontweight="bold", color=mNAVY, pad=15)
    fig.tight_layout()
    return _save_fig(fig, tmpdir, "resources.png")


# ────────────────────────────────────────────────────────────────────
# CHART 10: Cost of inaction (NEW)
# ────────────────────────────────────────────────────────────────────
def gen_cost_of_inaction(tmpdir):
    """Visual showing what happens if the programme doesn't get funded."""
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    ax.set_facecolor("white")

    # Title bar
    ax.text(5.5, 8.0, "If the Programme Doesn't Get Formal Support...",
            ha="center", va="center", fontsize=14, fontweight="bold", color=mRED)

    # Two columns: what you lose (left) vs what competitors gain (right)
    ax.text(2.75, 7.2, "WHAT YOU LOSE", ha="center", va="center",
            fontsize=11, fontweight="bold", color=mRED)
    ax.text(8.25, 7.2, "WHAT COMPETITORS GAIN", ha="center", va="center",
            fontsize=11, fontweight="bold", color=mNAVY)

    # Divider line
    ax.plot([5.5, 5.5], [0.5, 7.0], color=mLGRAY, linewidth=2, linestyle="--")

    # Left column: losses
    losses = [
        ("$896M ARR at risk", "IRP migrations untracked,\nPortfolio Reviews collapse"),
        ("Programme stays\ninformal", "No mandate, no budget,\nno quarterly reporting"),
        ("Scorecard objectives\nmissed", "14 of 18 objectives lose\ntheir execution engine"),
        ("Cross-OU demand\nunmet", "Banking & Life build\ntheir own tools (duplication)"),
        ("AI adoption stalls", "90% target unachievable\nwithout structured enablement"),
    ]
    for i, (title, desc) in enumerate(losses):
        y = 6.2 - i * 1.25
        box = FancyBboxPatch((0.3, y - 0.4), 4.9, 0.9,
                             boxstyle="round,pad=0.1", fc=(*mRED, 0.08),
                             ec=mRED, linewidth=1.5)
        ax.add_patch(box)
        ax.text(0.5, y + 0.1, title, fontsize=8, fontweight="bold",
                color=mRED, va="center")
        ax.text(0.5, y - 0.2, desc, fontsize=6.5, color=mDARK, va="center")

    # Right column: competitor gains
    gains = [
        ("AIG + Anthropic + Palantir", "Strategic AI partnership for\nunderwriting automation"),
        ("Zurich: $40M saved", "AI-driven claims processing\nand risk assessment"),
        ("Allianz: 135 days saved", "Document processing\nautomation at scale"),
        ("Markel: 113% productivity", "AI coding assistants across\nentire engineering team"),
        ("Industry: 87% YoY growth", "AI deployment accelerating\nfaster than ever"),
    ]
    for i, (title, desc) in enumerate(gains):
        y = 6.2 - i * 1.25
        box = FancyBboxPatch((5.8, y - 0.4), 4.9, 0.9,
                             boxstyle="round,pad=0.1", fc=(*mNAVY, 0.06),
                             ec=mNAVY, linewidth=1.5)
        ax.add_patch(box)
        ax.text(6.0, y + 0.1, title, fontsize=8, fontweight="bold",
                color=mNAVY, va="center")
        ax.text(6.0, y - 0.2, desc, fontsize=6.5, color=mDARK, va="center")

    # Bottom callout
    callout = FancyBboxPatch((1.5, 0.2), 8.0, 0.6,
                              boxstyle="round,pad=0.1", fc=(*mRED, 0.1),
                              ec=mRED, linewidth=2)
    ax.add_patch(callout)
    ax.text(5.5, 0.5, "The cost of inaction is not zero -- it is the gap between you and every competitor investing in AI.",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color=mRED)

    fig.tight_layout()
    return _save_fig(fig, tmpdir, "cost_inaction.png")


# ── PDF Class ───────────────────────────────────────────────────────

class ScorecardPDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.set_auto_page_break(True, margin=20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, "F")
        self.set_fill_color(*BLUE)
        self.rect(0, 12, 210, 1, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6,
                  "CS Gen AI Programme  |  2026 Strategic Programme Review  |  Scorecard Alignment",
                  0, 0, "L")
        self.set_text_color(*DARK)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MGRAY)
        self.cell(0, 10,
                  f"Strategic Programme Review  |  {DOC_DATE}  |  Page {self.page_no()}",
                  0, 0, "R")

    # ── helpers ──
    def section_title(self, title):
        if self.get_y() > 250:
            self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*NAVY)
        self.cell(0, 10, title, 0, 1)
        self.set_fill_color(*BLUE)
        self.rect(10, self.get_y(), 40, 0.8, "F")
        self.ln(4)

    def sub_title(self, title):
        if self.get_y() > 260:
            self.add_page()
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.cell(0, 8, title, 0, 1)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bold_body(self, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*DARK)
        self.cell(6, 5, "-", 0, 0)
        if bold_prefix:
            self.set_font("Helvetica", "B", 10)
            self.cell(self.get_string_width(bold_prefix) + 1, 5, bold_prefix, 0, 0)
            self.set_font("Helvetica", "", 10)
            self.multi_cell(0, 5, text)
        else:
            self.multi_cell(0, 5, text)
        self.ln(1)

    def callout_box(self, text, bg_color, text_color):
        if self.get_y() + 15 > 270:
            self.add_page()
        self.set_fill_color(*bg_color)
        y0 = self.get_y()
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*text_color)
        lines = self.multi_cell(180, 5.5, text, split_only=True)
        h = len(lines) * 5.5 + 6
        self.rect(10, y0, 190, h, "F")
        self.set_xy(15, y0 + 3)
        self.multi_cell(180, 5.5, text)
        self.ln(4)

    def numbered_item(self, num, title, desc):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BLUE)
        self.cell(8, 5, str(num) + ".", 0, 0)
        self.set_text_color(*NAVY)
        self.cell(0, 5, title, 0, 1)
        if desc:
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*MGRAY)
            self.set_x(self.get_x() + 8)
            self.multi_cell(0, 4.5, desc)
        self.ln(2)

    def add_table(self, headers, rows, col_widths=None):
        w = col_widths or [190 / len(headers)] * len(headers)
        if self.get_y() + 20 > 270:
            self.add_page()
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 8)
        for i, h in enumerate(headers):
            self.cell(w[i], 7, h, 1, 0, "L", True)
        self.ln()
        self.set_text_color(*DARK)
        for ri, row in enumerate(rows):
            bg = ri % 2 == 0
            if bg:
                self.set_fill_color(*LGRAY)
            max_lines = 1
            cell_texts = []
            for ci, cell in enumerate(row):
                lines = self.multi_cell(w[ci], 5, cell, split_only=True)
                cell_texts.append(lines)
                max_lines = max(max_lines, len(lines))
            rh = max_lines * 5 + 2
            if self.get_y() + rh > 270:
                self.add_page()
                self.set_fill_color(*NAVY)
                self.set_text_color(*WHITE)
                self.set_font("Helvetica", "B", 8)
                for i, h in enumerate(headers):
                    self.cell(w[i], 7, h, 1, 0, "L", True)
                self.ln()
                self.set_text_color(*DARK)
                if bg:
                    self.set_fill_color(*LGRAY)
            y_start = self.get_y()
            x_start = self.get_x()
            for ci, lines in enumerate(cell_texts):
                x = x_start + sum(w[:ci])
                self.set_xy(x, y_start)
                self.set_font("Helvetica", "", 8)
                if bg:
                    self.set_fill_color(*LGRAY)
                    self.rect(x, y_start, w[ci], rh, "F")
                self.rect(x, y_start, w[ci], rh)
                self.set_xy(x + 1, y_start + 1)
                for line in lines:
                    self.cell(w[ci] - 2, 5, line, 0, 2)
            self.set_y(y_start + rh)
        self.ln(3)

    def add_image_full_width(self, path, w=190):
        if self.get_y() + 80 > 270:
            self.add_page()
        x = (210 - w) / 2
        self.image(path, x=x, y=self.get_y(), w=w)
        from PIL import Image
        img = Image.open(path)
        iw, ih = img.size
        h = w * ih / iw
        self.set_y(self.get_y() + h + 5)

    def stat_box(self, number, label, color):
        """Compact stat callout."""
        if self.get_y() + 20 > 270:
            self.add_page()
        y0 = self.get_y()
        self.set_fill_color(*color)
        self.rect(10, y0, 190, 14, "F")
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*WHITE)
        self.set_xy(15, y0 + 1)
        self.cell(40, 12, number, 0, 0)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 12, label, 0, 0)
        self.set_y(y0 + 16)


# ── Build PDF ───────────────────────────────────────────────────────

def build_pdf(output_path):
    tmpdir = tempfile.mkdtemp()

    # Generate all charts
    heatmap_img = gen_heatmap(tmpdir)
    quadrant_img = gen_quadrant(tmpdir)
    coverage_img = gen_coverage_wheel(tmpdir)
    flow_img = gen_flow_diagram(tmpdir)
    gaps_img = gen_gaps_chart(tmpdir)
    three_horizon_img = gen_three_horizon(tmpdir)
    quarterly_img = gen_quarterly_roadmap(tmpdir)
    value_tree_img = gen_value_driver_tree(tmpdir)
    resource_img = gen_resource_chart(tmpdir)
    inaction_img = gen_cost_of_inaction(tmpdir)

    pdf = ScorecardPDF()

    # ═══════════════════════════════════════════════════════════════
    # PAGE 1: TITLE PAGE
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 180, 210, 2, "F")

    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 40)
    pdf.multi_cell(170, 16, "CS Gen AI Programme\nStrategic Programme\nReview")

    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(180, 200, 255)
    pdf.set_xy(20, 100)
    pdf.cell(0, 8, "2026 Scorecard Alignment  |  Investment Case")

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(140, 160, 210)
    pdf.set_xy(20, 115)
    pdf.cell(0, 7, "9 projects. 14 of 18 scorecard objectives. $896M ARR protected.")

    # Key stats strip
    pdf.set_font("Helvetica", "B", 42)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 140)
    pdf.cell(0, 20, "78%")
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(180, 200, 255)
    pdf.set_xy(20, 158)
    pdf.cell(0, 8, "of Insurance scorecard objectives served by this programme")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(156, 163, 175)
    pdf.set_xy(20, 195)
    pdf.multi_cell(0, 7,
        f"{DOC_DATE}\n"
        "Customer Success Gen AI Programme\n"
        "Moody's Analytics - Insurance Division")

    # ═══════════════════════════════════════════════════════════════
    # PAGE 2: THE NUMBER + CORPORATE ALIGNMENT (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1. The Programme at a Glance")

    pdf.stat_box("14 / 18", "Insurance scorecard objectives directly served by this programme", NAVY)
    pdf.stat_box("9", "Active projects across six workstreams", BLUE)
    pdf.stat_box("$896M", "ARR base protected by CLARA migration tracking", GREEN)
    pdf.stat_box("~5", "Full-time contributors delivering all of this", RED)

    pdf.ln(3)
    pdf.sub_title("Moody's Corporate Alignment")
    pdf.body(
        "This programme is not a side project -- it is the Insurance division's local "
        "implementation of a company-wide strategic mandate. Moody's has publicly committed "
        "to AI-first transformation:"
    )
    pdf.bullet(
        "Moody's GenAI products now generate $200M+ ARR, growing at 2x year-over-year.",
        "$200M GenAI ARR: "
    )
    pdf.bullet(
        "50+ domain-specific AI agents deployed across the company, using MCP server architecture "
        "-- the same architecture our App Factory and Build in Five use.",
        "50+ Agentic Solutions: "
    )
    pdf.bullet(
        "97% customer retention rate on GenAI products, cited by CEO Rob Fauber in earnings calls.",
        "97% Retention: "
    )
    pdf.bullet(
        "IRP Navigator already serves 300+ clients company-wide. The Insurance scorecard targets "
        "25% adoption -- WS5 is our contribution to that corporate KPI.",
        "Navigator at Scale: "
    )
    pdf.bullet(
        "Moody's formed the Generative Intelligence Group (GiG) to coordinate AI strategy. "
        "Our programme is GiG's natural insurance-division counterpart.",
        "GiG Strategy: "
    )

    pdf.callout_box(
        "Framing: When Diya asks 'why should I invest in this?', the answer is: "
        "'Because the CEO is telling analysts our AI products are the growth engine. "
        "This programme is how Insurance delivers on that promise.'",
        (230, 240, 255), NAVY
    )

    # ═══════════════════════════════════════════════════════════════
    # PAGE 3: INDUSTRY CONTEXT (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("2. Industry Context: Why Now")

    pdf.body(
        "The insurance industry is in the early stages of an AI transformation that will "
        "separate leaders from laggards within 24 months. BCG's research shows a widening "
        "'AI Value Gap' -- companies that scale AI see 2-5x the productivity gains of those "
        "that don't."
    )

    pdf.sub_title("The Numbers")
    pdf.bullet(
        "Insurance AI deployments grew 87% year-over-year (Evident AI Insurance Index 2025). "
        "But only 7% of insurers have scaled AI beyond pilot -- most are stuck in proof-of-concept.",
        "87% Growth, 7% Scaled: "
    )
    pdf.bullet(
        "Zurich Insurance saved $40M through AI-driven claims processing and risk assessment. "
        "That is what 'scaled AI' looks like.",
        "Zurich -- $40M: "
    )
    pdf.bullet(
        "Allianz reduced document processing time by 135 days through AI automation. "
        "Their engineering team now spends time on products, not paperwork.",
        "Allianz -- 135 Days: "
    )
    pdf.bullet(
        "Markel achieved 113% productivity increase from AI coding assistants across engineering. "
        "Our Cursor/Claude adoption programme is doing the same thing.",
        "Markel -- 113% Productivity: "
    )
    pdf.bullet(
        "AIG signed strategic partnerships with both Anthropic (Claude) and Palantir for "
        "underwriting automation, using MCP architecture for agentic workflows. "
        "Our Build in Five uses the same technology.",
        "AIG -- Strategic AI: "
    )

    pdf.callout_box(
        "Positioning: The average insurer takes 6-9 months to see ROI from AI investments. "
        "Your programme has been running for 10 weeks and CLARA is already in weekly use. "
        "You are ahead of the industry curve.",
        (240, 255, 240), DARK
    )

    pdf.sub_title("The Gainsight Validation")
    pdf.body(
        "Gainsight launched AI Copilot in 2025, validating the exact CS-AI integration approach "
        "your programme is building. Their copilot surfaces churn risk, recommends actions, and "
        "auto-generates customer briefs -- capabilities that map directly to CLARA's roadmap. "
        "The Gainsight Q2 transition is not just a scorecard objective; it is the moment your "
        "AI capabilities and Gainsight's platform converge."
    )

    # ═══════════════════════════════════════════════════════════════
    # PAGE 4: THREE-HORIZON ROADMAP (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("3. Three-Horizon Strategic Roadmap")

    pdf.body(
        "The programme follows a three-horizon model. Horizon 1 projects are already "
        "delivering value. Horizon 2 projects scale the platform through Q2-Q3 scorecard "
        "deadlines. Horizon 3 projects are strategic bets that position Insurance for 2027."
    )

    pdf.add_image_full_width(three_horizon_img)

    pdf.body(
        "Critical insight: Horizon 1 success funds Horizon 2 credibility. The reason to invest "
        "now is that CLARA, Build in Five, and Training have already proven the model works. "
        "The Q2-Q3 scorecard deadlines are the forcing function."
    )

    # ═══════════════════════════════════════════════════════════════
    # PAGE 5: QUARTERLY ROADMAP (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("4. Quarterly Delivery vs Scorecard Gates")

    pdf.body(
        "This timeline maps every programme project against the specific scorecard deadlines "
        "they serve. Vertical lines show scorecard gates. The message: every quarter has "
        "a delivery milestone that maps directly to a scorecard KPI."
    )

    pdf.add_image_full_width(quarterly_img)

    pdf.sub_title("Key Scorecard Deadlines")
    pdf.bullet(
        "Build in Five sales enablement tool ready for customer demos.",
        "Q1 -- Sales Enablement: "
    )
    pdf.bullet(
        "CS organisation transitions to Gainsight. CLARA integration must be live. "
        "AS Quick Start package and CatMoSAI both due.",
        "Q2 -- Gainsight + AS Tools: "
    )
    pdf.bullet(
        "75% of Analytical Services accounts modelled by agentic AI. "
        "This is the single hardest target and needs App Factory + dedicated effort.",
        "Q3 -- 75% AS Agentic (Critical): "
    )
    pdf.bullet(
        "NatCat modelling entirely on agentic AI. Full programme maturity.",
        "Q4 -- NatCat Full Agentic: "
    )

    # ═══════════════════════════════════════════════════════════════
    # PAGE 6: CORRELATION HEATMAP
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("5. Programme-Scorecard Correlation")

    pdf.body(
        "The heatmap below shows how each programme project maps to the eight scorecard pillars. "
        "'Direct Hit' means the project is explicitly named or directly measured by that scorecard target. "
        "'Strong' means a clear causal link. 'Indirect' means a supporting or enabling relationship."
    )

    pdf.add_image_full_width(heatmap_img)

    pdf.body(
        "Key observations: CLARA has the broadest coverage (5 pillars). "
        "Navigator L1 Automation and Training & Enablement have the highest concentration of Direct Hits. "
        "Risk & Security is the only pillar with minimal coverage -- addressed in new project proposals (Section 12)."
    )

    # ═══════════════════════════════════════════════════════════════
    # PAGE 7: VALUE DRIVER TREE (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("6. Value Driver Tree")

    pdf.body(
        "Every programme activity connects to a financial outcome through a measurable chain. "
        "This tree traces the path from what the team does daily to the numbers on the scorecard."
    )

    pdf.add_image_full_width(value_tree_img)

    pdf.body(
        "Total addressable value: $896M ARR protected through migration tracking, plus ~$1.2M "
        "in direct efficiency gains ($150K AS saving, ~$200K support cost reduction, ~$850K "
        "contractor spend reduction through AI tool adoption). Conservative estimates -- "
        "the real number is higher once sales enablement conversion is factored in."
    )

    # ═══════════════════════════════════════════════════════════════
    # PAGE 8: FLOW DIAGRAM
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("7. How Projects Deliver Scorecard Outcomes")

    pdf.body(
        "This diagram traces the causal chain from programme projects (left) through specific "
        "scorecard targets (centre) to business outcomes (right). Every arrow represents a "
        "documented, evidence-based connection."
    )

    pdf.add_image_full_width(flow_img)

    # ═══════════════════════════════════════════════════════════════
    # PAGES 9-12: DETAILED PROJECT MAPPINGS
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("8. Detailed Project Mappings")

    # -- CLARA --
    pdf.sub_title("8.1 CLARA (IRP Adoption Tracker)")
    pdf.body(
        "CLARA is the programme's flagship: a live web application that tracks IRP migration progress "
        "across the insurance portfolio. Used in weekly Portfolio Reviews led by Natalia. "
        "31 scorecard migration accounts loaded. CSMs log blockers, status, and action plans in real-time."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["32 RiskLink/RiskBrowser migrations (41% of 78 in-flight)", "CLARA tracks every one. Portfolio Reviews are the execution mechanism.", "DIRECT HIT"],
            ["Fully implement tiered customer success", "CLARA enables per-account health views, blocker tracking, and structured Portfolio Reviews.", "STRONG"],
            ["Effectively drive core product retention / reduce churn", "Surfaces renewal risks through blocker data and migration status.", "STRONG"],
            ["Gainsight Q2 transition for CS organisation", "Integration architecture designed (12 Mar meeting). Bi-directional POC planned.", "STRONG"],
            ["Maintain Strategic Accounts NPS >= FY25", "Improves account management quality, which feeds NPS.", "MODERATE"],
            ["Exit ARR of $896M / 8.4% growth", "Supports $69M net ARR increase by protecting migration accounts. ~75% of BU revenue is IRP-related.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # -- Build in Five --
    pdf.sub_title("8.2 Build in Five (WS6 - Dashboard Builder)")
    pdf.body(
        "Martin Davies' dashboard builder: a white-labelling platform with live Risk Modeller API integration, "
        "AI-assisted component generation, full theming, and save/load configurations. "
        "Compared by programme leadership to Databricks Genie. "
        "Stakeholder cascade defined: MCP server -> tech consulting -> demo team -> sales -> exceedance."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["Enhanced sales enablement (Q1 target)", "IS the enhanced sales enablement tool. Customer sees their data on IRP in 5 minutes.", "DIRECT HIT"],
            ["Achieve product-unit sales targets (36+ RM, 7+ RDL, 20+ RDE)", "Makes IRP tangible for customers. Visualise data in meeting -> higher conversion.", "STRONG"],
            ["Invest in scalable venture initiatives: Agentic workflows", "MCP integration IS an agentic workflow. Live API queries, AI-assisted generation.", "STRONG"],
            ["Focus on P&C Insurance Risk & Underwriting", "Demonstrates IRP platform to the exact prioritised market segment.", "STRONG"],
            ["Develop partner channel (Guidewire, Duck Creek)", "White-label template approach could become partner integration demo framework.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # -- Training & Enablement --
    pdf.sub_title("8.3 Training & Enablement (WS1)")
    pdf.body(
        "Conceptual framework exists (solution-focused training buckets, competency assessment, "
        "train-the-trainer). No formal deliverables yet. Two grads arriving April 7 could provide capacity. "
        "Cross-OU sessions with Banking and Life already delivered."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["90% of employees actively using CoPilot/Cursor (weekly)", "Only operational example of Cursor/Claude adoption in Insurance CS. Every person trained is a data point.", "DIRECT HIT"],
            ["100% employees up-to-date on AI curriculum", "Training framework IS the CS function's AI curriculum.", "STRONG"],
            ["Deliver min. 2 events to drive AI adoption across team", "Cross-OU sessions with Banking and Life already happened. AS wants 2+ education sessions.", "STRONG"],
            ["Learning Labs -- 80% of staff managers completing sessions", "Hands-on Cursor sessions IS the Learning Lab model for AI.", "MODERATE"],
            ["Minimise contractor spending through greater use of GenAI", "Every person trained on AI tools reduces the need for contractor augmentation.", "STRONG"],
        ],
        [65, 95, 30]
    )

    # -- Navigator L1 --
    pdf.sub_title("8.4 Navigator L1 Automation (WS5)")
    pdf.body(
        "Concept: use Navigator's upcoming API support to auto-answer L1 support tickets. "
        "Product team building the MCP server. CS needs to champion adoption and measure impact. "
        "Currently early stage with no CS-side build."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["25% of IRP product users using AI Navigators", "WS5 IS this. The scorecard literally names IRP Navigators.", "DIRECT HIT"],
            ["Measurable reduction in repeat/routine support cases", "AI-powered L1 automation = fewer tickets. The scorecard wants measurable data.", "DIRECT HIT"],
            ["Identify and prioritise self-service opportunities (Q2)", "Navigator work requires exactly this analysis -- what are common L1 questions?", "STRONG"],
            ["Validate Navigator effectiveness (90% accuracy target)", "CS feedback loop is needed. CE is best positioned to provide it.", "STRONG"],
        ],
        [65, 95, 30]
    )

    # -- App Factory --
    pdf.sub_title("8.5 App Factory (Infrastructure Platform)")
    pdf.body(
        "BenVH's deployment platform, now pivoted to an MCP server architecture. "
        "Any application (Build in Five, CLARA, Slidey, future tools) can consume it. "
        "Banking and Life both identified the deployment gap -- App Factory fills it."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["All new products built leveraging MAP & GenAI shared components", "App Factory's MCP server IS a GenAI shared component.", "STRONG"],
            ["75% of AS accounts modeled by agentic AI (Q3)", "App Factory provides the deployment platform for agentic workflows.", "STRONG"],
            ["NatCat modelling entirely on agentic AI (Q4) / $150K saving", "App Factory MCP architecture is the enabling infrastructure.", "STRONG"],
            ["Minimise contractor spending through GenAI", "Every tool built in App Factory replaces something a contractor would maintain.", "STRONG"],
            ["Proactively manage cloud cost efficiency", "Consolidates deployment infrastructure -- one platform vs N individual deployments.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # -- Cross-OU --
    pdf.sub_title("8.6 Cross-OU Collaboration")
    pdf.body(
        "Banking (Gina Greer, Olivier) and Life (Jack Cheyne, Christian Curran) engagement sessions. "
        "Idrees Deen as cross-OU coalition builder. Template/flat-pack approach for scaling CLARA. "
        "Concrete interest from multiple divisions."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["Build insurance-specific strategies for KYC, Asset Risk, Data Mgmt", "Cross-OU engagement directly supports multi-segment strategy.", "STRONG"],
            ["X-BU CE Engagement Model for KYC/Compliance, Asset & Credit Risk", "Cross-OU sessions ARE building this engagement model. You're ahead of the scorecard.", "STRONG"],
            ["Deliver min. 2 events to drive AI adoption", "Cross-OU sessions with Banking and Life are adoption events.", "STRONG"],
            ["RMS SFDC retirement and transition to MA SFDC (Q3)", "CLARA's Salesforce integration design supports this.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # -- Friday --
    pdf.sub_title("8.7 Friday (PM App)")
    pdf.body(
        "Internal project management application built by Azmain using Claude Code. Replaces "
        "slide-based Wednesday advisory project reviews. Syncs bidirectionally with CLARA for IRP projects. "
        "Endorsed by Diana, who plans to present to Ben/Charlotte for formal approval."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["Fully implement tiered customer success", "Replaces ad-hoc PM processes with structured tracking. Enables tiered approach to project oversight.", "STRONG"],
            ["90% of employees actively using CoPilot/Cursor (weekly)", "Built entirely by AI agents -- demonstrates the art of the possible.", "STRONG"],
            ["Minimise contractor spending through GenAI", "Replaces need for commercial PM tool with in-house AI-built alternative.", "MODERATE"],
            ["Mature product cost efficiency", "Reduces overhead on advisory project tracking, freeing CS time.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # -- CS Agent --
    pdf.sub_title("8.8 Customer Success Agent (WS3)")
    pdf.body(
        "Kevin Pern's Copilot Studio + Salesforce prototype. Banking already built a similar agent "
        "connecting to AR data for spend and fund scoring. Bernard (Life) built a separate Copilot health dashboard. "
        "Currently minimal progress with no programme oversight, but the pieces exist."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["Fully implement tiered customer success", "AI-assisted CS interactions enable tiered support. Agent handles routine, humans focus on strategic.", "STRONG"],
            ["Invest in scalable venture initiatives: Agentic workflows", "A CS Agent IS an agentic workflow by definition. Copilot Studio is the framework.", "STRONG"],
            ["90% of employees actively using CoPilot/Cursor (weekly)", "Copilot Studio usage directly drives this KPI.", "STRONG"],
            ["Measurable reduction in repeat/routine support cases", "Agent handles L1/routine inquiries, reducing human caseload.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # -- TSR Enhancements --
    pdf.sub_title("8.9 TSR Enhancements (Cat Bond Automation)")
    pdf.body(
        "Idris Abram's project to automate Transaction Summary Reports for cat bonds. First expansion "
        "beyond the core insurance CS team. Ben Brookes approved dedicated time. Azmain supporting with "
        "project planning. Treated as a proper scoped project, not a side experiment."
    )
    pdf.add_table(
        ["Scorecard Objective", "Connection", "Strength"],
        [
            ["Minimise contractor spending through greater use of GenAI", "Automates manual TSR generation -- replaces time-intensive human process with AI.", "DIRECT HIT"],
            ["Mature product cost efficiency", "Reduces operational cost of producing cat bond reports.", "STRONG"],
            ["90% of employees actively using CoPilot/Cursor (weekly)", "Idris using Cursor for development. Extends AI tooling into risk advisory team.", "STRONG"],
            ["Effective data and risk management (tech debt reduction)", "Structured automation reduces error-prone manual reporting.", "MODERATE"],
        ],
        [65, 95, 30]
    )

    # ═══════════════════════════════════════════════════════════════
    # QUICK WINS QUADRANT
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("9. Quick Wins: Where to Accelerate")

    pdf.body(
        "The quadrant below plots each initiative by the effort required to deliver it "
        "against its scorecard impact. Items in the top-left ('Quick Wins') should be "
        "prioritised for immediate attention."
    )

    pdf.add_image_full_width(quadrant_img)

    pdf.sub_title("Top 5 Rapid Wins")
    wins = [
        ("Navigator L1 Automation",
         "Scorecard target: 25% of IRP users on AI Navigators. "
         "CS just needs to champion adoption and measure support case reduction. "
         "Low build effort, high visibility KPI."),
        ("Training & Enablement",
         "Scorecard target: 90% weekly AI tool usage. Two grads arriving April 7. "
         "Cross-OU sessions already delivered. Systematise into formal programme."),
        ("Build in Five for Sales",
         "Scorecard target: enhanced sales enablement (Q1). Martin's demo is ready. "
         "MCP server integration in next 2 weeks completes the demo loop."),
        ("Analytical Services Agentic Workflows",
         "Scorecard target: 75% agentic AI by Q3, $150K saving. "
         "App Factory MCP architecture is ready. Connect with AS team."),
        ("Gainsight Transition",
         "Scorecard target: CS on Gainsight by Q2. Architecture alignment happening. "
         "CLARA integration in design phase."),
    ]
    for i, (title, desc) in enumerate(wins):
        pdf.numbered_item(i + 1, title, desc)

    # ═══════════════════════════════════════════════════════════════
    # NEW AI PROJECT PROPOSALS (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("10. New AI Project Proposals")

    pdf.body(
        "Seven additional AI projects that would fill scorecard gaps and strengthen the programme's "
        "coverage. Each maps to specific unmapped or under-served scorecard objectives. "
        "Ordered by feasibility (quick wins first)."
    )

    new_projects = [
        ("Migration Intelligence Agent",
         "Predicts at-risk IRP migrations using CLARA's historical data -- blocker patterns, "
         "time-to-resolve, CSM engagement levels. Surfaces early warnings before migrations stall.",
         "32 IRP migrations, core product retention, Strategic Accounts NPS",
         "Low (uses existing CLARA data)", "HIGH",
         "Zurich saved $40M by predicting claims outcomes. Same principle, different domain."),

        ("Renewal Risk Predictor",
         "Combines CLARA migration data with Gainsight health scores to predict renewal risk "
         "at account level. Auto-generates renewal briefs for CSMs.",
         "$896M ARR retention, tiered CS, churn reduction",
         "Medium (needs Gainsight integration)", "HIGH",
         "BCG estimates AI-driven churn prediction delivers 3-8% retention improvement."),

        ("AS Workflow Accelerator",
         "Purpose-built agentic workflows for Analytical Services: automated model runs, "
         "report generation, client delivery packages. Deployed via App Factory MCP.",
         "75% AS agentic by Q3, $150K saving, 20 staff redeployment, NatCat Q4",
         "Medium (App Factory ready, needs AS collaboration)", "CRITICAL",
         "Directly addresses the hardest scorecard target. Start Q2 to hit Q3 deadline."),

        ("Navigator Feedback Loop",
         "Automated accuracy measurement for AI Navigator responses. Captures user corrections, "
         "measures satisfaction, feeds into product improvement cycle.",
         "25% Navigator adoption, 90% accuracy target, self-service opportunities",
         "Low (lightweight tracking layer)", "MEDIUM",
         "The scorecard asks for measurable impact. This provides the measurement."),

        ("KYC/Compliance Prototype",
         "Insurance-specific agentic solution for KYC and AML compliance checks. "
         "Leverages Moody's existing KYC data assets with AI-driven analysis.",
         "KYC/AML agentic solutions (scorecard), X-BU CE engagement model",
         "High (new domain, regulatory complexity)", "MEDIUM",
         "Scorecard explicitly names this. Cross-OU collaboration provides the route in."),

        ("Risk Dashboard Builder",
         "Automated risk dashboards for Tier 1 and Tier 2 products using Build in Five "
         "templates. Risk managers see live data without manual report assembly.",
         "Risk dashboards for Tier 1&2, Risk & Security pillar",
         "Medium (Build in Five templates exist)", "MEDIUM",
         "Fills the programme's biggest gap: Risk & Security pillar (currently 15% coverage)."),

        ("CatMoSAI / AS Sales Enablement",
         "Integrates CatMoSAI outputs with Build in Five for Analytical Services sales demos. "
         "Prospects see live NatCat model results in branded dashboards.",
         "CatMoSAI Q2, AS Quick Start Q2, sales enablement",
         "Low (both tools exist, need integration)", "HIGH",
         "Two scorecard targets (CatMoSAI + AS Quick Start) share a Q2 deadline."),
    ]

    for name, desc, sc_targets, effort, priority, rationale in new_projects:
        if pdf.get_y() > 200:
            pdf.add_page()
        pdf.sub_title(name)
        pdf.body(desc)
        pdf.add_table(
            ["Dimension", "Detail"],
            [
                ["Scorecard targets served", sc_targets],
                ["Effort required", effort],
                ["Priority", priority],
                ["Industry rationale", rationale],
            ],
            [45, 145]
        )

    # ═══════════════════════════════════════════════════════════════
    # COVERAGE RADAR + GAPS
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("11. Scorecard Coverage Assessment")

    pdf.body(
        "The radar chart shows the programme's combined coverage of each scorecard pillar "
        "as a percentage. High coverage (>75%) means your projects directly address most "
        "objectives in that pillar."
    )

    pdf.add_image_full_width(coverage_img, w=140)

    pdf.sub_title("Coverage breakdown (9 projects)")
    pdf.bullet("IRP Migrations (95%): ", "CLARA is the primary execution tool. Near-complete coverage.")
    pdf.bullet("AI Adoption (90%): ", "Training, Navigator, App Factory, CS Agent, and TSR all contribute.")
    pdf.bullet("Customer Success (85%): ", "CLARA, Friday, CS Agent, and Navigator all contribute to tiered CS model.")
    pdf.bullet("People & Culture (75%): ", "Training framework and cross-OU sessions. Gap: no formal curriculum yet.")
    pdf.bullet("Agentic Workflows (75%): ", "App Factory, Build in Five, and CS Agent. Gap: need to connect AS team.")
    pdf.bullet("Efficiency (70%): ", "App Factory, TSR automation, Friday, and Gainsight. Gap: no cost attribution metrics yet.")
    pdf.bullet("GNB Growth (65%): ", "Build in Five and CLARA support sales. Gap: not directly driving deal closure.")
    pdf.bullet("Risk & Security (15%): ", "Programme's biggest gap. Risk Dashboard Builder (Section 10) would address this.")

    # ═══════════════════════════════════════════════════════════════
    # GAPS & VULNERABILITIES
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("12. Gaps & Vulnerabilities")

    pdf.body(
        "Honest assessment of where the programme is exposed. "
        "These should be addressed before presenting to Diya."
    )

    pdf.add_image_full_width(gaps_img)

    gaps_detail = [
        ("WS1 Training -- no deliverables yet (85%)",
         "The scorecard asks for 90% AI tool adoption. You have a framework and ad-hoc sessions. "
         "No structured curriculum, no measurement, no rollout plan.",
         "Reframe cross-OU sessions and Idris onboarding as pilot executions. "
         "Position grads (arriving April 7) as enablement capacity."),
        ("WS5 Navigator -- no CS ownership (75%)",
         "Scorecard puts this as joint Product + CE. CS has done nothing. "
         "Nobody is tracking support case categories or Navigator adoption.",
         "Claim the coordination role. Offer to drive adoption measurement "
         "and feedback. Low-cost, high-visibility."),
        ("WS3 CS Agent -- unconnected prototype (70%)",
         "Kevin built a Copilot Studio prototype but it has no programme oversight. "
         "Banking and Life have separate builds.",
         "Formal check-in with Kevin. Reframe the disconnected prototypes as cross-OU proof points."),
        ("Cost management -- zero attribution (70%)",
         "$10K/month Bedrock trajectory with no per-project or per-user tracking. "
         "The scorecard has cloud efficiency KPIs.",
         "Get BenVH to configure Bedrock tags. Frame cost against value: "
         "$10K/month vs $150K AS saving vs $896M migration ARR."),
        ("Kathryn Palkovics COE overlap (65%)",
         "Kathryn Palkovics' centre of excellence mandate overlaps with the AI programme. "
         "The scorecard's AI adoption targets could be claimed by her COE instead.",
         "Present to Diya before Kathryn Palkovics does. Anchor the scorecard mapping. "
         "Make it clear your programme IS the execution engine."),
        ("Cross-OU demand unfunded (60%)",
         "Banking and Life both want what you've built. No resourcing or formal structure.",
         "Frame this AS the argument for a dedicated team: "
         "'You asked us to engage them. Both need help. We need resources.'"),
    ]

    for title, desc, mitigation in gaps_detail:
        if pdf.get_y() > 230:
            pdf.add_page()
        pdf.bold_body(title)
        pdf.body(desc)
        pdf.callout_box("Mitigation: " + mitigation, (240, 248, 255), NAVY)

    # ═══════════════════════════════════════════════════════════════
    # RESOURCE MODEL (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("13. Resource Model")

    pdf.body(
        "The programme currently operates with ~7 contributors (5 core + 2 part-time), "
        "delivering against 14 scorecard objectives. This section models three states: "
        "current, minimum viable for 2026 delivery, and target for sustainable operations."
    )

    pdf.add_image_full_width(resource_img)

    pdf.sub_title("Current State (7 people)")
    pdf.add_table(
        ["Role", "Person", "Allocation", "Risk"],
        [
            ["Programme Lead / Architect", "Richard Dosoo", "~80%", "Stable"],
            ["Developer / Builder", "Azmain Hossain", "~100%", "HIGH: stretched thin, single point of failure"],
            ["Developer / Builder", "Martin Davies", "~100%", "MEDIUM: 12-week assignment ending"],
            ["Infrastructure / DevOps", "BenVH", "~60%", "HIGH: only deployer, burnout risk"],
            ["PM / Analyst", "You", "~80%", "Stable"],
            ["Part-time: Cat Bond", "Idris Abram", "~20%", "LOW"],
            ["Part-time: CS Agent", "Kevin Pern", "~10%", "MEDIUM: no oversight"],
        ],
        [55, 45, 30, 60]
    )

    pdf.sub_title("Minimum Viable (10 people) -- The Ask")
    pdf.add_table(
        ["Addition", "Why", "Cost", "Impact"],
        [
            ["+1 Developer (grad, Apr 7)", "Absorb Martin's work when assignment ends. Build Navigator feedback loop.", "Grad salary (already arriving)", "Covers Horizon 1 continuity"],
            ["+1 Enablement Lead (grad, Apr 7)", "Own Training & Enablement programme. Drive 90% AI adoption KPI.", "Grad salary (already arriving)", "Direct scorecard KPI ownership"],
            ["+1 Senior Developer", "Reduce Azmain single-point-of-failure risk. Build AS Agentic workflows.", "~GBP 70-85K", "Unlocks Q3 AS target"],
        ],
        [50, 55, 45, 40]
    )

    pdf.body(
        "The two grads arriving April 7 provide immediate capacity at minimal cost. "
        "The single additional developer is the critical ask -- without this hire, "
        "the Q3 75% AS agentic target is unachievable and Azmain remains a single point of failure."
    )

    # ═══════════════════════════════════════════════════════════════
    # COST OF INACTION (NEW)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("14. Cost of Inaction")

    pdf.body(
        "The cost of not investing in this programme is not zero. It is the widening gap "
        "between Moody's Insurance and every competitor scaling AI."
    )

    pdf.add_image_full_width(inaction_img)

    pdf.sub_title("Quantified Downside Risk")
    pdf.add_table(
        ["If this happens...", "The cost is...", "Probability"],
        [
            ["CLARA stops being maintained", "$896M ARR base loses its tracking mechanism. Portfolio Reviews revert to 300-slide Excel decks.", "MEDIUM without dedicated team"],
            ["Training programme doesn't launch", "90% AI adoption KPI missed. Insurance falls behind Banking (already using Copilot).", "HIGH without dedicated owner"],
            ["Cross-OU demand goes unmet", "Banking and Life build duplicate tools. ~$200K in wasted effort. Political damage.", "MEDIUM -- already happening"],
            ["AS agentic target missed (Q3)", "$150K saving unrealised. 20 staff not redeployed. NatCat Q4 target cascades.", "HIGH without developer hire"],
            ["Programme loses informal status", "Kathryn Palkovics' COE absorbs the AI narrative. Your team loses credit for 10 weeks of delivery.", "MEDIUM -- COE mandate active"],
        ],
        [55, 95, 40]
    )

    # ═══════════════════════════════════════════════════════════════
    # THE ASK -- SCR FORMAT (REVISED)
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("15. The Ask")

    pdf.sub_title("Situation")
    pdf.body(
        "The CS Gen AI Programme has delivered nine projects in 10 weeks, serving 14 of "
        "the 18 Insurance scorecard objectives. CLARA is in weekly use for Portfolio Reviews. "
        "Build in Five is ready for customer demos. Banking and Life are actively requesting "
        "our tools. We are ahead of industry benchmarks -- most insurers take 6-9 months to "
        "reach the stage we reached in 10 weeks."
    )

    pdf.sub_title("Complication")
    pdf.body(
        "This programme has no formal status, no dedicated budget, and runs on ~5 full-time "
        "people. Martin's 12-week assignment ends soon. Azmain is a single point of failure "
        "building every tool. BenVH is the only person who can deploy. Cross-OU demand is growing "
        "with no resources to meet it. Kathryn Palkovics' COE mandate could absorb the AI narrative "
        "if the programme doesn't formalise first."
    )

    pdf.sub_title("Resolution: Three Things We Need")

    pdf.callout_box(
        "1. FORMAL PROGRAMME STATUS\n"
        "Recognise the CS Gen AI Programme as an official initiative with quarterly reporting "
        "to Diya. This protects the scorecard mapping, prevents COE absorption, and gives "
        "the team a mandate to continue.",
        NAVY, WHITE
    )

    pdf.callout_box(
        "2. DEDICATED HEADCOUNT (+3 minimum)\n"
        "Two grads arriving April 7 (already funded). One additional senior developer "
        "(~GBP 70-85K) to remove the Azmain single-point-of-failure and unlock the Q3 "
        "AS agentic target. Total incremental cost: one salary.",
        BLUE, WHITE
    )

    pdf.callout_box(
        "3. RING-FENCED BUDGET (~$50K)\n"
        "Cloud infrastructure (Bedrock: ~$10K/month, with cost tags for attribution). "
        "Tools and licences (Cursor, Railway, monitoring). This is less than the cost "
        "of one contractor month -- and it replaces dozens.",
        GREEN, WHITE
    )

    pdf.ln(3)
    pdf.sub_title("Pitch Architecture (6 steps)")
    steps = [
        ("Open with the number",
         "\"Nine projects, 14 of 18 scorecard objectives. This programme is the execution engine for the Insurance scorecard.\""),
        ("Anchor to corporate strategy",
         "\"Moody's is generating $200M ARR from GenAI. The CEO calls it our growth engine. This programme is how Insurance delivers on that.\""),
        ("Lead with what's already working",
         "\"CLARA tracks 31 migration accounts. Build in Five is ready for customer demos. Cross-OU sessions delivered to Banking and Life.\""),
        ("Show the financial chain",
         "\"$896M ARR protected. $150K AS saving on track. $200K+ support cost reduction. All from a team of five.\""),
        ("Name the competitor threat",
         "\"AIG has signed strategic deals with Anthropic and Palantir. Zurich saved $40M with AI. We are doing this with five people and no budget.\""),
        ("Close with the specific ask",
         "\"We need three things: formal status (free), three headcount (two already arriving), and $50K budget (less than one contractor). \""),
    ]
    for i, (title, desc) in enumerate(steps):
        pdf.numbered_item(i + 1, title, desc)

    # ═══════════════════════════════════════════════════════════════
    # BACK PAGE
    # ═══════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 80)
    pdf.multi_cell(170, 12, "CS Gen AI Programme\nStrategic Programme Review")

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(180, 200, 255)
    pdf.set_xy(20, 115)
    pdf.cell(0, 8, f"{DOC_DATE}  |  Investment Case")

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 140)
    pdf.multi_cell(170, 10,
        "9 projects.\n"
        "14 of 18 scorecard objectives.\n"
        "$896M ARR protected.\n"
        "5 people.\n"
        "No budget.\n"
        "No formal status.\n"
        "\n"
        "Yet."
    )

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(140, 160, 210)
    pdf.set_xy(20, 240)
    pdf.multi_cell(0, 7,
        "\"The cost of inaction is not zero --\n"
        "it is the gap between you and every\n"
        "competitor investing in AI.\"")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 110, 160)
    pdf.set_xy(20, 270)
    pdf.cell(0, 5, "Customer Success Gen AI Programme  |  Moody's Analytics  |  Insurance Division")

    pdf.output(output_path)
    print(f"PDF created: {output_path}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "generated content/Scorecard_Alignment_Briefing.pdf"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    build_pdf(out)
