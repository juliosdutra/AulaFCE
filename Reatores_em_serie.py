from dataclasses import dataclass
import numpy as np


@dataclass
class ParametrosCSTR:
    """
    Classe que armazena os parâmetros de um reator CSTR.

    Atributos
    ---------
    vazao : float
        Vazão volumétrica de alimentação [unid. volume/tempo].

    volume : float
        Volume do reator [unid. volume].

    constante : float
        Constante cinética de reação de primeira ordem [1/tempo].
    """

    vazao: float = 50.0
    volume: float = 100.0
    constante: float = 0.5


def modelo_cstr(CAin, params):
    """
    Calcula a concentração de saída de um CSTR em regime permanente.

    O modelo considera:
    - mistura perfeita;
    - regime estacionário;
    - reação de primeira ordem.

    Equação:
        CA = (F / (F + V*k)) * CAin

    Parâmetros
    ----------
    CAin : float
        Concentração de entrada do componente A.

    params : ParametrosCSTR
        Objeto contendo os parâmetros do reator.

    Retorna
    -------
    CA : float
        Concentração de saída do componente A.
    """

    F = params.vazao
    V = params.volume
    k = params.constante

    CA = F / (F + V * k) * CAin

    return CA


def simula_cstr(CA0=1.0, num_estagios=3, params=None):
    """
    Simula uma série de reatores CSTR em cascata.

    Cada estágio recebe como entrada a concentração de saída
    do estágio anterior.

    Parâmetros
    ----------
    CA0 : float, opcional
        Concentração inicial de alimentação do primeiro reator.

    num_estagios : int, opcional
        Número de reatores CSTR em série.

    params : list[ParametrosCSTR], opcional
        Lista contendo os parâmetros de cada estágio.
        Caso não seja fornecida, todos os estágios utilizarão
        parâmetros padrão.

    Retorna
    -------
    CA : ndarray
        Vetor contendo as concentrações de saída de cada estágio.

    X : ndarray
        Vetor contendo as conversões acumuladas em cada estágio.
    """

    if params is None:
        params = [ParametrosCSTR() for _ in range(num_estagios)]

    CAin = CA0

    CA = np.zeros(num_estagios)
    X = np.zeros(num_estagios)

    for j in range(num_estagios):

        CA[j] = modelo_cstr(CAin, params[j])

        X[j] = (CA0 - CA[j]) / CA0

        CAin = CA[j]

    return CA, X
