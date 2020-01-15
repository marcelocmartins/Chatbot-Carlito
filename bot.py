import os
import time
import re
from datetime import datetime
from datetime import timedelta
from sys import exc_info
from typing import List

import click as click

#import Point as Point
import bs4
import requests
from time import sleep

from chatterbot.trainers import ListTrainer
from chatterbot import *
from selenium import webdriver


from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement


class HBot:
    # Setamos o caminho de nossa aplicação.
    dir_path = os.getcwd()

    # Nosso contrutor terá a entrada do nome do nosso
    def __init__(self, bot):
        # Setamos nosso bot e a forma que ele irá treinar.
        self.bot = ChatBot(bot)
        self.bot.set_trainer(ListTrainer)
        # Setamos onde está nosso chromedriver.
        self.chrome = self.dir_path + '\chromedriver.exe'
        # Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=" + self.dir_path + "\profile\wpp")
        # Iniciamos o driver.
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    def inicia(self):
        # Selenium irá entrar no whats e aguardar 10 segundos até o dom estiver pronto.
        self.driver.get('https://web.whatsapp.com')
        self.driver.implicitly_wait(10)

    def escuta(self):
        # Vamos setar todos as mensagens no grupo.
        post = self.driver.find_elements_by_class_name('_3_7SH')
        # Vamos pegar o índice da última conversa.
        ultimo = len(post) - 1
        # Vamos pegar o  texto da última conversa e retornar.

        try:
            texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        except Exception:
            texto = 'exception'

        return texto

    def imprime_resposta(self, texto):

        try:
            self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
            self.caixa_de_mensagem.send_keys(texto)
            time.sleep(1)
            self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
            self.botao_enviar.click()

            self.clica_fora = self.driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/input') #_3_7SH _3qMSo message-out
            self.clica_fora.click()
            self.clica_fora = self.driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/input')  # _3_7SH _3qMSo message-out
            self.clica_fora.click()
        except:
            print(texto)

    def responde(self, texto, estado_atual):
        # Setamos a reposta do bot na variável response.
        # response = self.bot.get_response(texto)
        # Transformas em string essa resposta.

        ################    AQUI     ###############

        eh_final = '0'

        eh_valida = self.valida_input(texto, estado_atual)

        #se for valida
        if eh_valida:



            # Se o status atual for final, pula os blocos de execução de fluxo normal e seta a resposta como
            if not (re.findall('#', estado_atual)) or (re.findall('!', estado_atual)):

                    #verifica se estado nao é zero, se sim procura resposta de estado+input
                    #a qualquer momento, se digitar 0 volta ao menu inicial
                    if texto == '0':
                        estado_atual = '0'

                    if estado_atual != '0':

                        if texto.lower() == 'voltar':

                            estado_procura = estado_atual[0:len(estado_atual)-1]

                            if estado_procura == '01':
                                estado_procura = '0'

                        else:

                            estado_procura = str(self.gera_indice_procura(texto, estado_atual)) #str(estado_atual) + str(texto)

                    else:
                        #caso estado atual seja 0, busca resposta pra 0
                        estado_procura = str(estado_atual)

                # Se for um status final, executa os fluxos de encontrar resposta,

                    #armazena resposta trazida pelo estado procurado
                    response, eh_final = self.encontra_resposta(estado_procura)
                    response = str(response)
                    # response = str.replace(response, 'PpP', '%0D%0D')

                    #####atualiza qual estado deve ir
                    if estado_atual != '0':
                        if response != 'invalida':

                            # atualiza resposta
                            if eh_final == '1':
                                self.imprime_resposta(response)
                                novo_status = estado_procura + '!'
                                estado_atual = novo_status
                                return response, str(novo_status)

                            if eh_final == '2':
                                self.imprime_resposta(response)
                                novo_status = estado_procura + '#'
                                estado_atual = novo_status
                                return response, str(novo_status)

                            if eh_final == '0':
                                self.imprime_resposta(response)
                                novo_status = estado_procura
                                #return response, str(novo_status)
                        else:

                            if estado_atual == '01':
                                novo_status = '0'

                            else:
                                novo_status = estado_atual

                            self.imprime_resposta('Resposta não encontrada para a opção informada, favor conferir novamente as opções')
                            response = self.encontra_resposta(novo_status)
                            response = str(response)
                            self.imprime_resposta(response)

                        if novo_status == '0':
                            novo_status = '0' + '1'


                    else:
                        self.imprime_resposta(response)
                        novo_status = '0' + '1'

                    ######

            # Se a resposta é válida e tem status final
            else:

                if re.findall('!', estado_atual):
                    response = 'Obrigado por sua avaliação'
                    self.imprime_resposta(response)

                else:
                    re.findall('#', estado_atual)
                    response = 'Obrigado por informar o número do chamado, após a sua resolução estarei apto a auxiliá-lo melhor no futuro'
                    self.imprime_resposta(response)
                    final = '1'
                    return final


        # Se a resposta não é valida
        else:

            if re.findall('!', estado_atual):
                eh_final = '1'

            if re.findall('#', estado_atual):
                eh_final = '2'


            if eh_final == '0':

                self.imprime_resposta('Resposta invalida, favor conferir novamente as opções')
                response = self.encontra_resposta(estado_atual)
                response = str(response)
                self.imprime_resposta(response)
                novo_status = estado_atual

            if eh_final == '2':
                self.imprime_resposta('Número do chamado inválido, o número não pode ter menos de 6 e mais de 8)')
                response = 'Por favor informe o número do chamado que você abriu para que eu possa monitorá-lo'
                self.imprime_resposta(response)
                novo_status = estado_atual
                return '0'


            if eh_final == '1':
                self.imprime_resposta('A avaliação deve ser de 1 a 3')
                response = 'Use *1* para Ruim, *2* para Bom e *3* para Ótimo'
                self.imprime_resposta(response)
                novo_status = estado_atual
                return '0'




        # Setamos caixa de mensagens preenchemos com a resposta e clicamos em enviar.

        # retorna para gravar em arquivo
        return str(response), str(novo_status)

    def procura_conv_nao_lida(self):

        abrir = '0'

        #Tenta abrir conversa que esteja com tag de nao lida _15G96
        try:

            self.contato = self.driver.find_element_by_xpath('//div/div/div/span/div/span[@class = "OUeyt"]')
            self.contato.click()
            self.contato.click()
            self.contato.click()
            time.sleep(1)

            abrir = '1'
        except:
            abrir = '0'

        return abrir

    def encontra_resposta(self, status):



        if status == '0':
            resposta = 'Ola, obrigado pelo contato! Estou aqui para ajudá-lo.' \
                       'Para que possamos entender melhor sua situação, digite:\n' \
                       '*1* - WMS T1 (Fábrica) \n*2* - WMS T2 (CDD)'

            resposta2 = resposta

            eh_final = '0'
            return resposta2, eh_final
        else:

            #se passou nos requisitos de valida
            #iremos procurar no arquivo
            status = str(status) + '::'

            with open('Base ChatBot_v3.txt') as arquivo:
                print('status procurado: '+status)
                for line in arquivo:
                    if not re.match(status, line):
                        resposta = 'invalida'
                        eh_final = '0'

                    else:
                        # Valida se é um status final, seja
                        if re.match(status + '!', line):
                            status = status + '!'
                            resposta = line
                            eh_final = '1'
                            resposta = str.replace(resposta, status + ' ', '')
                            resposta = resposta.replace('\n', '')
                            resposta = resposta.replace('!', '')
                            arquivo.close()
                            # Retorna para a função RESPONDE
                            return resposta, eh_final

                        if re.match(status + '#', line):
                            status = status + '#'
                            resposta = line
                            eh_final = '2'
                            resposta = str.replace(resposta, status + ' ', '')
                            resposta = resposta.replace('\n', '')
                            resposta = resposta.replace('#', '')
                            arquivo.close()
                            # Retorna para a função RESPONDE
                            return resposta, eh_final

                        resposta = line
                        eh_final = '0'
                        resposta = str.replace(resposta, status + ' ', '')
                        resposta = resposta.replace('\n', '')
                        print('resposta do arquivo: '+resposta)
                        arquivo.close()
                        # Retorna para a função RESPONDE
                        return resposta, eh_final

            arquivo.close()

            return resposta, eh_final



    def gera_indice_procura(self, texto, estado):

        if not re.findall('!', estado) or re.findall('#', estado):
            if len(texto) > 1:
                texto = self.converte_dois_digitos(texto)

            # concatena status com o texto
            indice = str(estado) + str(texto)

            return indice

            if len(texto) == 1:
                # concatena status com o texto
                indice = str(estado) + str(texto)

                return indice

        else:
            return estado

    def valida_input(self, texto, estado):

        possiveis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                     'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                     'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        permitidas = ['voltar']

        avaliacao = ['1', '2', '3']

        if re.findall('!', estado):

            if texto in avaliacao:
                return 1
            else:
                return 0

        if re.findall('#', estado):

            if len(texto) > 6 and len(texto) < 9:
                return 1
            else:
                return 0

        if estado != '0':
            if len(texto) == 1:
                if texto in possiveis:
                    return 1
                else:
                    return 0
            else:
                texto = self.converte_dois_digitos(texto)
                if texto in possiveis:
                    return 1
                else:
                    if texto.lower() in permitidas:
                        return 1
                    else:
                        return 0

        return 1

    def salva_conversa(self, contato, status, horario, ultimo_texto, nota):
        ref_arquivo = open("Historico de Conversas.txt", "a+")

        ref_arquivo.write('\n')
        ref_arquivo.write('Contato: ')
        ref_arquivo.write(contato)
        ref_arquivo.write('\n')
        ref_arquivo.write('Status: ')
        ref_arquivo.write(status)
        ref_arquivo.write('\n')
        ref_arquivo.write('Horário da Ultima Interação: ')
        ref_arquivo.write(horario)
        ref_arquivo.write('\n')
        ref_arquivo.write('Ultimo texto: ')
        ref_arquivo.write(ultimo_texto)
        ref_arquivo.write('\n')
        ref_arquivo.write('Nota do atendimento/Numero do Chamado: ')
        ref_arquivo.write(nota)
        ref_arquivo.write('\n')

        ref_arquivo.close()

    def retorna_contato(self):
        #_3XrHh  _1wjf
        try:
            nome_contato = self.driver.find_element_by_xpath('//div[@class = "_3XrHh"]').text
        #nome_contato = 'contato'
        except:
            nome_contato = 'exception'

        return nome_contato

    def clica_fora(self):

        try:

            self.clica_fora = self.driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/input')  # _3_7SH _3qMSo message-out
            self.clica_fora.click()

        except:
            print('deu erro no clica fora')

    def tira_contato_hora(self, lista_contatos):

        tira_contato = 0
        while tira_contato < len(lista_contatos):
            # if datetime.strptime(lista_contatos([tira_contato][2],'%Y-%m-%d %H:%M:%S.%f' )) < datetime.now() - timedelta(minutes=20):
            if (lista_contatos[tira_contato][2] < datetime.now() - timedelta(minutes=20)) or (len(lista_contatos[tira_contato]) > 4):
                contato_antigo = lista_contatos[tira_contato]
                print('contato retirado da lista  ' + str(contato_antigo))
                lista_contatos.remove(contato_antigo)
            tira_contato = tira_contato + 1
            return lista_contatos


    def converte_dois_digitos (self, texto):
        if texto == '10':
            return 'A'
        if texto == '11':
            return 'B'
        if texto == '12':
            return 'C'
        if texto == '13':
            return 'D'
        if texto == '14':
            return 'E'
        if texto == '15':
            return 'F'
        if texto == '16':
            return 'G'
        if texto == '17':
            return 'H'
        if texto == '18':
            return 'I'
        if texto == '19':
            return 'J'
        if texto == '20':
            return 'K'
        if texto == '21':
            return 'L'
        if texto == '22':
            return 'M'
        if texto == '23':
            return 'N'
        if texto == '24':
            return 'O'
        if texto == '25':
            return 'P'
        if texto == '26':
            return 'Q'
        if texto == '27':
            return 'R'
        if texto == '28':
            return 'S'
        if texto == '29':
            return 'T'
        if texto == '30':
            return 'U'
        if texto == '31':
            return 'V'
        if texto == '32':
            return 'W'
        if texto == '33':
            return 'X'
        if texto == '34':
            return 'Y'
        if texto == '35':
            return 'Z'

        return 'invalido'