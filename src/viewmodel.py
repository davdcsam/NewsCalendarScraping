from traitlets import HasTraits, Unicode, observe

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
        self._model.start_date = change["new"]

    @observe("end_date")
    def _on_end_date_change(self, change):
        self._model.end_date = change["new"]

    @observe("url")
    def _update_model(self, change):
        self._model.url = change["new"]
