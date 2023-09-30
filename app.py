from password_manager.model import Model
from password_manager.view import View
from password_manager.presenter import Presenter


if __name__ == "__main__":
    presenter = Presenter(Model, View)
    presenter.run()
