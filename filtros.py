import streamlit as st

def criar_filtro_com_selecionar_todos(nome_filtro, opcoes):
    """
    Cria um filtro com checkboxes e a funcionalidade "Selecionar Todos" na sidebar.
    
    Args:
        nome_filtro (str): O título do filtro.
        opcoes (list): Lista de opções para os checkboxes.
    
    Returns:
        list: Lista das opções selecionadas.
    """
    st.sidebar.subheader(nome_filtro)

    # Checkbox para "Selecionar Todos" na sidebar
    selecionar_todos = st.sidebar.checkbox("Selecionar todos", value=True, key=f"selecionar_todos_{nome_filtro}")

    # Lista dinâmica para checkboxes individuais na sidebar
    checkbox_estados = {}

    # Controle dinâmico dos checkboxes
    todos_selecionados = True  # Flag para verificar se todos estão selecionados
    for opcao in opcoes:
        # Estado inicial com base no "Selecionar Todos"
        # Quando "Selecionar todos" estiver marcado, as opções também estarão marcadas por padrão
        checkbox_estado = st.sidebar.checkbox(opcao, value=selecionar_todos, key=f"{nome_filtro}_{opcao}")
        checkbox_estados[opcao] = checkbox_estado
        # Atualiza a flag se algum checkbox individual estiver desmarcado
        if not checkbox_estado:
            todos_selecionados = False

    # Retorna as opções selecionadas
    return [opcao for opcao, estado in checkbox_estados.items() if estado]



def criar_filtro_com_multiselect(nome_filtro, opcoes):
    """
    Cria um filtro com multiselect e a funcionalidade "Selecionar Todos".
    
    Args:
        nome_filtro (str): O título do filtro.
        opcoes (list): Lista de opções para o filtro.
    
    Returns:
        list: Lista das opções selecionadas.
    """
    st.sidebar.subheader(nome_filtro)

    # Adiciona a funcionalidade "Selecionar Todos" com valor True por padrão
    selecionar_todos = st.sidebar.checkbox("Selecionar todos", value=True, key=f"selecionar_todos_{nome_filtro}")
    
    if selecionar_todos:
        # Se "Selecionar todos" estiver marcado, todas as opções são pré-selecionadas
        selecionadas = st.sidebar.multiselect(
            f"Selecione as opções do {nome_filtro}:",
            opcoes,
            default=opcoes,  # Seleciona todas as opções
            key=f"multiselect_{nome_filtro}"
        )
    else:
        # Caso contrário, o usuário pode selecionar manualmente
        selecionadas = st.sidebar.multiselect(
            f"Selecione as opções do {nome_filtro}:",
            opcoes,
            default=[],  # Nenhuma pré-selecionada
            key=f"multiselect_{nome_filtro}"
        )
    
    return selecionadas

def criar_filtro_com_valor_unico(nome_filtro, opcoes):
    """
    Cria um filtro no Streamlit que permite selecionar apenas um valor de uma lista.
    
    Args:
        nome_filtro (str): O título do filtro.
        opcoes (list): Lista de opções disponíveis para seleção.
    
    Returns:
        str: A opção selecionada.
    """
    #st.sidebar.subheader(nome_filtro)
    
    # Definindo o primeiro valor como padrão
    valor_selecionado = st.sidebar.radio(nome_filtro, options=opcoes, index=0, key=f"radio_{nome_filtro}")
    
    return valor_selecionado
