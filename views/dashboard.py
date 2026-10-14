import math
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from exporter import exportar_para_excel, exportar_para_pdf


def criar_textura_degrade(cor_topo, cor_base):
  texture = Texture.create(size=(1, 2), colorfmt="rgba")
  buf = bytes(cor_topo + cor_base)
  texture.blit_buffer(buf, colorfmt="rgba", bufferfmt="ubyte")
  texture.mag_filter = "linear"
  return texture


class PieChart3DWidget(FloatLayout):
  """Gráfico de Pizza corrigido com preenchimento adequado e estatísticas."""

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.size_hint_y = None
    self.height = "240dp"
    self.locais_data = []
    self.bind(pos=self.draw_chart, size=self.draw_chart)

  def update_data(self, reunioes):
      contagem_locais = {}

      for reg in reunioes:
          # reg[2] = local, reg[3] = membros (ou o índice correto da quantidade de membros)
          local_raw = reg[2] if len(reg) > 6 and reg[2] else "Sede Principal"
          local = local_raw.strip().title()

          # Pega a quantidade de membros da reunião (ajuste o índice se necessário, ex: reg[3])
          try:
              membros = int(reg[3]) if len(reg) > 3 else 0
          except (ValueError, TypeError):
              membros = 0

          contagem_locais[local] = contagem_locais.get(local, 0) + membros

      total_geral = (
          sum(contagem_locais.values()) if contagem_locais else 1
      )  # Soma total de todas as pessoas

      self.locais_data = []
      cores = [
          (0.92, 0.22, 0.52, 1),
          (0.58, 0.22, 0.88, 1),
          (0.15, 0.68, 0.92, 1),
          (0.25, 0.82, 0.38, 1),
          (0.95, 0.65, 0.15, 1),
          (0.85, 0.35, 0.95, 1),
      ]

      idx = 0
      for local, qtd in contagem_locais.items():
          pct = (qtd / total_geral) * 100
          self.locais_data.append(
              {"local": local, "qtd": qtd, "pct": pct, "cor": cores[idx % len(cores)]}
          )
          idx += 1

      self.draw_chart()

  def draw_chart(self, *args):
    self.canvas.before.clear()
    self.canvas.clear()
    self.clear_widgets()

    with self.canvas.before:
      Color(0.12, 0.16, 0.22, 0.85)
      RoundedRectangle(pos=self.pos, size=self.size, radius=[16])

    if not self.locais_data:
      return

    cx = self.x + 110
    cy = self.center_y
    raio = 80

    angulo_acumulado = 0
    with self.canvas:
      for item in self.locais_data:
        pct = item["pct"]
        angulo_fatia = (pct / 100.0) * 360

        r, g, b, a = item["cor"]
        Color(r, g, b, a)

        # Desenho das fatias da pizza
        Ellipse(
            pos=(cx - raio, cy - raio), size=(raio * 2, raio * 2), angle_start=angulo_acumulado, angle_end=angulo_acumulado + angulo_fatia
        )
        angulo_acumulado += angulo_fatia

    # Exibir porcentagem sobre as fatias
    angulo_acumulado = 0
    for item in self.locais_data:
      pct = item["pct"]
      angulo_fatia = (pct / 100.0) * 360
      angulo_medio = angulo_acumulado + (angulo_fatia / 2)
      angulo_acumulado += angulo_fatia

      rad = math.radians(angulo_medio)
      tx = cx + (raio * 0.55) * math.cos(rad) - 20
      ty = cy + (raio * 0.55) * math.sin(rad) - 10

      lbl_pct = MDLabel(
          text=f"{pct:.0f}%",
          font_style="Body",
          role="small",
          bold=True,
          halign="center",
          theme_text_color="Custom",
          text_color=(1, 1, 1, 1),
          size_hint=(None, None),
          size=("40dp", "20dp"),
          pos=(tx, ty),
      )
      self.add_widget(lbl_pct)

    # Painel Lateral de Informações Úteis
    panel_x = self.x + 230
    panel_w = self.width - 250

    lbl_info_title = MDLabel(
        text="📊 Informações e Estatísticas",
        font_style="Title",
        role="small",
        bold=True,
        theme_text_color="Custom",
        text_color=(0.25, 0.82, 0.88, 1),
        size_hint=(None, None),
        size=(panel_w, "25dp"),
        pos=(panel_x, cy + 50),
    )
    self.add_widget(lbl_info_title)

    total_reunioes_locais = sum([item["qtd"] for item in self.locais_data])
    local_principal = (
        max(self.locais_data, key=lambda x: x["qtd"])["local"]
        if self.locais_data
        else "N/A"
    )

    infos = [
        f"• Total de Locais Ativos: {len(self.locais_data)}",
        f"• Reuniões Registradas: {total_reunioes_locais}",
        f"• Local em Destaque: {local_principal}",
    ]

    py = cy + 20
    for info in infos:
      lbl_inf = MDLabel(
          text=info,
          font_style="Body",
          role="small",
          theme_text_color="Custom",
          text_color=(0.85, 0.9, 0.95, 1),
          size_hint=(None, None),
          size=(panel_w, "20dp"),
          pos=(panel_x, py),
      )
      self.add_widget(lbl_inf)
      py -= 22


