import matplotlib.pyplot as plt
import numpy as np


def grafico_cstr(CA, X):
    """
    Gera um gráfico combinado para reatores CSTR em série.

    O gráfico apresenta:
    - concentração em barras;
    - conversão em linha;
    - dois eixos y independentes.

    Parâmetros
    ----------
    CA : ndarray
        Vetor contendo as concentrações de saída.

    X : ndarray
        Vetor contendo as conversões acumuladas.
    """

    # ------------------------------------------------------
    # Estágios
    # ------------------------------------------------------

    estagios = np.arange(1, len(CA) + 1)

    # ------------------------------------------------------
    # Figura principal
    # ------------------------------------------------------

    fig, ax1 = plt.subplots(figsize=(8, 5))

    # ------------------------------------------------------
    # Eixo 1 -> Concentração
    # ------------------------------------------------------

    barras = ax1.bar(
        estagios,
        CA,
        alpha=0.7
    )

    ax1.set_xlabel("Estágio")

    ax1.set_ylabel(
        r"Concentração $C_A$"
    )

    ax1.set_title("CSTRs em Série")

    ax1.grid(True, axis='y')

    # Valores nas barras
    for barra in barras:

        altura = barra.get_height()

        ax1.text(
            barra.get_x() + barra.get_width()/2,
            altura,
            f"{altura:.2f}",
            ha='center',
            va='bottom'
        )

    # ------------------------------------------------------
    # Eixo 2 -> Conversão
    # ------------------------------------------------------

    ax2 = ax1.twinx()

    ax2.plot(
        estagios,
        100 * X,
        marker='o',
        linewidth=2,
        color='red'
    )

    # Deixa o eixo da conversão vermelho
    ax2.set_ylabel(
        "Conversão (%)",
        color='red'
    )

    ax2.tick_params(
        axis='y',
        colors='red'
    )

    # Valores nos pontos
    for x, y in zip(estagios, 100 * X):

        ax2.text(
            x,
            y,
            f"{y:.1f}%",
            ha='center',
            va='bottom',
            color='red'
        )

    # ------------------------------------------------------
    # Ajuste final
    # ------------------------------------------------------

    plt.tight_layout()

    plt.show()
