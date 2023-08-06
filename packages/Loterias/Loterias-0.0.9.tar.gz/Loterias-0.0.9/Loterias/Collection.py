
import sys
from threading import Thread
#from pandas import DataFrame
import pandas as pd
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

class srcCounter:
    def __init__(self, dezenas=0):
        self.__dezenas = dezenas
        self.soma = []
        self.cont = []

        #Lista para integrar o dicionário final
        self.finalSoma = []
        self.finalCont = []

        self.doMake()

    def doMake(self):
        self.soma = [0 for i in range(0, self.__dezenas)]
        self.cont = [0 for i in range(0, self.__dezenas)]

    def resetCont(self):
        self.cont = [0 for i in range(0, self.__dezenas)]

    def calculate(self, v):
        self.soma[v] += 1
        self.cont[v] += 1

    @property
    def getDict(self):
        soma = {}
        cont = {}

        def __process(i):
            soma.update({f'smDz{i}': self.soma[i]})
            cont.update({f'ctDz{i}': self.cont[i]})

        #for i in range(0, self.__dezenas):
        #    soma.update({f'smDz{i}': self.soma[i]})
        #    cont.update({f'ctDz{i}': self.cont[i]})
        [__process(i) for i in range(0, self.__dezenas)]

        r = {}
        r.update(soma)
        r.update(cont)
        return r

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


    @property
    def showSetup(self):
        print('Jogo             ', self.__lb().jogo)
        print('Dezenas          ', self.__lb().volante.dezenas)
        print('Sorteios         ', self.__lb().volante.sorteio)
        print('Sorteio inicial  ', self.sorteioInicial)
        print('Sorteio final    ', self.sorteioFinal)
        print('Threads          ', self.maxThreads)

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

        self.__verbose = f'Processar thread {th.index} Sorteio {th.lb.concurso} / Atual: {self.__concursoAtual} de {self.__concursoMax}'

        # Verifica, não houve erro
        if th.lb.error.id == 0:
            sorteios = th.lb.listaDezenas()
            sorteios = [int(s) for s in sorteios]

            toSave = {
                'concurso': th.lb.numero(),
                'data': th.lb.dataApuracao(),
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

    def __doMakeCount(self):
        self.__verbose = 'Calcular ocorrências'
        #Executa a contagem - precisa ser incluído no final de todos os processos, pois a busca é feita em thread
        bloco = pd.DataFrame(self.buffer).sort_values(by='concurso')

        counter = srcCounter(self.__lb().volante.dezenas)

        gruposDZ = list(bloco['dezenas'])
        concurso = list(bloco['concurso'])

        dc = []

        #Verifica individualmente cada grupo de dezenas
        for i in range(0, len(gruposDZ)):
            dzn = gruposDZ[i]
            #Reseta contagem individual de valores
            counter.resetCont()

            #Calcula todos os valores de uma vez só [soma e contagem]
            [counter.calculate(dz) for dz in dzn]

            cto = {'concurso': concurso[i]}
            cto.update(counter.getDict)

            dc.append(cto)

        blocCount = pd.DataFrame(dc)

        self.buffer = pd.merge(bloco, blocCount, on='concurso')

        pass
        #bloco['soma'] = soma
        #bloco['contagem'] = contagem

        #self.buffer = bloco


    def startAndWait(self):
        self.__verbose = 'Preparar threads'
        self.start()
        self.__verbose = 'Iniciar pesquisa'
        self.wait()

    @property
    def values(self) -> pd.DataFrame:
        if len(self.buffer) == 0:
            self.startAndWait()
            print('')
        return self.buffer
        #df = DataFrame(self.buffer)
        #return df.sort_values(by='concurso')


    @property
    def volante(self):
        return self.__lb().volante

    @property
    def getDezenas(self):
        dzs = self.__lb().volante.sorteio
        cols = ['concurso', 'data']
        for i in range(1, dzs+1):
            cols.append(f'Dz{i}')

        return self.values[cols]

    @property
    def getSomas(self):
        dzs = self.__lb().volante.dezenas
        cols = ['concurso', 'data']
        for i in range(0, dzs):
            cols.append(f'smDz{i}')

        return self.values[cols]

    @property
    def getContagem(self):
        dzs = self.__lb().volante.dezenas
        cols = ['concurso', 'data']
        for i in range(0, dzs):
            cols.append(f'ctDz{i}')

        return self.values[cols]