class TowerChart3DWidget(FloatLayout):
  """Gráfico de Torres 3D proporcional ao volume de membros por local."""

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.size_hint_y = None
    self.height = "250dp"
    self.locais_data = []
    self.bind(pos=self.draw_chart, size=self.draw_chart)

  def update_data(self, reunioes):
    contagem_locais = {}

    for reg in reunioes:
      local_raw = reg[2] if len(reg) > 6 and reg[2] else "Sede Principal"
      local = local_raw.strip().title()

      try:
        membros = int(reg[3]) if len(reg) > 3 else 0
      except (ValueError, TypeError):
        membros = 0

      contagem_locais[local] = contagem_locais.get(local, 0) + membros

    total_geral = sum(contagem_locais.values()) if contagem_locais else 1

    self.locais_data = []
    cores = [
        (0.92, 0.22, 0.52, 1),
        (0.58, 0.22, 0.88, 1),
        (0.15, 0.68, 0.92, 1),
        (0.25, 0.82, 0.38, 1),
        (0.95, 0.65, 0.15, 1),
        (0.85, 0.35, 0.95, 1),
    ]

    idx = 0
    for local, qtd in contagem_locais.items():
      pct = (qtd / total_geral) * 100
      self.locais_data.append(
          {"local": local, "qtd": qtd, "pct": pct, "cor": cores[idx % len(cores)]}
      )
      idx += 1

    self.draw_chart()

  def draw_chart(self, *args):
      self.canvas.before.clear()
      self.canvas.clear()
      self.clear_widgets()

      with self.canvas.before:
          Color(0.12, 0.16, 0.22, 0.85)
          RoundedRectangle(pos=self.pos, size=self.size, radius=[16])

      if not self.locais_data:
          return

      cx = self.x + 110
      cy = self.center_y
      raio = 80

      angulo_acumulado = 0
      with self.canvas:
          for item in self.locais_data:
              pct = item["pct"]
              angulo_fatia = (pct / 100.0) * 360

              r, g, b, a = item["cor"]
              Color(r, g, b, a)

              # Desenho das fatias da pizza
              Ellipse(
                  pos=(cx - raio, cy - raio), size=(raio * 2, raio * 2), angle_start=angulo_acumulado,
                  angle_end=angulo_acumulado + angulo_fatia
              )
              angulo_acumulado += angulo_fatia

      # Posicionamento centralizado das porcentagens dentro de cada fatia
      angulo_acumulado = 0
      for item in self.locais_data:
          pct = item["pct"]
          angulo_fatia = (pct / 100.0) * 360
          angulo_medio = angulo_acumulado + (angulo_fatia / 2)
          angulo_acumulado += angulo_fatia

          rad = math.radians(angulo_medio)
          # Ajustado para 0.65 para posicionar o texto bem no miolo/centro da fatia
          tx = cx + (raio * 0.62) * math.cos(rad) - 20
          ty = cy + (raio * 0.62) * math.sin(rad) - 10

          lbl_pct = MDLabel(
              text=f"{pct:.0f}%",
              font_style="Body",
              role="small",
              bold=True,
              halign="center",
              theme_text_color="Custom",
              text_color=(1, 1, 1, 1),
              size_hint=(None, None),
              size=("40dp", "20dp"),
              pos=(tx, ty),
          )
          self.add_widget(lbl_pct)

      # Painel Lateral de Informações Úteis
      panel_x = self.x + 230
      panel_w = self.width - 250

      lbl_info_title = MDLabel(
          text="📊 Informações e Estatísticas",
          font_style="Title",
          role="small",
          bold=True,
          theme_text_color="Custom",
          text_color=(0.25, 0.82, 0.88, 1),
          size_hint=(None, None),
          size=(panel_w, "25dp"),
          pos=(panel_x, cy + 50),
      )
      self.add_widget(lbl_info_title)

      total_reunioes_locais = sum([item["qtd"] for item in self.locais_data])
      local_principal = (
          max(self.locais_data, key=lambda x: x["qtd"])["local"]
          if self.locais_data
          else "N/A"
      )

      infos = [
          f"• Total de Locais Ativos: {len(self.locais_data)}",
          f"• Reuniões Registradas: {total_reunioes_locais}",
          f"• Local em Destaque: {local_principal}",
      ]

      py = cy + 20
      for info in infos:
          lbl_inf = MDLabel(
              text=info,
              font_style="Body",
              role="small",
              theme_text_color="Custom",
              text_color=(0.85, 0.9, 0.95, 1),
              size_hint=(None, None),
              size=(panel_w, "20dp"),
              pos=(panel_x, py),
          )
          self.add_widget(lbl_inf)
          py -= 22

  def draw_chart(self, *args):
    self.canvas.before.clear()
    self.canvas.clear()
    self.clear_widgets()

    with self.canvas.before:
      Color(0.12, 0.16, 0.22, 0.85)
      RoundedRectangle(pos=self.pos, size=self.size, radius=[16])

    if not self.locais_data:
      return

    w, h = self.width, self.height
    num_torres = len(self.locais_data)
    largura_torre = max(45, min(65, (w - 40) / num_torres - 15))
    espacamento = (
        (w - 20 - (largura_torre * num_torres)) / (num_torres + 1)
        if num_torres > 0
        else 20
    )

    max_qtd = max([item["qtd"] for item in self.locais_data] + [1])
    altura_max_desenho = h - 90

    with self.canvas:
      for i, item in enumerate(self.locais_data):
        x = self.x + 10 + espacamento + i * (largura_torre + espacamento)
        y = self.y + 45

        alt_torre = max(35, (item["qtd"] / max_qtd) * altura_max_desenho)

        Color(0.08, 0.10, 0.14, 1)
        RoundedRectangle(pos=(x, y), size=(largura_torre, 15), radius=[4])

        r, g, b, a = item["cor"]
        Color(r, g, b, a)
        Rectangle(pos=(x, y + 12), size=(largura_torre, alt_torre))

    for i, item in enumerate(self.locais_data):
      x = self.x + 10 + espacamento + i * (largura_torre + espacamento)
      y = self.y + 45
      alt_torre = max(35, (item["qtd"] / max_qtd) * altura_max_desenho)

      lbl_pct = MDLabel(
          text=f"{item['pct']:.0f}%",
          font_style="Title",
          role="small",
          bold=True,
          halign="center",
          theme_text_color="Custom",
          text_color=(1, 1, 1, 1),
          size_hint=(None, None),
          size=(largura_torre, "30dp"),
          pos=(x, y + alt_torre - 10),
      )
      self.add_widget(lbl_pct)

      lbl_nome = MDLabel(
          text=item["local"],
          font_style="Body",
          role="small",
          bold=True,
          halign="center",
          theme_text_color="Custom",
          text_color=(0.8, 0.85, 0.9, 1),
          size_hint=(None, None),
          size=(largura_torre + 20, "20dp"),
          pos=(x - 10, self.y + 15),
      )
      self.add_widget(lbl_nome)


