# Autor: Felipe Rosa Borges de Morais            DATA de início: 24/08
# frbmoraisaero@gmail.com                        DATA de término: 29/08
# Entusiasta da programação - Estudante de Engenharia Aeronáutica
#

import random
import sqlite3


def criatabela():
    conn = sqlite3.connect('card.s3db')  # conectando
    cursor = conn.cursor()  # definindo um cursor
    # cria a tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );
    """)


def verifica_luhn(a):
    a = str(a)
    lista = list(a)
    lista = [int(a) for a in lista]
    for i in range(len(lista)):
        if i % 2 == 0:
            lista[i] *= 2
    lista = [a - 9 if a > 9 else a for a in lista]
    control_number = sum(lista)
    if control_number % 10 == 0:
        return False
    else:
        return True


criatabela()


class Tabela:
    def __init__(self, idd, an, pin, balance):
        self.idd = int(idd)
        self.an = str(an)
        self.pin = str(pin)
        self.balance = int(balance)

    @staticmethod
    def criandotabela():
        conn = sqlite3.connect('card.s3db')  # conectando
        cursor = conn.cursor()  # definindo um cursor
        # cria a tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS card(
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
        );
        """)

        conn.close()

    def apaga_conta(self):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM card WHERE number = ?', (self.an, ))
        conn.commit()
        conn.close()

    @staticmethod
    def verifica():
        conn = sqlite3.connect('card.s3db')  # conectando
        cursor = conn.cursor()  # definindo um cursor
        cursor.execute("SELECT number FROM card")
        records = cursor.fetchall()
        contas = list(records)

        conn.close()
        return contas

    def select(self):
        conn = sqlite3.connect('card.s3db')  # conectando
        cursor = conn.cursor()  # definindo um cursor
        cursor.execute("SELECT * FROM card WHERE number = (?) AND pin = (?)", (self.an, self.pin))
        records = cursor.fetchall()
        for linha in records:
            self.idd = linha[0]
            self.an = linha[1]
            self.pin = linha[2]
            self.balance = linha[3]

        conn.close()

    def add_income(self, adicional):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        cursor.execute("UPDATE card SET balance = ? WHERE id = ?", (self.balance + adicional, self.idd))
        conn.commit()
        conn.close()

    @staticmethod
    def add_income_other_account(adicional, ann):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM card WHERE number = ?", (ann, ))
        records = cursor.fetchall()
        balance_before = None
        for linha in records:
            balance_before = linha[0]

        cursor.execute("UPDATE card SET balance = ? WHERE number = ?", (balance_before + adicional, ann))
        conn.commit()
        conn.close()

    def inserir(self):
        conn = sqlite3.connect('card.s3db')  # conectando
        cursor = conn.cursor()  # definindo um cursor
        cursor.execute("""
        INSERT INTO card (id, number, pin, balance)
        VALUES (?, ?, ?, ?)""", (self.idd, self.an, self.pin, self.balance))

        conn.commit()
        conn.close()

    @staticmethod
    def printa_tabela():
        conn = sqlite3.connect('card.s3db')
        cursor = conn.execute("SELECT id, number, pin, balance from card")

        print("Tabela card")
        print(f"id - {' ' * 3}number - {' ' * 10}pin - {' ' * 3}balance")
        for linha in cursor:
            print(f'{linha[0]}{" "*7}{linha[1]}{" "*5}{linha[2]}{" "*5}{linha[3]}')
        conn.close()


class Display:  # Esta classe contém as interfaces que serão apresentadas ao usuário
    def __init__(self):
        pass

    @staticmethod
    def dp1():
        return '1. Criar conta\n2. Log in\n0. Sair'

    @staticmethod
    def dp2(ann, pinpin):
        return f'\nSeu cartão foi criado\nNúmero do seu cartão:\n{ann}\nSua senha:\n{pinpin}\n'

    @staticmethod
    def dp3():
        print(f'\nInsira o número do seu cartão:')

    @staticmethod
    def dp4():
        print(f'Insira sua senha')

    @staticmethod
    def dp5():
        print(f'\nLog in efetuado com sucesso\n')

    @staticmethod
    def dp6():
        print(f'\nNúmero do cartão ou senha incorretos\n')

    @staticmethod
    def dp7():
        print(f'1. Saldo\n2. Depósito\n3. Trasnferência\n4. Fechar conta\n5. Log out\n0. Sair')

    @staticmethod
    def dp8(balanco):
        print(f'\nSaldo {balanco}\n')

    @staticmethod
    def dp9():
        print(f'\nLog out efetuado com sucesso!\n')

    @staticmethod
    def dp10():
        print(f'Bye!')

    @staticmethod
    def dp11():
        print('Valor a depositar:')

    @staticmethod
    def dp12():
        print('Depósito efetuado com sucesso')

    @staticmethod
    def dp13():
        print('Transferência\nInsira o número do seu cartão:')

    @staticmethod
    def dp14():
        print('Insira a quantidade de dinheiro que deseja transferir:')

    @staticmethod
    def dp15():
        print('Dinheiro insuficiente!\n')

    @staticmethod
    def dp16():
        print('Operação realizada com sucesso!\n')

    @staticmethod
    def dp17():
        print('A conta foi excluida!\n')

    @staticmethod
    def dp18():
        print('Este cartão não existe.\n')

    @staticmethod
    def dp19():
        print('Provavelmente o número inserido do cartão está incorreto. Digite novamente\n')


