
import sys
from threading import Thread
from pandas import DataFrame
from .Loto import ExportLoteriaBase
# from .Volante import Volantes
from .Apurar import Apostas

import warnings
warnings.filterwarnings('ignore')

class srcThread(Thread):
    '''
    Executa dados via Thread sem misturar valores externos
    '''

    def __init__(self, thNdx=-1, loteriaBase=ExportLoteriaBase(), concurso=0, callProcess=None, autoStart=False):
        Thread.__init__(self)
        self.index = thNdx
        self.lb = loteriaBase
        self.lb.concurso = concurso
        self.stop = False
        self.callProcess = callProcess

        if autoStart and (thNdx >= 0):
            self.start()

    def run(self) -> None:
        while not self.stop:
            if not self.stop and self.callProcess:
                self.stop = self.callProcess(self)


class Collection:
    def __init__(self, loteriaBase=ExportLoteriaBase, maxThreads=8, concursoStart=1, verbose=False, autoStart=False):
        self.buffer = []

        self.__repescar = []
        self.__th = []
        self.__lb = loteriaBase
        self.__concursoStart = concursoStart

        if concursoStart < 1:
            self.__concursoStart = 1

        self.__concursoAtual = self.__concursoStart
        self.__thMax = 0

        #Soma individual de sorteios
        self.contagem = [0 for s in range(0, self.__lb().volante.dezenas)]

        self.verbose = verbose

        lb = loteriaBase()
        self.__concursoMax = lb.numero()

        self.maxThreads = maxThreads

        self.apostas = Apostas(self)  # Volantes(self)

        if autoStart:
            self.start()

    @property
    def jogo(self):
        return self.__lb().jogo

    @property
    def __verbose(self):
        pass

    @__verbose.setter
    def __verbose(self, v):
        if self.verbose:
            sys.stdout.write('\r' + v)
            sys.stdout.flush()

    @property
    def sorteioInicial(self):
        return self.__concursoStart

    @sorteioInicial.setter
    def sorteioInicial(self, v):
        self.__concursoStart = v
        if self.__concursoAtual < v:
            self.__concursoAtual = v

            # Reposiciona todas as threads
            for th in self.__th:
                th.lb.concurso = self.__concursoAtual
                self.__concursoAtual += 1

            #Reseta o buffer de dados
            self.buffer = []

    @property
    def sorteioFinal(self):
        return self.__concursoMax

    @sorteioFinal.setter
    def sorteioFinal(self, v):
        if v > self.__concursoStart:
            self.__concursoMax = v

            if self.__concursoAtual > v:
                self.__concursoAtual = v

            #Reseta o buffer
            self.buffer = []

    @property
    def maxThreads(self):
        return self.__thMax

    @maxThreads.setter
    def maxThreads(self, v):
        if (self.__thMax != v) and (v > 1):
            self.__thMax = v
            self.__dumpThreads()

    def __dumpThreads(self):

        # Encerra todas as Threads anteriores, se houver
        for th in self.__th:
            th.stop = True

        # Reseta a lista de threads
        self.__th = []

        # Instancia todas as threads
        for i in range(0, self.__thMax):
            self.__th.append(srcThread(thNdx=i, loteriaBase=self.__lb(), concurso=self.__concursoAtual,
                                       callProcess=self.__callProcess, autoStart=False))

            if self.verbose:
                __verbose = f'Iniciar thread {i} Concurso {self.__concursoAtual}'
                print(__verbose)

            self.__concursoAtual += 1

    def __callProcess(self, th) -> bool:

        th.lb.todosDados()

        self.__verbose = f'Processar thread {th.index} Sorteio {th.lb.concurso} / Atual: {self.__concursoAtual}'

        # Verifica, não houve erro
        if th.lb.error.id == 0:
            sorteios = th.lb.listaDezenas()
            sorteios = [int(s) for s in sorteios]

            toSave = {
                'concurso': th.lb.numero(),
                'dezenas': sorteios,
                'sorteio': th.lb.dezenasNomeadas(),
                'hash': th.lb.hash(),
            }

            #Carrega a lista de dezenas de forma nomeada
            sorteios = th.lb.dezenasNomeadas()
            [toSave.update(srt) for srt in sorteios]

            #[toSave.update(s) for s in sorteios]

            self.buffer.append(toSave)

        else:
            self.__repescar.append(self.__concursoAtual)
            self.__verbose = f'Falha na pesquisa. Inclusão na repescagem {self.__concursoAtual}'

        # Verifica se chegou ao máximo
        r = (self.__concursoAtual + 1) > self.__concursoMax

        if not r:
            self.__concursoAtual += 1
            th.lb.concurso = self.__concursoAtual

        return r

    def start(self):
        '''
        Inicia todas as threads
        '''
        for th in self.__th:
            th.start()

    def wait(self):
        '''
        Aguarda conclusão das threads
        '''

        def doStop() -> bool:
            r = True
            for th in self.__th:
                r = r and th.stop
            return r

        meStop = False
        while not meStop:
            meStop = doStop()

        self.__doMakeCount()

        print('')

    def __doMakeCount(self):
        #Executa a contagem - precisa ser incluído no final de todos os processos, pois a busca é feita em thread
        bloco = DataFrame(self.buffer).sort_values(by='concurso')

        contagem_soma = [0 for s in range(0, self.__lb().volante.dezenas)]
        contagem_individual = [0 for s in range(0, self.__lb().volante.dezenas)]

        dezenas = list(bloco['dezenas'])

        soma = []
        contagem = []


        #Diferença entre o sorteio atual e o anterior
        diferenciacao = []

        firstDiferenciacao = True

        for dzn in dezenas:
            contagem_individual = [0 for s in range(0, self.__lb().volante.dezenas)]
            for dz in dzn:
                contagem_soma[dz] += 1
                contagem_individual[dz] += 1
            soma.append(list(contagem_soma))
            contagem.append(contagem_individual)

            #Primeira vez que a diferenciacao está sendo feita,
            #Nãm tem registro anterior para substrair contagem
            """
            if firstDiferenciacao:
                diferenciacao.append(list(contagem))
            else:
                diferencial = [0 for s in range(0, self.__lb().volante.dezenas)]
                for i in range(0, len(contagem)):
                    diferencial[i]
            """

        bloco['soma'] = soma
        bloco['contagem'] = contagem

        self.buffer = bloco


    def startAndWait(self):
        self.__verbose = 'Preparar threads'
        self.start()
        self.__verbose = 'Iniciar pesquisa'
        self.wait()

    @property
    def values(self) -> DataFrame:
        if len(self.buffer) == 0:
            self.startAndWait()
        return self.buffer
        #df = DataFrame(self.buffer)
        #return df.sort_values(by='concurso')