class MetricCard(MDCard):

  def __init__(self, title, value, bg_color_rgba, **kwargs):
    super().__init__(**kwargs)
    self.orientation = "vertical"
    self.padding = ["16dp", "12dp", "16dp", "12dp"]
    self.spacing = "4dp"
    self.size_hint_y = None
    self.height = "95dp"
    self.style = "filled"
    self.md_bg_color = bg_color_rgba
    self.radius = [16]

    lbl_title = MDLabel(
        text=title,
        font_style="Body",
        role="medium",
        theme_text_color="Custom",
        text_color=(1, 1, 1, 0.85),
    )
    lbl_val = MDLabel(
        text=str(value),
        font_style="Display",
        role="small",
        bold=True,
        theme_text_color="Custom",
        text_color=(1, 1, 1, 1),
    )
    self.add_widget(lbl_title)
    self.add_widget(lbl_val)


class DashboardScreen(MDScreen):

  def __init__(self, db_manager, **kwargs):
    self.grid_cards = None
    self.container_resumo = None
    self.chart_torres = None
    self.chart_pizza = None
    self.menu_exportar = None
    self.bg_rect = None
    super().__init__(**kwargs)
    self.db_manager = db_manager

    self.aplicar_fundo_degrade()
    self.build_ui()

  def aplicar_fundo_degrade(self):
    with self.canvas.before:
      Color(1, 1, 1, 1)
      textura = criar_textura_degrade([13, 17, 23, 255], [22, 27, 34, 255])
      self.bg_rect = Rectangle(
          texture=textura, pos=self.pos, size=self.size
      )
    self.bind(pos=self.atualizar_bg, size=self.atualizar_bg)

  def atualizar_bg(self, *args):
    if self.bg_rect:
      self.bg_rect.pos = self.pos
      self.bg_rect.size = self.size

  def build_ui(self):
    scroll = ScrollView()
    layout = BoxLayout(
        orientation="vertical",
        padding="16dp",
        spacing="16dp",
        size_hint_y=None,
    )
    layout.bind(minimum_height=layout.setter("height"))

    header = MDLabel(
        text="Dashboard Frequência\n(ALGO A MAIS)",
        font_style="Title",
        role="medium",
        bold=True,
        theme_text_color="Custom",
        text_color=(1, 1, 1, 1),
        size_hint_y=None,
        height="50dp",
    )
    layout.add_widget(header)

    sub_torres = MDLabel(
        text="Distribuição por Torres (Nome & %)",
        font_style="Body",
        role="medium",
        theme_text_color="Custom",
        text_color=(0.7, 0.75, 0.8, 1),
        size_hint_y=None,
        height="24dp",
    )
    layout.add_widget(sub_torres)

    self.chart_torres = TowerChart3DWidget()
    layout.add_widget(self.chart_torres)

    sub_pizza = MDLabel(
        text="Distribuição por Gráfico de Pizza & Estatísticas",
        font_style="Body",
        role="medium",
        theme_text_color="Custom",
        text_color=(0.7, 0.75, 0.8, 1),
        size_hint_y=None,
        height="24dp",
    )
    layout.add_widget(sub_pizza)

    self.chart_pizza = PieChart3DWidget()
    layout.add_widget(self.chart_pizza)

    self.grid_cards = GridLayout(cols=2, spacing="12dp", size_hint_y=None)
    self.grid_cards.bind(minimum_height=self.grid_cards.setter("height"))
    layout.add_widget(self.grid_cards)

    self.container_resumo = MDCard(
        orientation="vertical",
        padding="16dp",
        spacing="8dp",
        size_hint_y=None,
        height="170dp",
        style="filled",
        md_bg_color=(0.12, 0.16, 0.22, 0.85),
        radius=[16],
    )
    layout.add_widget(self.container_resumo)

    btn_novo = MDButton(
        MDButtonText(
            text="+ Preencher Novo Relatório",
            theme_text_color="Custom",
            text_color=(0.07, 0.09, 0.12, 1),
            bold=True,
        ),
        style="filled",
        size_hint_x=1,
        size_hint_y=None,
        height="52dp",
        md_bg_color=(0.25, 0.82, 0.88, 1),
        on_release=self.ir_para_formulario,
    )
    layout.add_widget(btn_novo)

    btn_exportar = MDButton(
        MDButtonText(
            text="Exportar / Compartilhar Relatório",
            theme_text_color="Custom",
            text_color=(0.07, 0.09, 0.12, 1),
            bold=True,
        ),
        style="filled",
        size_hint_x=1,
        size_hint_y=None,
        height="50dp",
        md_bg_color=(0.95, 0.75, 0.25, 1),
        on_release=self.abrir_menu_exportar,
    )
    layout.add_widget(btn_exportar)

    btn_historico = MDButton(
        MDButtonText(
            text="Ver Histórico e Editar Relatórios",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
        ),
        style="outlined",
        size_hint_x=1,
        size_hint_y=None,
        height="48dp",
        on_release=self.ir_para_historico,
    )
    layout.add_widget(btn_historico)

    scroll.add_widget(layout)
    self.add_widget(scroll)

  def abrir_menu_exportar(self, button_instance):
    items_menu = [
        {
            "text": "Exportar e Compartilhar PDF",
            "on_release": lambda: self.executar_exportacao("pdf"),
        },
        {
            "text": "Exportar e Compartilhar Excel",
            "on_release": lambda: self.executar_exportacao("excel"),
        },
    ]
    self.menu_exportar = MDDropdownMenu(
        caller=button_instance, items=items_menu, width_mult=4
    )
    self.menu_exportar.open()

  def executar_exportacao(self, tipo):
    if self.menu_exportar:
      self.menu_exportar.dismiss()
    if tipo == "pdf":
      exportar_para_pdf()
    elif tipo == "excel":
      exportar_para_excel()

  def on_pre_enter(self, *args):
    super().on_pre_enter(*args)
    self.atualizar_dashboard()

  def atualizar_dashboard(self):
    if self.grid_cards is None:
      return

    self.grid_cards.clear_widgets()
    (
        total_reunioes,
        media_part,
        media_memb,
        media_conv,
    ) = self.db_manager.obter_estatisticas_gerais()

    self.grid_cards.add_widget(
        MetricCard(
            "Reuniões Realizadas", total_reunioes, (0.88, 0.58, 0.22, 0.9)
        )
    )
    self.grid_cards.add_widget(
        MetricCard(
            "Média de Presença Total",
            int(media_part),
            (0.22, 0.62, 0.66, 0.9),
        )
    )
    self.grid_cards.add_widget(
        MetricCard(
            "Média de Membros", int(media_memb), (0.18, 0.68, 0.38, 0.9)
        )
    )
    self.grid_cards.add_widget(
        MetricCard(
            "Média de Convidados", int(media_conv), (0.58, 0.32, 0.72, 0.9)
        )
    )

    reunioes = self.db_manager.listar_reunioes()

    if self.chart_torres:
      self.chart_torres.update_data(reunioes)
    if self.chart_pizza:
      self.chart_pizza.update_data(reunioes)

    self.container_resumo.clear_widgets()
    lbl_resumo_title = MDLabel(
        text=(
            f"Resumo da Última Reunião ({reunioes[0][1]})"
            if reunioes
            else "Resumo da Última Reunião"
        ),
        font_style="Title",
        role="small",
        bold=True,
        theme_text_color="Custom",
        text_color=(1, 1, 1, 1),
    )
    self.container_resumo.add_widget(lbl_resumo_title)

    if reunioes:
      ultimo = reunioes[0]
      detalhes = [
          ("Local", ultimo[2]),
          ("Membros", ultimo[3]),
          ("Total Reunião", ultimo[6]),
      ]
      for rotulo, valor in detalhes:
        row = BoxLayout(orientation="horizontal")
        row.add_widget(
            MDLabel(
                text=rotulo,
                theme_text_color="Custom",
                text_color=(0.7, 0.75, 0.8, 1),
            )
        )
        row.add_widget(
            MDLabel(
                text=str(valor),
                bold=True,
                halign="right",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
            )
        )
        self.container_resumo.add_widget(row)
    else:
      self.container_resumo.add_widget(
          MDLabel(
              text="Nenhum registro cadastrado ainda.",
              theme_text_color="Custom",
              text_color=(0.6, 0.6, 0.6, 1),
          )
      )

  def ir_para_formulario(self, *args):
    form_screen = self.manager.get_screen("formulario")
    form_screen.preparar_novo_registro()
    self.manager.current = "formulario"

  def ir_para_historico(self, *args):
    self.manager.current = "historico"