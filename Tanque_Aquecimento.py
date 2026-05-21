from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp


@dataclass
class ParametrosAquecimento:
    """
    Classe que armazena os parâmetros do tanque aquecido.

    Modelo considerado:
    -------------------
    Tanque perfeitamente misturado aquecido por resistência elétrica.

    Equação do modelo:
    ------------------
    dT/dt = (U*A*(Tamb - T) + q) / (m*Cp)

    Condição nominal utilizada:
    ----------------------------
    - U = 150 W/(m²·°C)
    - A = 5 m²
    - Tamb = 25 °C
    - q = 5000 W
    - m = 50 kg
    - Cp = 1670 J/(kg·°C)
    """

    U: float = 150.0
    A: float = 5.0
    Tamb: float = 25.0
    q: float = 5000.0
    m: float = 50.0
    Cp: float = 1670.0


def modelo_aquecimento(t, T, params):
    """
    Modelo dinâmico do tanque aquecido.

    Parâmetros
    ----------
    t : float
        Tempo [s]

    T : ndarray
        Temperatura do sistema [°C]

    params : ParametrosAquecimento
        Parâmetros do processo.

    Retorna
    -------
    dTdt : list
        Derivada temporal da temperatura.
    """

    U = params.U
    A = params.A
    Tamb = params.Tamb
    q = params.q
    m = params.m
    Cp = params.Cp

    dTdt = (U * A * (Tamb - T[0]) + q) / (m * Cp)

    return [dTdt]


def simula_aquecimento(tempo, T0=25.0, params=None):
    """
    Simula o aquecimento do tanque usando solve_ivp.

    Parâmetros
    ----------
    tempo : ndarray
        Vetor de tempo [s]

    T0 : float, opcional
        Temperatura inicial [°C]

    params : ParametrosAquecimento, opcional
        Parâmetros do sistema.

    Retorna
    -------
    T : ndarray
        Perfil temporal de temperatura.
    """

    if params is None:
        params = ParametrosAquecimento()

    sol = solve_ivp(
        lambda t,T: modelo_aquecimento(t, T, params),
        t_span=(tempo[0], tempo[-1]),
        y0=[T0],
        t_eval=tempo,
        args=(params,),
        method="RK45"
    )

    return sol.t, sol.y[0]
