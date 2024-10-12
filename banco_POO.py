from abc import ABC, abstractmethod
from datetime import datetime

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 2000
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
    
    @property
    def saldo(self):
      return self._saldo

    @property
    def numero(self):
      return self._numero

    @property
    def agencia(self):
      return self._agencia

    @property
    def cliente(self):
      return self._cliente

    @property
    def historico(self):
      return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
      return cls(numero, cliente)
    
    def sacar(self, valor):
      saldo = self.saldo

      if valor > saldo:
        print("Não foi possível sacar este valor pois não há saldo suficiente.")

      elif valor > 0:
        self._saldo -= valor
        print("Saque realizado com sucesso!")
        return True

      else:
        print("A operação não foi bem sucedida. O valor digitado é inválido!")

      return False

    def depositar(self, valor):
      pass


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
      super().__init__(numero, cliente)
      self.limite = limite
      self. limite_saques = limite_saques

    def sacar(self, valor):
      numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

      excedeu_limite = valor > self.limite
      excedeu_saques = numero_saques >= self.limite_saques

      if excedeu_limite:
        print("Não é permitido sacar mais do que R$ 500,00 de uma única vez.")

      elif excedeu_saques:
        print("Você atingiu seu limite diário de saques!")

      else:
        return super().sacar(valor)

      return False
    
    def __str__(self):
      return f"""\
          Agência:\t{self.agencia}
          C/C:\t\t{self.numero}
          Titular:\t{self.cliente.nome}
      """


class Cliente:
    def __init__(self, endereco):
      self.endereco = endereco
      self.contas = []

    def realizar_transacao(self,conta, transacao):
      transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
      self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
      super().__init__(endereco)
      self.cpf = cpf
      self.nome = nome
      self.data_nascimento = data_nascimento
      

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):    
      self.valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
      sucesso_transacao = conta.sacar(self.valor)

      if sucesso_transacao:
        conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
      self.valor = valor

    @property
    def valor(self):
      return self._valor

    def registrar(self, conta):
      sucesso_transacao = conta.sacar(self.valor)

      if sucesso_transacao:
        conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
      self._transacoes = []

    @property
    def transacoes(self):
      return self._transacoes
    
    def adicionar_transacao(self, transacao):
      self._transacoes.append(
        {
          "tipo": transacao.__class__.__name__,
          "valor": transacao.valor,
          "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        }
        )
