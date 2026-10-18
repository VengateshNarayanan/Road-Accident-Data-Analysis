
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import METRICS
from calculations import (
    filter_geography,
    get_available_states,
    get_summary_cards,
    get_state_data,
    sort_by_metric,
)
from plots import create_figure


class AccidentDashboard:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.figure = None
        self.canvas = None

        self.root.title("Road Accident Data Analysis System")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        self.mode_var = tk.StringVar(value="Overall Analysis")
        self.geography_var = tk.StringVar(value="State / UT")
        self.state_var = tk.StringVar()
        self.metric_var = tk.StringVar(value="Accident Cases")
        self.top_n_var = tk.StringVar(value="10")

        self._build_interface()
        self._update_mode()
        self.refresh_dashboard()

    def _build_interface(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(
            header,
            text="ROAD ACCIDENT DATA ANALYSIS SYSTEM",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Explore aggregate accident statistics by location",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        # Filters
        controls = ttk.LabelFrame(
            main,
            text="Analysis Filters",
            padding=12,
        )
        controls.pack(fill="x", pady=(0, 10))

        for column in range(6):
            controls.columnconfigure(column, weight=1)

        self.mode_group = self._create_filter(
            controls,
            "Analysis Mode",
            self.mode_var,
            ["Overall Analysis", "State-wise Analysis"],
            0,
            width=22,
            callback=self._on_mode_changed,
        )

        self.geo_group = self._create_filter(
            controls,
            "Compare Geography",
            self.geography_var,
            ["State / UT", "City"],
            1,
            width=16,
            callback=self._on_filter_changed,
        )

        self.state_group = self._create_filter(
            controls,
            "Select State / UT",
            self.state_var,
            get_available_states(self.data),
            2,
            width=27,
            callback=self._on_filter_changed,
        )

        self.metric_group = self._create_filter(
            controls,
            "Metric",
            self.metric_var,
            list(METRICS.keys()),
            3,
            width=25,
            callback=self._on_filter_changed,
        )

        self.top_group = self._create_filter(
            controls,
            "Top Locations",
            self.top_n_var,
            ["5", "10", "15", "20", "50"],
            4,
            width=12,
            callback=self._on_filter_changed,
        )

        ttk.Button(
            controls,
            text="Refresh Analysis",
            command=self.refresh_dashboard,
        ).grid(
            row=1,
            column=5,
            padx=(12, 4),
            pady=(5, 0),
            sticky="w",
        )

        # Summary cards
        self.summary_frame = ttk.Frame(main)
        self.summary_frame.pack(fill="x", pady=(0, 8))
        self.summary_labels = {}

        for index, title in enumerate(
            ["Accident Cases", "People Injured", "Deaths"]
        ):
            self.summary_frame.columnconfigure(index, weight=1)

            card = ttk.LabelFrame(
                self.summary_frame,
                text=title,
                padding=(12, 10),
            )
            card.grid(
                row=0,
                column=index,
                padx=(0 if index == 0 else 6, 6),
                pady=4,
                sticky="nsew",
            )

            value_label = ttk.Label(
                card,
                text="0",
                font=("Segoe UI", 19, "bold"),
            )
            value_label.pack(pady=5)
            self.summary_labels[title] = value_label

        # Status
        self.status_label = ttk.Label(
            main,
            text="",
            padding=(2, 5),
            font=("Segoe UI", 9),
        )
        self.status_label.pack(fill="x")

        # Scrollable chart area
        chart_container = ttk.Frame(main)
        chart_container.pack(fill="both", expand=True)

        self.chart_canvas = tk.Canvas(
            chart_container,
            highlightthickness=0,
            borderwidth=0,
        )

        vertical_scrollbar = ttk.Scrollbar(
            chart_container,
            orient="vertical",
            command=self.chart_canvas.yview,
        )

        self.chart_canvas.configure(
            yscrollcommand=vertical_scrollbar.set
        )

        vertical_scrollbar.pack(side="right", fill="y")
        self.chart_canvas.pack(side="left", fill="both", expand=True)

        self.chart_frame = ttk.Frame(self.chart_canvas)

        self.chart_window = self.chart_canvas.create_window(
            (0, 0),
            window=self.chart_frame,
            anchor="nw",
        )

        self.chart_frame.bind(
            "<Configure>",
            self._update_scroll_region,
        )

        self.chart_canvas.bind(
            "<Configure>",
            self._resize_chart_frame,
        )

        self.chart_canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel,
        )

    def _create_filter(
        self,
        parent,
        label_text,
        variable,
        values,
        column,
        width=18,
        callback=None,
    ):
        group = ttk.Frame(parent)
        group.grid(
            row=0,
            column=column,
            padx=5,
            sticky="nw",
        )

        ttk.Label(
            group,
            text=label_text,
        ).pack(anchor="w", pady=(0, 5))

        combo = ttk.Combobox(
            group,
            textvariable=variable,
            values=values,
            state="readonly",
            width=width,
        )
        combo.pack(anchor="w", fill="x")

        if callback is not None:
            combo.bind("<<ComboboxSelected>>", callback)

        return group

    def _update_scroll_region(self, _event=None):
        self.chart_canvas.configure(
            scrollregion=self.chart_canvas.bbox("all")
        )

    def _resize_chart_frame(self, event):
        self.chart_canvas.itemconfigure(
            self.chart_window,
            width=event.width,
        )

    def _on_mousewheel(self, event):
        if self.chart_canvas.winfo_exists():
            self.chart_canvas.yview_scroll(
                int(-event.delta / 120),
                "units",
            )

    def _update_mode(self):
        state_mode = (
            self.mode_var.get() == "State-wise Analysis"
        )

        if state_mode:
            # State-wise mode: hide geography and Top Locations
            self.geo_group.grid_remove()
            self.top_group.grid_remove()

            self.state_group.grid(
                row=0,
                column=1,
                padx=5,
                sticky="nw",
            )

            self.metric_group.grid(
                row=0,
                column=2,
                padx=5,
                sticky="nw",
            )

            # Update available states
            available_states = get_available_states(self.data)

            state_combo = self.state_group.winfo_children()[1]
            state_combo.configure(values=available_states)

            if (
                available_states
                and self.state_var.get() not in available_states
            ):
                self.state_var.set(available_states[0])

        else:
            # Overall mode: hide the state selector
            self.state_group.grid_remove()

            self.geo_group.grid(
                row=0,
                column=1,
                padx=5,
                sticky="nw",
            )

            self.metric_group.grid(
                row=0,
                column=2,
                padx=5,
                sticky="nw",
            )

            self.top_group.grid(
                row=0,
                column=3,
                padx=5,
                sticky="nw",
            )

    def _on_mode_changed(self, _event=None):
        self._update_mode()
        self.refresh_dashboard()

    def _on_filter_changed(self, _event=None):
        self.refresh_dashboard()

    def refresh_dashboard(self):
        state_mode = (
            self.mode_var.get() == "State-wise Analysis"
        )

        if state_mode:
            selected_df = get_state_data(
                self.data,
                self.state_var.get(),
            )
        else:
            selected_df = filter_geography(
                self.data,
                self.geography_var.get(),
            )

        if selected_df.empty:
            self.status_label.configure(
                text="No records found for the selected filters."
            )

            for label in self.summary_labels.values():
                label.configure(text="0")

            if self.canvas is not None:
                self.canvas.get_tk_widget().destroy()
                self.canvas = None

            if self.figure is not None:
                plt.close(self.figure)
                self.figure = None

            return

        # Update summary cards
        summary = get_summary_cards(selected_df)

        for title, value in summary.items():
            if title in self.summary_labels:
                self.summary_labels[title].configure(
                    text=f"{value:,}"
                )

        # Prepare chart data and status
        if state_mode:
            chart_data = selected_df

            self.status_label.configure(
                text=(
                    "Showing aggregate statistics for "
                    f"{self.state_var.get()}."
                )
            )
        else:
            top_n = int(self.top_n_var.get())

            chart_data = sort_by_metric(
                selected_df,
                self.metric_var.get(),
                top_n,
            )

            self.status_label.configure(
                text=(
                    f"Comparing {len(selected_df)} "
                    f"{self.geography_var.get()} records. "
                    f"Displaying up to "
                    f"{min(top_n, len(selected_df))} "
                    "locations in the ranking chart."
                )
            )

        # Remove previous chart
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if self.figure is not None:
            plt.close(self.figure)
            self.figure = None

        # Create and display updated chart
        self.figure = create_figure(
            chart_data,
            self.metric_var.get(),
            int(self.top_n_var.get()),
            state_mode=state_mode,
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.chart_frame,
        )

        chart_widget = self.canvas.get_tk_widget()
        chart_widget.pack(fill="both", expand=True)

        self.canvas.draw_idle()

        self.chart_canvas.yview_moveto(0)
        self.root.update_idletasks()
        self._update_scroll_region()
