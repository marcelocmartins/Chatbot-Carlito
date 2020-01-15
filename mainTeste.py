from _datetime import datetime, timedelta
import re
from tkinter import *
from botTeste import HBot
import time
from CarlitoDB import DB_Commands

#####
# Setamos nosso bot passando o nome do mesmo.
cbot = HBot('Carlito')

#Comando para iniciar = abre o Chrome e entra no whatsapp web
cbot.inicia()

#trabalhando com lista  de contatos atual
#cada linha se refere a um contato
#cada coluna se refere a uma determinada informação deste contato
#[0 = nome_contato, 1 = status, 2 = ultima_interacao data, 3 = ultimo_texto, 4= ultima entrada valida]
lista_contatos = []

#controle de conversa aberta ou não
# 0 = não , 1 = sim
# estado inicial sempre será 0 pois nenhuma conversa será aberta logo ao iniciar
conversa_aberta = '0'
contato_antigo = []

while True:
    #procura conversa com msg nao lida (se há "bolinha verde" no canto)
    conversa_aberta = cbot.procura_conv_nao_lida()


    if conversa_aberta == '1':
        # Vamos procurar o contato/grupo que está em um span
        # e possui o título igual que buscamos e vamos clicar.
        nome_contato = cbot.retorna_contato()
        print('nome encontrado na barra superior: '+nome_contato)

        if nome_contato != 'exception':
            # Procura se o contato está na lista de contatos atuais


                #ordena
                #lista_contatos.sort()

            i = 0
            indice_atual = -1
            #procura indice atual
            while i < len(lista_contatos):
                if nome_contato == lista_contatos[i][0]:
                    indice_atual = i
                i = i+1

            if indice_atual < 0:
                #se nao encontra o contato, cria uma nova instancia para a lista
                lista_contatos.append([nome_contato, '0', datetime.now(), ''])
                indice_atual = len(lista_contatos) - 1
                print('contato add a lista')

            print('indice que encontrou o contato: '+ str(indice_atual))
            print(' contato: '+ str(lista_contatos[indice_atual]))
            texto = cbot.escuta()

            # Verifica se o status tem $!


            # Verifica se o status tem $? e armazena o número do chamado
            #se o texto for diferente do último texto da lista de informações do contato
            #o bot deve interpretar o que foi dito e responder
            print('entrada: ' + texto + ' / ultimo texto da conversa: '+ str(lista_contatos[indice_atual][3]))

            if not len(lista_contatos[indice_atual]) > 4:





                if texto != lista_contatos[indice_atual][3]:

                   #setamos o texto lido como o último texto da conversa
                    lista_contatos[indice_atual][3] = texto

                    #pegamos o estado atual do indice e procuramos a resposta
                    estado_atual = lista_contatos[indice_atual][1]
                    print('atual status: ' + str(lista_contatos[indice_atual][1]))
                    response, novo_status = cbot.responde(texto, estado_atual)

                if re.findall('!', lista_contatos[indice_atual][1]):
                    lista_contatos[indice_atual].append(texto)
                    cbot.commands.insert_db_nota(lista_contatos[indice_atual][0], lista_contatos[indice_atual][1],lista_contatos[indice_atual][2], lista_contatos[indice_atual][4])

                if re.findall('#', lista_contatos[indice_atual][1]):
                    lista_contatos[indice_atual].append(texto)
                    cbot.commands.insert_db_chamado(lista_contatos[indice_atual][0], lista_contatos[indice_atual][1], lista_contatos[indice_atual][2], lista_contatos[indice_atual][4])

                    #cbot.salva_conversa(response, texto)

                #seta status trazido da resposta
                lista_contatos[indice_atual][1] = novo_status
                print('novo status: '+ str(lista_contatos[indice_atual][1]))
                lista_contatos[indice_atual][2] = datetime.now()
                print('nova data: '+ str(lista_contatos[indice_atual][2]))
                lista_contatos[indice_atual][3] = response
                print('nova ult msg: '+ str(lista_contatos[indice_atual][3]))
                print('contato pos interacao: ' + str(lista_contatos[indice_atual]))
                print('------------')


    cbot.tira_contato_hora(lista_contatos)



