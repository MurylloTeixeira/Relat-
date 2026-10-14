[app]

# (str) Título da sua aplicação (exibido na tela inicial do celular)
title = Relatô+

# (str) Nome do pacote (apenas letras minúsculas, sem espaços ou acentos)
package.name = relatoplus

# (str) Domínio do pacote
package.domain = org.muryllo

# (list) Extensões de ficheiros a incluir no APK
source.include_exts = py,png,jpg,kv,atlas,db

# (list) Diretório com o código-fonte
source.dir = .

# (str) Versão da aplicação
version = 1.0.0

# (list) Requisitos da aplicação (Python, Kivy, KivyMD 2.0.0 e bibliotecas adicionais)
requirements = python3,kivy,kivymd==2.0.0,openpyxl,reportlab,sqlite3,plyer

# (str) Ficheiro do ícone da aplicação (adicione a imagem do ícone como icon.png na raiz do projeto)
icon.filename = %(source.dir)s/icon.png

# (list) Permissões do Android necessárias para salvar e compartilhar relatórios em PDF/Excel
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Orientação suportada (portrait = vertical)
orientation = portrait

# (list) Arquiteturas suportadas (arm64-v8a cobre praticamente todos os celulares modernos)
android.archs = arm64-v8a

# (int) Nível de API mínimo suportado (Android 7.0+)
android.minapi = 24

# (int) Nível de API alvo (Android 13)
android.api = 33

# (str) Versão fixa do Android SDK Build Tools
android.build_tools_version = 33.0.2

[buildozer]

# (int) Nível de log (0 = apenas erros, 2 = debug completo)
log_level = 2

# (int) Exibir alerta ao rodar como root
warn_on_root = 1
