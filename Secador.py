# ==========================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ==========================================================

# Classe para armazenamento de parâmetros
from dataclasses import dataclass

# Solver de equações diferenciais
from scipy.integrate import solve_ivp

# Biblioteca numérica
import numpy as np

# Biblioteca de gráficos
import matplotlib.pyplot as plt

# Biblioteca para download no Google Colab
from google.colab import files


# ==========================================================
# CLASSE DE PARÂMETROS
# ==========================================================

@dataclass
class ParametrosSecagem:
    """
    Classe que armazena parâmetros do modelo de secagem.

    Modelo considerado
    ------------------
    Modelo cinético de secagem de primeira ordem:

    dX/dt = -k (X - Xe)

    onde:
    X  : umidade do sólido
    Xe : umidade de equilíbrio
    k  : constante cinética de secagem

    A constante cinética depende da temperatura.
    """

    # Umidade de equilíbrio
    Xe: float = 0.05

    @staticmethod
    def constante(T):
        """
        Calcula a constante cinética de secagem.

        Parâmetros
        ----------
        T : float
            Temperatura de operação [°C]

        Retorno
        -------
        k : float
            Constante cinética [h^-1]
        """

        return 0.2 * (1 + 0.02 * (T - 60))


# ==========================================================
# MODELO MATEMÁTICO
# ==========================================================

def Secagem_modelo(t, X, T, ParametrosSecagem):
    """
    Modelo diferencial de secagem.

    Equação:
        dX/dt = -k (X - Xe)

    Parâmetros
    ----------
    t : float
        Tempo [h]

    X : float
        Umidade do sólido

    T : float
        Temperatura de operação [°C]

    Retorno
    -------
    dXdt : float
        Taxa de variação da umidade
    """

    # Umidade de equilíbrio
    Xe = ParametrosSecagem.Xe

    # Constante cinética
    k = ParametrosSecagem.constante(T)

    # Modelo diferencial
    return -k * (X - Xe)


# ==========================================================
# FUNÇÃO DE SIMULAÇÃO
# ==========================================================

def Simula_Secagem(
    tfinal=5.0,
    X0=0.5,
    T=60.0
):
    """
    Simula o processo de secagem.

    Parâmetros
    ----------
    tfinal : float
        Tempo final da simulação [h]

    X0 : float
        Umidade inicial

    T : float
        Temperatura de operação [°C]

    Retorno
    -------
    t : ndarray
        Vetor de tempo

    X : ndarray
        Perfil de umidade
    """

    # Resolve o sistema diferencial
    sol = solve_ivp(

        # Modelo matemático
        Secagem_modelo,

        # Intervalo de integração
        t_span=(0, tfinal),

        # Condição inicial
        y0=[X0],

        # Argumentos adicionais
        args=(T,ParametrosSecagem),

        # Pontos de avaliação
        t_eval=np.linspace(0, tfinal, 100),

        # Método numérico
        method='BDF'
    )

    return sol.t, sol.y[0]
