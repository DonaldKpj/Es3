import numpy as np
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key):
        self.d = None
        self.pi = None
        self.f = None
        self.key = key
        self.color = "white"
        self.next = None

    def get_data(self):
        return self.key

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.key = new_data

    def set_next(self, new_next):
        self.next = new_next


class LinkedList:
    def __init__(self):
        self.head = None

    def search(self, item):
        current = self.head
        found = False
        while current and (not found):
            if current.get_data() == item:
                found = True
                break
            else:
                current = current.get_next()
        return found

    def add(self, item):
        tmp = Node(key=item)
        tmp.set_next(self.head)
        self.head = tmp

    def printL(self):
        current = self.head
        while current.get_next():
            print(" -> ", current.key)
            current = current.get_next()

        print(" -> ", current.get_data(), " Questa è la radice della componente.")


class Graph:
    def __init__(self, size, prob):
        self.time = 0
        self.vect = []
        self.Matrix = self.Grafo_Probabilizzato(size, prob)
        # self.Matrix = np.random.randint(1, size=(size, size))
        self.size = size
        self.radice = None
        self.limite = 0

    def Crea_Graph(self):
        for i in range(0, self.size):
            self.vect.append(Node(key=i))
        # for row in self.Matrix:
        #     print(row)

    def Grafo_Probabilizzato(self, size, prob):
        m = np.random.randint(10, size=(size, size))
        for x in range(0, size):
            for y in range(0, size):
                if m[x][y] < prob / 10:
                    m[x][y] = 1
                else:
                    m[x][y] = 0
        return m

    def dfs(self):
        for x in range(0, len(self.vect)):
            if self.vect[x].color == "white":
                self.dfs_visit(self.vect[x])

    def dfs_visit(self, u):
        self.time += 1
        u.d = self.time
        u.color = "Grey"
        for x in range(0, self.size):
            if self.Matrix[u.key][x] != 0:
                if self.vect[x].color == "white":
                    self.vect[x].pi = u.key
                    self.dfs_visit(self.vect[x])
        u.color = "Black"
        self.time += 1
        u.f = self.time

    def stampa(self, n):
        for x in range(0, n):
            print("Colore:", self.vect[x].color, " Tempo iniziale:", self.vect[x].d, " Tempo finale:", self.vect[x].f,
                  " Padre:", self.vect[x].pi, " Chiave:",
                  self.vect[x].key)

    def transpose(self):
        self.Matrix = np.transpose(self.Matrix)
        # for row in self.Matrix:
        #     print(row)

    def ordina(self):
        ordinato = []
        while self.vect:
            max = self.vect[0].f
            i = 0
            for x in range(0, len(self.vect)):
                if self.vect[x].f > max:
                    i = x
                    max = self.vect[x].f
            # print(self.vect[i].f)

            ordinato.append(Node(key=self.vect[i].key))
            self.vect.remove(self.vect[i])
        self.vect.clear()
        self.vect = ordinato
        self.time = 0

    def stamp(self):
        for x in range(0, len(self.vect)):
            o=0
            # print(self.vect[x].f, " --> ", self.vect[x].key)

    def numero_scc(self):
        count = 0
        for x in range(0, len(self.vect)):
            if self.vect[x].pi is None:
                count += 1
        #print(count)
        return count

    def trovaComponenti(self):
        i = -1
        self.vect.sort(key=lambda x: x.d)
        A = np.empty([self.numero_scc(), ], dtype=list)
        for j in range(0, A.size):
            A[j] = LinkedList()
        for element in self.vect:
            if element.pi is None:
                i += 1
                A[i] = LinkedList()
                A[i].add(element.key)
            else:
                if A[i].search(element.pi) is True:
                    A[i].add(element.key)
        for j in range(0, A.size):
            o = 0
            # print("Componente:", j + 1, "°")
            # A[j].printL()


def main():
    prob = 30

    f = open('DimensioneCrescente.txt', 'w')
    f.write('Dimensione ')
    f.write(' SCC\n')

    g = open('ProbCrescente.txt', 'w')
    g.write('ProbabilitàCrescente\n')
    g.write('Probabilità ')
    g.write(' SCC\n')

    numerocomp = []
    
    for n in range(1, 100):
        tot = 0
        for j in range(1, 30):
            grafo = Graph(n, prob)
            grafo.Crea_Graph()
            #grafo.stampa(n)
            grafo.dfs()
            #print("Dopo dfs:")
            # grafo.stampa(n)
            grafo.transpose()
            # grafo.stamp()
            grafo.ordina()
            # grafo.stampa(n)
            # grafo.stamp()
            grafo.dfs()
            # grafo.stampa(n)
            num = grafo.numero_scc()
            tot = tot + num
            #print("Il numero di componenti fortemente connesse è: ", num)
            grafo.trovaComponenti()
        numerocomp.insert(n, tot / j)
        if n % 2 & n % 3:
            f.write(str(n))
            f.write(' & ')
            f.write(str(round(tot / j, 4)))
            f.write(' \\\ \hline\n')
    x = np.arange(1, 100, 1)
    plt.plot(x, numerocomp, label="Probabilità fissata dimensione cresscente")
    plt.savefig('DimensioneCrescente.png', bbox_inches='tight')
    plt.close()

    n = 100
    numerocomp = []
    for prob in range(0, 105, 5): #0 100 5
    #for prob in np.arange(0, 1.05, 0.05):
        tot = 0
        for j in range(1, 30): #30
            grafo = Graph(n, prob)
            grafo.Crea_Graph()
            # grafo.stampa(n)
            grafo.dfs()
            #print("Dopo dfs:")
            # grafo.stampa(n)
            grafo.transpose()
            # grafo.stamp()
            grafo.ordina()
            # grafo.stampa(n)
            # grafo.stamp()
            grafo.dfs()
            # grafo.stampa(n)
            num = grafo.numero_scc()
            tot = tot + num
            #print("Il numero di componenti fortemente connesse è: ", num)
            grafo.trovaComponenti()
        numerocomp.insert(int(prob), tot / j)
        g.write(str(prob))
        g.write(' &  ')
        g.write(str(round(tot / j, 4)))
        g.write(' \\\ \hline\n')

    x = np.arange(0, 105, 5) #0 0.2 0.01
    plt.plot(x, numerocomp, label="Dimensione fissata, probabilità di archi crescente")
    plt.savefig('ProbCrescente.png', bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
