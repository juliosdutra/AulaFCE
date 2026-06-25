# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 08:22:58 2026

@author: Julio Dutra
"""

# Importar as bibliotecas 
import numpy as  np
import matplotlib.pyplot as plt
import streamlit as st

# Configurar a aplicação
st.set_page_config(
    page_title="Calculadora PVT",
    page_icon="🧪",
    layout="wide")

# Constantes do problema
R = 0.08314 # Constante dos gases
gases = {
        "CO2": {"a": 3.592, "b": 0.04267},
        "N2" : {"a": 1.390, "b": 0.03913},
        "CH4": {"a": 2.253, "b": 0.04278}
        }

# Interface
st.title("Calculadora PVT")
st.caption("Equação de Estado de van der Waals")

# Barra lateral
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    
    gas = st.selectbox(
        "Escolha o gás",
        list(gases.keys()))
    
    T = st.number_input(
        "Temperatura (K)",
        min_value=200.0,
        max_value=1000.0,
        value = 350.0,
        step=10.0)
    
    V = st.number_input(
        "Volume molar (L/mol)",
        min_value = 0.01,
        max_value = 3.0,
        value = 0.3,
        step = 0.01,
        format = "%.3f")
    
    calcular = st.button('Calcular')
    
    st.divider()
    st.caption('Desenvolvido por Julio Dutra')
    st.caption('julio.dutra@ufes.br')

# Página principal: resultados!!

# Identificando os parametros da equação de estado
a = gases[gas]["a"]
b = gases[gas]["b"]

# Dividindo em duas colunas
col1, col2 = st.columns([1,2])

if calcular:
    
    if V<=b:
        st.error(
            f"O volume molar deve ser maior que b = {b:.5f} L/mol"
            )
    else:
        # Equação de van der Waals
        P = R*T/(V-b) - a/V**2
        
        with col1:
            with st.container(border=True):
                st.subheader("Resultado")
                st.metric(
                    "Pressão",
                    f"{P:.2f} bar"
                    )
                st.caption(
                    f"Gás:{gas}"
                    )
                st.caption(
                    f"T:{T:.1f} K"
                    )
                st.caption(
                    f"V:{V:.3f} L/mol"
                    )
        
        with col2:
            volumes = np.linspace(0.1, 2.0, 100)
            Pvdw = R*T/(volumes-b) - a/volumes**2
            Pideal = R*T/volumes
            
            fig, ax = plt.subplots(figsize=(5,3.5))
            ax.plot(volumes, Pvdw,
                    label ='van der Waals', linewidth=2)
            ax.plot(volumes, Pideal,
                    label ='Gás ideal', linewidth=2)
            ax.scatter(V, P,
                       color="red", s=60, zorder=5)
            
            ax.set_xlim(0.1, 2.0)
            ax.set_ylim(bottom=0)            
            ax.set_xlabel("Volume molar (L/mol)")
            ax.set_ylabel("Pressão (bar)")
            ax.set_title(f"{gas} T = {T:.1f} K")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
            
            st.info(
                f" a = {a:.3f} |  b = {b:.5f}"
                )
            st.latex(
                r"P = \frac{R T}{V-b} - \frac{a}{V^2}"
                )
            
            
        









