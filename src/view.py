import ipywidgets as widgets
from IPython.display import display

class View:
    def __init__(self, view_model) -> None:
        self._view_model = view_model

        self.start_DatePicker = widgets.DatePicker(
            description='Start',
            disabled=False
        )

        self.end_DatePicker = widgets.DatePicker(
            description='End',
            disabled=False
        )

        self.label_test = widgets.Label("Init")

        self.start_DatePicker.observe(self._on_start_picker_change, names="value")
        self.end_DatePicker.observe(self._on_end_picker_change, names="value")

    def _on_start_picker_change(self, change):
        if change["new"] is not None:
            self._view_model.start_date = str(change["new"])
            self._update_label()

    def _on_end_picker_change(self, change):
        if change["new"] is not None:
            self._view_model.end_date = str(change["new"])
            self._update_label()

    def _update_label(self):
        self.label_test.value = f"Start: {self._view_model.start_date}, End: {self._view_model.end_date}"

    def display_datepickers(self):
        display(self.start_DatePicker)
        display(self.end_DatePicker)
        display(self.label_test)
