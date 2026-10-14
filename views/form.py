from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText


class FormScreen(MDScreen):

  def __init__(self, db_manager, **kwargs):
    super().__init__(**kwargs)
    self.db_manager = db_manager
    self.edit_id = None
    self.md_bg_color = (0.07, 0.09, 0.12, 1)
    self.build_ui()

  def build_ui(self):
    scroll = ScrollView()
    layout = BoxLayout(
        orientation="vertical",
        padding="20dp",
        spacing="16dp",
        size_hint_y=None,
    )
    layout.bind(minimum_height=layout.setter("height"))

    self.lbl_titulo = MDLabel(
        text="Preencher Relatório",
        font_style="Title",
        role="medium",
        bold=True,
        theme_text_color="Custom",
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height="40dp",
    )
    layout.add_widget(self.lbl_titulo)

    # Campos essenciais simplificados
    self.input_data = MDTextField(
        MDTextFieldHintText(text="Data (DD/MM/AAAA)"),
        mode="outlined",
        size_hint_x=1,
    )
    layout.add_widget(self.input_data)

    self.input_local = MDTextField(
        MDTextFieldHintText(text="Local da Reunião (Ex: Sede, Auditório)"),
        mode="outlined",
        size_hint_x=1,
    )
    layout.add_widget(self.input_local)

    self.input_membros = MDTextField(
        MDTextFieldHintText(text="Quantidade de Membros"),
        mode="outlined",
        input_filter="int",
        size_hint_x=1,
    )
    layout.add_widget(self.input_membros)

    btn_salvar = MDButton(
        MDButtonText(
            text="Salvar Relatório",
            theme_text_color="Custom",
            text_color=(0.07, 0.09, 0.12, 1),
            bold=True,
        ),
        style="filled",
        size_hint_x=1,
        size_hint_y=None,
        height="52dp",
        md_bg_color=(0.25, 0.82, 0.88, 1),
        on_release=self.salvar_dados,
    )
    layout.add_widget(btn_salvar)

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
    layout.add_widget(btn_voltar)

    scroll.add_widget(layout)
    self.add_widget(scroll)

  def preparar_novo_registro(self):
    self.edit_id = None
    self.lbl_titulo.text = "Novo Relatório de Reunião"
    self.input_data.text = ""
    self.input_local.text = ""
    self.input_membros.text = ""

  def carregar_para_edicao(self, reg_data):
    # reg_data: (id, data, local, membros, conv_novos, conv_tot, total_part)
    self.edit_id = reg_data[0]
    self.lbl_titulo.text = f"Editar Relatório (ID: {self.edit_id})"
    self.input_data.text = str(reg_data[1])
    self.input_local.text = str(reg_data[2])
    self.input_membros.text = str(reg_data[3])

  def salvar_dados(self, *args):
    data = self.input_data.text.strip()
    local = self.input_local.text.strip() or "Sede Principal"
    try:
      membros = int(self.input_membros.text.strip() or 0)
    except ValueError:
      return

    if not data:
      return

    # Como os convidados foram removidos temporariamente, os valores ficam em 0
    conv_novos = 0
    convidados_total = 0
    total_participantes = membros

    if self.edit_id:
      self.db_manager.atualizar_reuniao(
          self.edit_id,
          data,
          local,
          membros,
          conv_novos,
          convidados_total,
          total_participantes,
      )
    else:
      self.db_manager.inserir_reuniao(
          data,
          local,
          membros,
          conv_novos,
          convidados_total,
          total_participantes,
      )

    self.manager.current = "dashboard"