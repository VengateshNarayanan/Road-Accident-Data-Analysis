
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
import textwrap

from config import (
    NAME_COLUMN,
    METRICS,
    ACCIDENT_CATEGORIES,
)
from calculations import get_category_totals, get_heatmap_matrix


def wrap_labels(labels, width=20):
    """Wrap long location/category labels to prevent overlap."""
    return [
        "\n".join(textwrap.wrap(str(label), width=width))
        for label in labels
    ]


def create_figure(df, metric_name, top_n=10, state_mode=False):
    # A larger figure gives each of the four charts more room.
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(15, 10),
        constrained_layout=True
    )

    ax1, ax2, ax3, ax4 = axes.flatten()

    if df.empty:
        for ax in axes.flatten():
            ax.text(
                0.5,
                0.5,
                "No data available",
                ha="center",
                va="center",
                fontsize=12,
                transform=ax.transAxes
            )
            ax.set_axis_off()

        fig.suptitle(
            "Accident Analysis",
            fontsize=17,
            fontweight="bold"
        )
        return fig

    # Chart 1: Location ranking or selected state's categories.
    if state_mode:
        categories = list(ACCIDENT_CATEGORIES.keys())

        values = [
            int(df[columns["cases"]].sum())
            for columns in ACCIDENT_CATEGORIES.values()
        ]

        wrapped_categories = wrap_labels(categories, width=24)

        ax1.barh(wrapped_categories, values, height=0.55)
        ax1.set_title(
            "Accident Cases by Category",
            fontsize=12,
            pad=12
        )
        ax1.set_xlabel("Number of cases", fontsize=10)
        ax1.tick_params(axis="y", labelsize=9)
        ax1.invert_yaxis()

    else:
        metric_column = METRICS[metric_name]

        ranked = (
            df.nlargest(top_n, metric_column)
            .sort_values(metric_column, ascending=True)
        )

        labels = wrap_labels(ranked[NAME_COLUMN], width=22)

        ax1.barh(labels, ranked[metric_column], height=0.65)
        ax1.set_title(
            f"Top {len(ranked)} Locations",
            fontsize=12,
            pad=12
        )
        ax1.set_xlabel(metric_name, fontsize=10)
        ax1.tick_params(axis="y", labelsize=8)
        ax1.tick_params(axis="x", labelsize=9)
        ax1.grid(axis="x", linestyle="--", alpha=0.3)
        ax1.set_axisbelow(True)

    # Chart 2: Accident cases by category.
    totals = get_category_totals(df)
    category_labels = ["Road", "Railway", "Crossing"]
    x = np.arange(len(totals))

    ax2.bar(x, totals["Cases"], width=0.6)
    ax2.set_xticks(x)
    ax2.set_xticklabels(
        category_labels,
        rotation=0,
        ha="center",
        fontsize=9
    )
    ax2.set_title("Cases by Accident Category", fontsize=12, pad=12)
    ax2.set_ylabel("Cases", fontsize=10)
    ax2.tick_params(axis="y", labelsize=9)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    ax2.set_axisbelow(True)

    # Chart 3: Injuries and deaths by category.
    width = 0.36

    ax3.bar(
        x - width / 2,
        totals["Injured"],
        width,
        label="Injured"
    )
    ax3.bar(
        x + width / 2,
        totals["Deaths"],
        width,
        label="Deaths"
    )

    ax3.set_xticks(x)
    ax3.set_xticklabels(
        category_labels,
        rotation=0,
        ha="center",
        fontsize=9
    )
    ax3.set_title("Injuries vs Deaths", fontsize=12, pad=12)
    ax3.set_ylabel("People", fontsize=10)
    ax3.tick_params(axis="y", labelsize=9)
    ax3.legend(fontsize=9, loc="best")
    ax3.grid(axis="y", linestyle="--", alpha=0.3)
    ax3.set_axisbelow(True)

    # Chart 4: Relative category heatmap.
    matrix = get_heatmap_matrix(df)

    if not matrix.empty:
        image = ax4.imshow(
            matrix.values,
            aspect="auto",
            vmin=0,
            vmax=1,
            cmap="viridis"
        )

        ax4.set_xticks(range(len(matrix.columns)))
        ax4.set_xticklabels(
            matrix.columns,
            rotation=0,
            fontsize=9
        )

        ax4.set_yticks(range(len(matrix.index)))
        ax4.set_yticklabels(
            wrap_labels(matrix.index, width=22),
            fontsize=9
        )

        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                value = matrix.iloc[row, col]

                # Use contrasting text for readability.
                text_color = "white" if value < 0.45 else "black"

                ax4.text(
                    col,
                    row,
                    f"{value:.2f}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color=text_color
                )

        ax4.set_title(
            "Relative Category Heatmap",
            fontsize=12,
            pad=12
        )

        fig.colorbar(
            image,
            ax=ax4,
            shrink=0.85,
            pad=0.04,
            label="Relative value"
        )

    else:
        ax4.text(
            0.5,
            0.5,
            "No heatmap data available",
            ha="center",
            va="center",
            transform=ax4.transAxes
        )
        ax4.set_axis_off()

    # Main title stays separate from individual chart titles.
    title = (
        f"State-wise Accident Analysis: {df.iloc[0][NAME_COLUMN]}"
        if state_mode
        else "Overall Accident Analysis"
    )

    fig.suptitle(
        title,
        fontsize=16,
        fontweight="bold"
    )

    return fig
