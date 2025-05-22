#definindo a estrutura dos processos
class Processo:
    def __init__(self, pid, chegada, duracao, prioridade, tipo):
        self.pid = pid
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.tipo = tipo

        #Outros atributos auxiliares
        self.tempo_restante = duracao
        self.inicio = None
        self.fim = None
        self.tempo_espera = 0
        self.tempo_execucao = 0

    def __repr__(self):
        return f"(PID={self.pid}, chegada={self.chegada}, duracao={self.duracao}, prioridade={self.prioridade}, tipo={self.tipo})"

