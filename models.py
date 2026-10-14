class ReuniaoModel:

  def __init__(self, data_str, membros, convidados_novos):
    self.data_str = data_str
    self.membros = int(membros) if str(membros).isdigit() else 0
    self.convidados_novos = (
        int(convidados_novos) if str(convidados_novos).isdigit() else 0
    )

  @property
  def convidados_total(self):
    return self.convidados_novos

  @property
  def total_participantes(self):
    return self.membros + self.convidados_total

  def validar(self):
    if self.membros < 0:
      return False, "O número de membros não pode ser negativo."
    if self.convidados_novos < 0:
      return False, "A quantidade de convidados novos deve ser maior ou igual a zero."
    return True, "Validação concluída com sucesso."