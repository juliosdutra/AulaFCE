from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp


@dataclass
class ParametrosBioreator:
    """
    # Parâmetros do Biorreator

    Armazena os parâmetros do modelo de Michaelis-Menten
    com dependência de temperatura via Arrhenius.

    ## Atributos

    - **Vmax_ref**: velocidade máxima de referência.
    - **Km**: constante de Michaelis-Menten.
    - **Ea**: energia de ativação.
    - **R**: constante universal dos gases.
    - **Tref**: temperatura de referência.
    """

    Vmax_ref: float = 5.0      # mg/L.h
    Km: float = 20.0           # mg/L
    Ea: float = 30000.0        # J/mol
    R: float = 8.314           # J/(mol.K)
    Tref: float = 298.15       # K


def vmax_arrhenius(T, params):
    """
    Calcula a velocidade máxima de consumo (Vmax)
    utilizando a equação de Arrhenius.

    Parameters
    ----------
    T : float
        Temperatura em graus Celsius.
    params : ParametrosBioreator
        Parâmetros do modelo.

    Returns
    -------
    float
        Valor de Vmax para a temperatura especificada.
    """

    Tk = T + 273.15

    vmax = params.Vmax_ref * np.exp(
        -params.Ea / params.R
        * (1 / Tk - 1 / params.Tref)
    )

    return vmax


def bioreator_modelo(t, S, T, params):
    """
    Define a EDO do consumo de substrato segundo
    a cinética de Michaelis-Menten.

    Parameters
    ----------
    t : float
        Tempo de integração (não utilizado explicitamente).
    S : array_like
        Concentração de substrato.
    T : float
        Temperatura em graus Celsius.
    params : ParametrosBioreator
        Parâmetros do modelo.

    Returns
    -------
    float
        Derivada temporal da concentração.
    """

    S = S[0]

    vmax = vmax_arrhenius(T, params)

    dSdt = -vmax * S / (params.Km + S)

    return [dSdt]


def simula_bioreator(S0, tempo_final, T, params):
    """
    Simula o consumo de substrato em um biorreator.

    Parameters
    ----------
    S0 : float
        Concentração inicial de substrato (mg/L).
    tempo_final : float
        Tempo final de simulação (h).
    T : float
        Temperatura de operação (°C).
    params : ParametrosBioreator
        Parâmetros do modelo.

    Returns
    -------
    tempo : ndarray
        Vetor de tempo.
    concentracao : ndarray
        Perfil temporal da concentração de substrato.
    """

    tempo = np.linspace(0, tempo_final, 100)

    solucao = solve_ivp(
        bioreator_modelo,
        (0, tempo_final),
        [S0],
        args=(T, params),
        t_eval=tempo
    )

    concentracao = solucao.y[0]

    return tempo, concentracao
