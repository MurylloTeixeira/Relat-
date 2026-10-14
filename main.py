from database import DatabaseManager
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from views.dashboard import DashboardScreen
from views.form import FormScreen
from views.history import HistoryScreen


class AlgoAMaisApp(MDApp):

  def build(self):
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "Cyan"

    self.db_manager = DatabaseManager()

    sm = MDScreenManager()
    sm.add_widget(
        DashboardScreen(name="dashboard", db_manager=self.db_manager)
    )
    sm.add_widget(FormScreen(name="formulario", db_manager=self.db_manager))
    sm.add_widget(HistoryScreen(name="historico", db_manager=self.db_manager))

    return sm


if __name__ == "__main__":
  AlgoAMaisApp().run()