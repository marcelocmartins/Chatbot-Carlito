from CarlitoDB import DB_Commands
from datetime import datetime

contato = 'Marcelo'
status = '01231'
nota = '3'
ultima_hora = datetime.now()
chamado = ''
tabela = ''

commands = DB_Commands()



# tabela1 = str.replace()str.replace(str.replace(str.replace(tabela1, "\\", ''),'(',''),')','')


tabela = commands.select_table(status)

resposta = commands.select_response(status, tabela)

print(resposta)