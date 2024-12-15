import warnings
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from filtros import *  # Importando a função
from dados import *
warnings.filterwarnings('ignore')

# Configurando o layout
st.set_page_config( layout="wide")


grupos,df,orcamento=carregar()

# CSS para criar o retângulo
st.markdown(
    """
    <style>
    .retangulo-cinza {
        background-color: #D3D3D3; /* Cor cinza */
        height: 100px; /* Altura do retângulo */
        display: flex;
        justify-content: center; /* Centraliza horizontalmente */
        align-items: center; /* Centraliza verticalmente */
        font-size: 36px; /* Tamanho da fonte */
        font-weight: bold; /* Texto em negrito */
        color: #000; /* Cor do texto */
        margin-bottom: 20px; /* Espaço abaixo do retângulo */
        width: 100%; /* Largura total */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Criando a função para cada página
def Gastos():
    st.markdown(
    """
    <div class="retangulo-cinza">
        Gastos Monteiro Reis
    </div>
    """,
    unsafe_allow_html=True
)
    df_filtered = df.copy()
    
    ano_mes_selecionados=criar_filtro_com_multiselect("Filtro de Ano Mês", df_filtered['Ano-Mês'].unique())
    df_filtered = df_filtered[df_filtered["Ano-Mês"].isin(ano_mes_selecionados)]

    grupo_selecionados=criar_filtro_com_selecionar_todos("Filtro de Grupo",df_filtered['Despesa'].unique())
    df_filtered = df_filtered[df_filtered["Despesa"].isin(grupo_selecionados)]
    
    categoria_selecionados =criar_filtro_com_multiselect("Filtro da Categoria", sorted(df_filtered['Destino'].unique()))     
    df_filtered = df_filtered[df_filtered["Destino"].isin(categoria_selecionados)]
    
    df1=df_filtered.groupby(['Ano-Mês','Despesa'])['Valor2'].sum().reset_index()
    df_totais = df1.groupby('Ano-Mês')['Valor2'].sum().reset_index()
    df_totais['Valor2_label'] = df_totais['Valor2'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    valor_maximo = 3000 #max(df_totais['Valor2'])*0.11
    
    fig = px.bar(
        df1,
        x="Ano-Mês",  # Eixo X
        y="Valor2",  # Eixo Y
        color="Despesa",  # Coluna para a legenda
        title="Despesas por Mês e Origem",
        labels={"Ano-Mês": "Mês-Ano", "Valor2": "Total", "Despesa": "Despesa"},
        text="Valor2",
        color_discrete_map={"Monteiro Reis": "#E66C37", "Augusto": "#118DFF", "Valéria": "#CC479B", "Economias e Investimentos": "#1DB3B1"}
    )

    # Configurando rótulos com fonte fixa
    fig.update_traces(
        texttemplate='%{text:.2f}',       # Formatação dos valores
        insidetextanchor='middle',        # Centraliza o texto
        textfont=dict(size=16),           # Define tamanho fixo dos rótulos
        cliponaxis=False                  # Permite exibir rótulos fora do limite
    )

    # Ajuste dinâmico da posição e tamanho do texto com base no tamanho da barra
    fig.for_each_trace(
    lambda trace: trace.update(
        textposition=[
            # Para cada valor da barra (para cada categoria de "Despesa"), se for menor que o valor máximo,
            # movemos o rótulo para fora da barra
            'outside' if v < valor_maximo else 'inside' for v in trace.y  # Ajusta dinamicamente
        ],
        textfont=dict(size=16)
        # A fonte continua fixa para todos os rótulos
        )
    )

    # Adicionando trace adicional com marcadores e texto
    fig.add_trace(
        go.Scatter(
            x=df_totais['Ano-Mês'],
            y=df_totais['Valor2'],
            mode='markers+text',  # Apenas marcadores e texto
            name="Total por Mês",
            marker=dict(size=12, color='#999999', symbol='triangle-up'),  # Estilo dos marcadores
            text=df_totais['Valor2_label'],  # Formatação do texto
            textfont=dict(size=16),  # Define tamanho fixo do texto
            textposition="top center",  # Texto acima do marcador
            hovertemplate="Mês: %{x}<br>Total: R$ %{y:.2f}<extra></extra>"  # Formato do hover
        )
    )

    # Configurando o layout do gráfico
    fig.update_layout(
        title={
            'text': "Despesas por Mês e Origem",  # Título
            'font': {'size': 24},                # Tamanho da fonte do título
            'x': 0.5,                            # Centralizar título
            'xanchor': 'center'                  # Ancorar no centro
        },
        font=dict(size=12),                      # Define tamanho padrão para todos os textos
        yaxis=dict(title="Valor"),              # Rótulo do eixo Y
        xaxis=dict(title="Ano-Mês")             # Rótulo do eixo X
    )

    df2 = df_filtered.groupby('Destino')['Valor2'].sum().reset_index().sort_values(by='Valor2',ascending=False)

    fig2 = px.bar(
        df2,
        x="Destino",  # Eixo X
        y="Valor2",  # Eixo Y
        title="Gasto por categoria",
        labels={"Destino": "Categoria", "Valor2": "Gasto (R$)"},
        text="Valor2"
    )
    fig2.update_traces(marker=dict(color='#6B007B'))
    fig2.update_traces(texttemplate='%{text:.2f}', textposition='inside', insidetextanchor='middle')
    fig2.update_layout(font=dict(size=12))
    fig2.update_layout(
    title={
        'text': "Gastos por Categoria",  # Texto do título
        'font': {'size': 24},  # Tamanho da fonte
        'x': 0.5,  # Centralizando o título
        'xanchor': 'center'  # Garantir que o título esteja centralizado
    }
    )

    df3 = df_filtered.groupby(['Destino','Beneficiário'],dropna=False)['Valor2'].sum().reset_index().sort_values(by='Valor2',ascending=False)
    df3.rename(columns={'Valor2':'Total (R$) 1','Destino':'Categoria'},inplace=True)
    df3['Total (R$)'] = df3['Total (R$) 1'].apply(lambda x: f"{x:,.2f}".replace(',','a').replace('.', ',').replace('a','.'))
    df3['Total (R$) 1'] = df3['Total (R$) 1'].round(2)
    df3=df3.reset_index(drop=True)

    with st.container():
        st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns([1,4])
    with col1:
        st.dataframe(df3[['Categoria', 'Beneficiário', 'Total (R$) 1']])
        
    with col2:
        #st.pyplot(fig_bottom_right)
        st.plotly_chart(fig2, use_container_width=True)


def Orcamento():
    st.markdown(
    """
    <div class="retangulo-cinza">
        Orçamento Mensal
    </div>
    """,
    unsafe_allow_html=True
)
    df_filtered_orcamento = orcamento.copy()
    
    ano_mes_selecionados_orcamento=criar_filtro_com_valor_unico("Filtro de Ano Mês", df_filtered_orcamento['Ano-Mês'].unique())
    df_filtered_orcamento = df_filtered_orcamento[df_filtered_orcamento["Ano-Mês"]==ano_mes_selecionados_orcamento]
    df4 = df_filtered_orcamento.groupby(['Origem','Ano-Mês'],dropna=False)[['Disponivel','total']].sum().reset_index()
    df4['total']=df4['total'].round(2)
    
    fig4 = px.bar(
    df4,
    x="Origem",  # Eixo X
    y="Disponivel",  # Eixo Y
    title="Valor disponível",
    text="Disponivel",  # Exibe o valor diretamente nas barras
)

    # Configurando rótulos com fonte fixa
    fig4.update_traces(
        texttemplate='%{text:.2f}',       # Formatação dos valores
        insidetextanchor='middle',        # Centraliza o texto
        textfont=dict(size=16),           # Define tamanho fixo dos rótulos
        cliponaxis=False                  # Permite exibir rótulos fora do limite
    )

    # Ajuste dinâmico da posição do texto com base no tamanho da barra
    fig4.for_each_trace(
        lambda trace: trace.update(
            textposition=[
                'outside' if v < 20 else 'inside' for v in trace.y  # Ajusta dinamicamente
            ]
        )
    )

    # Adicionando trace adicional com marcadores e texto
    fig4.add_trace(
        go.Scatter(
            x=df4['Origem'],
            y=df4['total'],
            mode='markers+text',  # Apenas marcadores e texto
            name="Total",
            marker=dict(size=12, color='#999999', symbol='triangle-up'),  # Estilo dos marcadores
            text=df4['total'].apply(lambda x: f"R$ {x:,.2f}"),  # Formatação do texto
            textfont=dict(size=16),  # Define tamanho fixo do texto
            textposition="top center",  # Texto acima do marcador
            hovertemplate="Origem: %{x}<br>Total: R$ %{y:.2f}<extra></extra>"  # Formato do hover
        )
    )

    # Configurando o layout do gráfico
    fig4.update_layout(
        title={
            'text': "Valor disponível",  # Título
            'font': {'size': 24},        # Tamanho da fonte do título
            'x': 0.5,                    # Centralizar título
            'xanchor': 'center'          # Ancorar no centro
        },
        font=dict(size=16),              # Define tamanho padrão para todos os textos
        yaxis=dict(title="Disponível"), # Rótulo do eixo Y
        xaxis=dict(title="Origem")      # Rótulo do eixo X
    )

    
    with st.container():
        st.plotly_chart(fig4, use_container_width=True)

        
# Criando a barra lateral para a troca de páginas
pagina_selecionada = st.sidebar.radio(
    "Navegue entre as páginas:",
    ("Gastos", "Orçamento")
)

# Exibindo a página com base na seleção
if pagina_selecionada == "Gastos":
    Gastos()
elif pagina_selecionada == "Orçamento":
    Orcamento()