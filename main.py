from src.model import Model
from src.view import View
from src.viewmodel import ViewModel

model = Model()
viewmodel = ViewModel(model)
view = View(viewmodel)