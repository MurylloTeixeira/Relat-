import sqlite3


class DatabaseManager:

  def __init__(self, db_name="frequencia_algo_a_mais.db"):
    self.db_name = db_name
    self.criar_tabela()

  def criar_tabela(self):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS reunioes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                local TEXT,
                membros INTEGER,
                convidados_novos INTEGER,
                convidados_total INTEGER,
                total_participantes INTEGER
            )
        """)
    conn.commit()
    conn.close()

  def inserir_reuniao(
      self, data, local, membros, convidados_novos, convidados_total, total_part
  ):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO reunioes (data, local, membros, convidados_novos, convidados_total, total_participantes)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (data, local, membros, convidados_novos, convidados_total, total_part),
    )
    conn.commit()
    conn.close()

  def atualizar_reuniao(
      self,
      id_reuniao,
      data,
      local,
      membros,
      convidados_novos,
      convidados_total,
      total_part,
  ):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE reunioes 
            SET data = ?, local = ?, membros = ?, convidados_novos = ?, convidados_total = ?, total_participantes = ?
            WHERE id = ?
        """,
        (
            data,
            local,
            membros,
            convidados_novos,
            convidados_total,
            total_part,
            id_reuniao,
        ),
    )
    conn.commit()
    conn.close()

  def listar_reunioes(self):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT id, data, local, membros, convidados_novos, convidados_total, total_participantes 
            FROM reunioes 
            ORDER BY id DESC
        """)
    dados = cursor.fetchall()
    conn.close()
    return dados

  def obter_estatisticas_gerais(self):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT 
                COUNT(*), 
                COALESCE(ROUND(AVG(total_participantes), 1), 0), 
                COALESCE(ROUND(AVG(membros), 1), 0), 
                COALESCE(ROUND(AVG(convidados_total), 1), 0)
            FROM reunioes
        """)
    stats = cursor.fetchone()
    conn.close()
    return stats