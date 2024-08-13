import ipywidgets as widgets
from IPython.display import display


class View:
    def __init__(self, view_model) -> None:
        self._view_model = view_model

        self.start_datepicker = widgets.DatePicker(description="Start", disabled=False)
        self.end_datepicker = widgets.DatePicker(description="End", disabled=False)
        self.label_test = widgets.Label("")
        self.print_url_button = widgets.Button(description="Print URL")

        self.start_datepicker.observe(self._on_start_picker_change, names="value")
        self.end_datepicker.observe(self._on_end_picker_change, names="value")
        self.print_url_button.on_click(self._print_url)

    def _on_start_picker_change(self, change):
        if change["new"] is not None:
            self._view_model.start_date = change["new"].strftime("%b%d.%Y")
            self._update_label()

    def _on_end_picker_change(self, change):
        if change["new"] is not None:
            self._view_model.end_date = change["new"].strftime("%b%d.%Y")
            self._update_label()

    def _update_label(self):
        self.label_test.value = (
            f"Start: {self._view_model.start_date}, End: {self._view_model.end_date}"
        )

    def _print_url(self, button):
        # Imprime el valor actual de model.url
        print(f"Current model URL: {self._view_model._model.url}")

    def display_datepickers(self):
        display(self.start_datepicker)
        display(self.end_datepicker)
        display(self.label_test)
        display(self.print_url_button)
