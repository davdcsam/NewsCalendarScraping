import ipywidgets as widgets
from IPython.display import display


class View:
    def __init__(self, view_model) -> None:
        self._view_model = view_model

        self.start_datepicker = widgets.DatePicker(description="Start", disabled=False)
        self.end_datepicker = widgets.DatePicker(description="End", disabled=False)

        self.currencies_checklist = widgets.Checkbox(
            description="Currencies", value=False
        )

        self.currencies_options = widgets.VBox(
            [
                widgets.Checkbox(description="AUD", value=False),
                widgets.Checkbox(description="CAD", value=False),
                widgets.Checkbox(description="CHF", value=False),
                widgets.Checkbox(description="CNY", value=False),
                widgets.Checkbox(description="EUR", value=False),
                widgets.Checkbox(description="GBP", value=False),
                widgets.Checkbox(description="JPY", value=False),
                widgets.Checkbox(description="NZD", value=False),
                widgets.Checkbox(description="USD", value=False),
            ]
        )

        self.label_test = widgets.Label("Fill in all entry points")

        self.start_datepicker.observe(self._on_start_picker_change, names="value")
        self.end_datepicker.observe(self._on_end_picker_change, names="value")
        for checkbox in self.currencies_options.children:
            checkbox.observe(self._on_currencies_change, names="value")

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

    def _on_currencies_change(self, change):
        selected_currencies = [
            idx + 1
            for idx, checkbox in enumerate(self.currencies_options.children)
            if checkbox.value
        ]
        self._view_model.currencies = ",".join(map(str, selected_currencies))
        self._update_label()

    def _update_label(self):
        self.label_test.value = f"Start: {self._view_model.start_date}, End: {self._view_model.end_date}, Currencies: {self._view_model.currencies}"

    def _print_url(self, button):
        print(self._view_model.url)

    def display_datepickers(self):
        display(self.start_datepicker)
        display(self.end_datepicker)
        display(self.currencies_options)
        display(self.label_test)
        display(self.update_label_button)
