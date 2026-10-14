from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class HistoryScreen(MDScreen):

  def __init__(self, db_manager, **kwargs):
    super().__init__(**kwargs)
    self.db_manager = db_manager
    self.md_bg_color = (0.07, 0.09, 0.12, 1)
    self.build_ui()

  def build_ui(self):
    scroll = ScrollView()
    self.layout_conteudo = BoxLayout(
        orientation="vertical",
        padding="20dp",
        spacing="12dp",
        size_hint_y=None,
    )
    self.layout_conteudo.bind(
        minimum_height=self.layout_conteudo.setter("height")
    )

    header = MDLabel(
        text="Histórico de Relatórios",
        font_style="Title",
        role="medium",
        bold=True,
        theme_text_color="Custom",
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height="40dp",
    )
    self.layout_conteudo.add_widget(header)

    self.container_cards = BoxLayout(
        orientation="vertical", spacing="10dp", size_hint_y=None
    )
    self.container_cards.bind(
        minimum_height=self.container_cards.setter("height")
    )
    self.layout_conteudo.add_widget(self.container_cards)

    btn_voltar = MDButton(
        MDButtonText(
            text="Voltar ao Dashboard",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
        ),
        style="outlined",
        size_hint_x=1,
        size_hint_y=None,
        height="48dp",
        on_release=lambda x: setattr(self.manager, "current", "dashboard"),
    )
    self.layout_conteudo.add_widget(btn_voltar)

    scroll.add_widget(self.layout_conteudo)
    self.add_widget(scroll)

  def on_pre_enter(self, *args):
    super().on_pre_enter(*args)
    self.carregar_historico()

  def carregar_historico(self):
    self.container_cards.clear_widgets()
    reunioes = self.db_manager.listar_reunioes()

    if not reunioes:
      lbl_vazio = MDLabel(
          text="Nenhum relatório encontrado.",
          font_style="Body",
          role="medium",
          theme_text_color="Custom",
          text_color=(0.6, 0.6, 0.6, 1),
          halign="center",
          size_hint_y=None,
          height="50dp",
      )
      self.container_cards.add_widget(lbl_vazio)
      return

    for reg in reunioes:
      reg_id, data_str, local, membros, conv_novos, conv_tot, total_geral = reg

      card = MDCard(
          orientation="vertical",
          padding="16dp",
          spacing="6dp",
          size_hint_y=None,
          height="105dp",
          style="filled",
          md_bg_color=(0.12, 0.16, 0.22, 0.85),
          radius=[12],
      )

      lbl_info = MDLabel(
          text=f"📅 Data: {data_str}  |  📍 Local: {local}",
          font_style="Title",
          role="small",
          bold=True,
          theme_text_color="Custom",
          text_color=(1, 1, 1, 1),
      )
      card.add_widget(lbl_info)

      lbl_detalhes = MDLabel(
          text=f"👥 Membros (Total): {total_geral}",
          font_style="Body",
          role="small",
          theme_text_color="Custom",
          text_color=(0.7, 0.75, 0.8, 1),
      )
      card.add_widget(lbl_detalhes)

      btn_editar = MDButton(
          MDButtonText(
              text="Editar Registro",
              theme_text_color="Custom",
              text_color=(0.07, 0.09, 0.12, 1),
              bold=True,
          ),
          style="filled",
          size_hint_x=1,
          size_hint_y=None,
          height="36dp",
          md_bg_color=(0.25, 0.82, 0.88, 1),
          on_release=lambda x, r=reg: self.editar_registro(r),
      )
      card.add_widget(btn_editar)
      self.container_cards.add_widget(card)

  def editar_registro(self, reg_data):
    form_screen = self.manager.get_screen("formulario")
    form_screen.carregar_para_edicao(reg_data)
    self.manager.current = "formulario"