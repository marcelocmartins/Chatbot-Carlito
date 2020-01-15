import pyodbc
import re

class DB_Commands:

    def __init__(self):

        self.conn = pyodbc.connect('Driver={SQL Server};'
                                    'Server=NT-03418\SQLEXPRESS;'
                                    'Database=Carlito;'
                                    'Trusted_Connection=yes;')

    def insert_db_nota(self, contato, status, ultima_hora, nota):

        self.contato = contato
        self.status = status
        self.ultima_hora = ultima_hora
        self.nota = nota


        cursor = self.conn.cursor()

        cursor.execute(
                       '''
                       INSERT INTO Carlito_Teste.dbo.conversas(contato, status, nota, ultima_hora) VALUES (?, ?, ?, ?); 
                       ''',
                       self.contato, self.status, self.nota, self.ultima_hora
                      )
        cursor.commit()


    def insert_db_chamado(self, contato, status, ultima_hora, chamado):

        self.contato = contato
        self.status = status
        self.ultima_hora = ultima_hora
        self.chamado = chamado



        cursor = self.conn.cursor()

        cursor.execute(
                       '''
                       INSERT INTO Carlito_Teste.dbo.conversas(contato, status, chamado, ultima_hora) VALUES (?, ?, ?, ?); 
                       ''',
                       self.contato, self.status, self.chamado, self.ultima_hora
                      )
        cursor.commit()

    def select_table(self, status):

        if len(status) > 3:

            self.status_table = status + '%'
            self.statusarray = []
            self.statusarray.append(self.status_table)



            cursor = self.conn.cursor()

            self.query_table = 'SELECT nome_tabela FROM Carlito_Teste.dbo.assunto WHERE status like ?'


            cursor.execute(self.query_table, [(self.statusarray[0][0:4])])
            row = cursor.fetchone()

            if row:

                self.table = str(row)
                tamanho = len(self.table)
                self.table = self.table[2:tamanho-4]
                return self.table


            else:
                print('tabela inválida')

        else:
            self.table = 'dialogos'
            return self.table


    def select_response(self, status, table):

        cursor = self.conn.cursor()
        self.query_answer = 'SELECT resposta, final FROM Carlito_Teste.dbo.'+table+' WHERE status = ?'




        cursor.execute(self.query_answer, [(status)])
        row = cursor.fetchone()
        if row:
            return row
        else:
            return 'invalida', status
