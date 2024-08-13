from traitlets import HasTraits, Unicode, observe
from datetime import datetime


class ViewModel(HasTraits):
    start_date = Unicode()
    end_date = Unicode()
    url = Unicode()
    currencies = Unicode()
    impacts = Unicode()

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

    @observe("currencies")
    def _on_currencies_change(self, change):
        self._update_url()

    @observe("impacts")
    def _on_impacts_change(self, change):
        self._update_url()

    def _update_url(self):
        if self.start_date and self.end_date:
            try:
                start_date_obj = datetime.strptime(self.start_date, "%b%d.%Y").date()
                end_date_obj = datetime.strptime(self.end_date, "%b%d.%Y").date()
            except ValueError:
                print("Error en el formato de la fecha.")
                return

            # Dates
            formatted_start = start_date_obj.strftime("%b%d.%Y")
            formatted_end = end_date_obj.strftime("%b%d.%Y")

            # Currencies
            currencies_list = self.currencies.split(",")
            if len(currencies_list) == 1:
                currencies_param = currencies_list[0]
            else:
                currencies_param = ",".join(currencies_list)

            # Impacts
            impacts_list = [
                impact for impact in self.impacts.split(",") if impact.strip()
            ]
            impacts_list = [str(int(impact) - 1) for impact in impacts_list]
            if len(impacts_list) == 1:
                impacts_param = impacts_list[0]
            else:
                impacts_param = ",".join(impacts_list)

            self.url = f"{self._model.base_url}?range={formatted_start}-{formatted_end}&permalink=true&impacts={impacts_param}&event_types=1,2,3,4,5,7,8,9,10,11&currencies={currencies_param}"

            print(f"ViewModel URL updated to: {self.url}")
            self._model.url = self.url
