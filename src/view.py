import ipywidgets as widgets
from IPython.display import display


class View:
    def __init__(self, view_model) -> None:
        self._view_model = view_model

        self.start_datepicker = widgets.DatePicker(description="Start", disabled=False)
        self.end_datepicker = widgets.DatePicker(description="End", disabled=False)

        self.label_url = widgets.Label("Please fill in the blanks")

        # Checkboxes for Event Types
        self.event_options = widgets.HBox(
            [
                widgets.VBox(
                    [
                        widgets.Checkbox(value=False, description="Growth"),
                        widgets.Checkbox(value=False, description="Inflation"),
                        widgets.Checkbox(value=False, description="Employment"),
                        widgets.Checkbox(value=False, description="Central Bank"),
                        widgets.Checkbox(value=False, description="Bonds"),
                    ]
                ),
                widgets.VBox(
                    [
                        widgets.Checkbox(value=False, description="All Events"),
                        widgets.Checkbox(value=False, description="Housing"),
                        widgets.Checkbox(value=False, description="Consumer Surveys"),
                        widgets.Checkbox(value=False, description="Business Surveys"),
                        widgets.Checkbox(value=False, description="Speeches"),
                        widgets.Checkbox(value=False, description="Misc"),
                    ]
                ),
            ]
        )

        self.currencies_options = widgets.HBox(
            [
                widgets.VBox(
                    [
                        widgets.Checkbox(description="AUD", value=False),
                        widgets.Checkbox(description="CAD", value=False),
                        widgets.Checkbox(description="CHF", value=False),
                        widgets.Checkbox(description="CNY", value=False),
                        widgets.Checkbox(description="EUR", value=False),
                    ]
                ),
                widgets.VBox(
                    [
                        widgets.Checkbox(description="GBP", value=False),
                        widgets.Checkbox(description="JPY", value=False),
                        widgets.Checkbox(description="NZD", value=False),
                        widgets.Checkbox(description="USD", value=False),
                    ]
                ),
            ]
        )

        self.impact_options = widgets.HBox(
            [
                widgets.Checkbox(description="Gray", value=False),
                widgets.Checkbox(description="Yellow", value=False),
                widgets.Checkbox(description="Orange", value=False),
                widgets.Checkbox(description="Red", value=False),
            ]
        )

        self.start_datepicker.observe(self._on_start_picker_change, names="value")
        self.end_datepicker.observe(self._on_end_picker_change, names="value")
        for checkbox in self.currencies_options.children:
            checkbox.observe(self._on_currencies_change, names="value")
        for checkbox in self.impact_options.children:
            checkbox.observe(self._on_impact_change, names="value")
        for checkbox in self.event_options.children:
            checkbox.observe(self._on_event_type_change, names="value")

        self.update_label_button = widgets.Button(description="Print URL")
        self.update_label_button.on_click(self._print_url)

    def _on_start_picker_change(self, change):
        if change["new"] is not None:
            self._view_model.start_date = change["new"].strftime("%b%d.%Y")
            self._update_label()

    def _on_end_picker_change(self, change):
        if change["new"] is not None:
            self._view_model.end_date = change["new"].strftime("%b%d.%Y")
            self._update_label()

    def _on_event_type_change(self, change):
        selected_events = [
            idx + 1
            for idx, checkbox in enumerate(self.event_options.children)
            if checkbox.value
        ]
        self._view_model.event_types = ",".join(map(str, selected_events))
        self._update_label()

    def _on_currencies_change(self, change):
        selected_currencies = [
            idx + 1
            for idx, checkbox in enumerate(self.currencies_options.children)
            if checkbox.value
        ]
        self._view_model.currencies = ",".join(map(str, selected_currencies))
        self._update_label()

    def _on_impact_change(self, change):
        selected_impacts = [
            idx
            for idx, checkbox in enumerate(self.impact_options.children)
            if checkbox.value
        ]
        self._view_model.impacts = ",".join(map(str, selected_impacts))
        self._update_label()

    def _update_label(self):
        self.label_url.value = (
            f"Start: {self._view_model.start_date}, End: {self._view_model.end_date}, "
            f"Currencies: {self._view_model.currencies}, Impacts: {self._view_model.impacts}, "
            f"Event Types: {self._view_model.event_types}"
        )

    def _print_url(self, button):
        print(self._view_model.url)

    def display_datepickers(self):
        display(self.start_datepicker)
        display(self.end_datepicker)
        display(self.label_url)
        display(self.currencies_options)
        display(self.impact_options)
        display(self.event_options)
        display(self.update_label_button)
