from traitlets import HasTraits, Unicode, observe
from datetime import datetime


class ViewModel(HasTraits):
    start_date = Unicode()
    end_date = Unicode()
    url = Unicode()

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.url = model.url

    @observe("start_date")
    def _on_start_date_change(self, change):
        self._update_url()

    @observe("end_date")
    def _on_end_date_change(self, change):
        self._update_url()

    def _update_url(self):
        if self.start_date and self.end_date:
            try:
                start_date_obj = datetime.strptime(self.start_date, "%b%d.%Y").date()
                end_date_obj = datetime.strptime(self.end_date, "%b%d.%Y").date()
            except ValueError:
                print("Err date format")
                return

            formatted_start = start_date_obj.strftime("%b%d.%Y")
            formatted_end = end_date_obj.strftime("%b%d.%Y")
            self.url = f"https://www.forexfactory.com/calendar?range={formatted_start}-{formatted_end}&permalink=true"
            print(f"ViewModel URL updated to: {self.url}")  # Mensaje de depuración
            self._model.url = self.url