class Account:  # conta, número de pin e balanço do usuário são armazenados nesta classe
    def __init__(self, an=0, pin=0, balance=0, idd=1):
        self.an = an
        self.pin = pin
        self.balance = balance
        self.idd = idd

    def generatean(self):  # Gera um número de cartão aleatório para o usuário seguindo o algoritmo de LUHN
        random.seed()
        self.an = str(400000) + \
                str(random.randrange(100, 999)) + \
                str(random.randrange(100, 999)) + \
                str(random.randrange(100, 999))  # O número gerado consiste de 12 números aleatórios
        lista = list(self.an)
        # lista = [4, 0, 0, 0, 0, 0, 8, 4, 4, 9, 4, 3, 3, 4, 0]
        # Control number -- LUHN algoritmo
        # ---------------------------
        lista = [int(a) for a in lista]
        for i in range(len(lista)):
            if i % 2 == 0:
                lista[i] *= 2
        lista = [a - 9 if a > 9 else a for a in lista]
        control_number = sum(lista)
        # Checkdigit number
        # -------------------------------
        for checkdigit in range(10):
            control_number += checkdigit
            if control_number % 10 == 0:
                lista.append(checkdigit)
                break
            control_number -= checkdigit

        self.an = self.an + str(lista[-1])
        self.an = int(self.an)

    def generatepin(self):  # Gera um número de pin aleatório para o usuário entre 1000 e 9999
        random.seed()
        self.pin = random.randrange(1000, 9999)


def validacao(numero, pin, objetoan, objetopin):
    if numero == objetoan and pin == objetopin:
        return True
    else:
        return False


def criaobjetoconta(contador):
    conta = Account()
    conta.generatean()
    conta.generatepin()
    conta.idd += contador
    return conta


def funcionamento():
    a = 1
    while a == 1 or a == 2:

        disp = Display()
        print(disp.dp1())

        a = int(input())  # Entrada do usuário

        if a == 1:
            conn = sqlite3.connect('card.s3db')
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM card')
            ultimoid = len(list(cursor))
            x = ultimoid
            conta = criaobjetoconta(x)
            x += 1
            tabela = Tabela(conta.idd, conta.an, conta.pin, conta.balance)  # cria objeto tabela
            tabela.inserir()  # inseri os dados na tabela
            # tabela.printa_tabela()  # mostra a tabela
            print(disp.dp2(conta.an, conta.pin))

        elif a == 2:
            disp.dp3()
            ent_an = int(input())
            disp.dp4()
            ent_pin = int(input())

            conta_logada = Tabela(0, ent_an, ent_pin, 0)
            conta_logada.select()

            if conta_logada.idd != 0:
                valid = True
            else:
                valid = False

            if valid:
                disp.dp5()  # Logado com sucesso

                while valid:  # LOOP de quando ocliente está logado na conta
                    disp.dp7()

                    a = int(input())

                    if a == 1:  # Mostra o saldo da conta
                        conta_logada.select()
                        disp.dp8(conta_logada.balance)
                    elif a == 2:  # Faz depósito no saldo da conta
                        disp.dp11()
                        valor = int(input())
                        conta_logada.select()
                        conta_logada.add_income(valor)
                        disp.dp12()
                    elif a == 3:  # Faz trsnferência de uma conta para outra
                        disp.dp13()
                        conta_a_transf = str(input())
                        contas = conta_logada.verifica()
                        while verifica_luhn(conta_a_transf):
                            disp.dp19()
                            conta_a_transf = str(input())
                            contas = conta_logada.verifica()
                        if (conta_a_transf, ) in contas:
                            disp.dp14()
                            money_to_transfer = int(input())
                            conta_logada.select()
                            if conta_logada.balance >= money_to_transfer:
                                conta_logada.add_income(-money_to_transfer)
                                conta_logada.add_income_other_account(money_to_transfer, conta_a_transf)
                                disp.dp16()
                            else:
                                disp.dp15()
                        else:
                            disp.dp18()
                    elif a == 4:  # Close account
                        disp.dp17()
                        conta_logada.apaga_conta()
                        valid = False
                        a = 1
                    elif a == 5:
                        disp.dp9()
                        valid = False
                        a = 1
                    elif a == 0:
                        valid = False
                        a = 0
            else:
                disp.dp6()  # Não logado
        else:
            disp.dp10()

funcionamento()