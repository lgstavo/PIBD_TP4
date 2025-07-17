# pip install psycopg2-binary

import psycopg2
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

conn = psycopg2.connect(
    dbname='saude',
    user='postgres',
    password='postgres',
    host='localhost')

class Medicamento:
    def __init__(self, cod_anvisa_med, nome_comercial, fabricante_med, apresentacao_med, forma_administracao_med, principio_ativo_med):
        self.cod_anvisa = cod_anvisa_med
        self.nome_comercial = nome_comercial
        self.fabricante = fabricante_med
        self.apresentacao = apresentacao_med
        self.forma_administracao = forma_administracao_med
        self.principio_ativo = principio_ativo_med

class EstoqueMedicamento:
    def __init__(self, lote_med, cod_anvisa_med, cod_unidade, validade_med_estoque, quantidade_med_estoque):
        self.lote = lote_med
        self.cod_anvisa = cod_anvisa_med
        self.cod_unidade = cod_unidade
        self.validade = validade_med_estoque.strftime("%d/%m/%Y")
        self.quantidade = quantidade_med_estoque

class UnidadeSaude:
    def __init__(self, cod_unidade, nome_unidade, tel_unidade, tipo_unidade, rua_end_unidade, num_end_unidade, bairro_end_unidade, cep_end_unidade):
        self.cod = cod_unidade
        self.nome = nome_unidade
        self.telefone = tel_unidade
        self.cep = cep_end_unidade
        self.rua = rua_end_unidade
        self.numero = num_end_unidade
        self.bairro = bairro_end_unidade
        self.tipo = tipo_unidade


# GET /medicamentos
def get_medicamentos():
    df = pd.read_sql_query(
        'SELECT * FROM medicamento',
        conn)
    medicamentos = df.to_dict(orient='records')
    return [Medicamento(**med) for med in medicamentos]

# POST /medicamentos
def post_medicamento(medicamento: Medicamento):
    query = """
    INSERT INTO medicamento (cod_anvisa_med, nome_comercial, fabricante_med, apresentacao_med, forma_administracao_med, principio_ativo_med)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                medicamento.cod_anvisa,
                medicamento.nome_comercial,
                medicamento.fabricante,
                medicamento.apresentacao,
                medicamento.forma_administracao,
                medicamento.principio_ativo
            ))
        conn.commit()
        return {'status': 'success', 'message': 'Medicamento adicionado com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# GET /medicamentos/<cod_anvisa>
def get_medicamento(cod_anvisa):
    df = pd.read_sql_query(
        'SELECT * FROM medicamento WHERE cod_anvisa_med = %s',
        conn,
        params=(cod_anvisa,))
    if df.empty:
        return None
    medicamento = Medicamento(**df.iloc[0].to_dict())
    return medicamento

# DELETE /medicamentos/<cod_anvisa>
def delete_medicamento(cod_anvisa):
    query = 'DELETE FROM medicamento WHERE cod_anvisa_med = %s'
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (cod_anvisa,))
        conn.commit()
        return {'status': 'success', 'message': 'Medicamento deletado com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}
    
# UPDATE /medicamentos/<cod_anvisa>
def update_medicamento(medicamento: Medicamento):
    query = """
    UPDATE medicamento
    SET nome_comercial = %s, fabricante_med = %s, apresentacao_med = %s, forma_administracao_med = %s, principio_ativo_med = %s
    WHERE cod_anvisa_med = %s
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                medicamento.nome_comercial,
                medicamento.fabricante,
                medicamento.apresentacao,
                medicamento.forma_administracao,
                medicamento.principio_ativo,
                medicamento.cod_anvisa
            ))
        conn.commit()
        return {'status': 'success', 'message': 'Medicamento atualizado com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# GET /unidades
def get_unidades():
    df = pd.read_sql_query(
        'SELECT * FROM unidadesaude',
        conn)
    unidades = df.to_dict(orient='records')
    return [UnidadeSaude(**un) for un in unidades]

# POST /unidades
def post_unidade(unidade: UnidadeSaude):
    query = """
    INSERT INTO unidadesaude (cod_unidade, nome_unidade, tel_unidade, tipo_unidade, rua_end_unidade, num_end_unidade, bairro_end_unidade, cep_end_unidade)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                unidade.cod,
                unidade.nome,
                unidade.telefone,
                unidade.tipo,
                unidade.rua,
                unidade.numero,
                unidade.bairro,
                unidade.cep
            ))
        conn.commit()
        return {'status': 'success', 'message': 'Unidade de saúde adicionada com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# GET /unidades/<cod_unidade>
def get_unidade(cod_unidade):
    df = pd.read_sql_query(
        'SELECT * FROM unidadesaude WHERE cod_unidade = %s',
        conn,
        params=(cod_unidade,))
    if df.empty:
        return None
    
    unidade = UnidadeSaude(**df.iloc[0].to_dict())
    return unidade

# DELETE /unidades/<cod_unidade>
def delete_unidade(cod_unidade):
    query = 'DELETE FROM unidadesaude WHERE cod_unidade = %s'
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (cod_unidade,))
        conn.commit()
        return {'status': 'success', 'message': 'Unidade de saúde deletada com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# UPDATE /unidades/<cod_unidade>
def update_unidade(unidade: UnidadeSaude):
    query = """
    UPDATE unidadesaude
    SET nome_unidade = %s, tel_unidade = %s, tipo_unidade = %s, rua_end_unidade = %s, num_end_unidade = %s, bairro_end_unidade = %s, cep_end_unidade = %s
    WHERE cod_unidade = %s
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                unidade.nome,
                unidade.telefone,
                unidade.tipo,
                unidade.rua,
                unidade.numero,
                unidade.bairro,
                unidade.cep,
                unidade.cod
            ))
        conn.commit()
        return {'status': 'success', 'message': 'Unidade de saúde atualizada com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# GET /unidades/<cod_unidade>/medicamentos
def get_estoque_medicamentos(cod_unidade):
    df = pd.read_sql_query(
        'SELECT * FROM medicamentoestocado WHERE cod_unidade = %s',
        conn,
        params=(cod_unidade,))
    if df.empty:
        return []
    
    estoque = df.to_dict(orient='records')
    return [EstoqueMedicamento(**item) for item in estoque]

# POST /unidades/<cod_unidade>/medicamentos
def post_estoque_medicamento(estoque: EstoqueMedicamento):
    query = """
    INSERT INTO medicamentoestocado (lote_med, cod_anvisa_med, cod_unidade, validade_med_estoque, quantidade_med_estoque)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                estoque.lote,
                estoque.cod_anvisa,
                estoque.cod_unidade,
                estoque.validade,
                estoque.quantidade
            ))
        conn.commit()
        return {'status': 'success', 'message': 'Medicamento adicionado ao estoque com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# GET /unidades/<cod_unidade>/medicamentos/<lote>/<cod_anvisa>
def get_estoque_medicamento(cod_unidade, lote, cod_anvisa):
    df = pd.read_sql_query(
        'SELECT * FROM medicamentoestocado WHERE cod_unidade = %s AND lote_med = %s AND cod_anvisa_med = %s',
        conn,
        params=(cod_unidade, lote, cod_anvisa))
    
    if df.empty:
        return None
    
    estoque = EstoqueMedicamento(**df.iloc[0].to_dict())
    return estoque

# PUT /unidades/<cod_unidade>/medicamentos
def update_estoque_medicamento(estoque: EstoqueMedicamento):
    query = """
    UPDATE medicamentoestocado
    SET quantidade_med_estoque = %s
    WHERE lote_med = %s AND cod_anvisa_med = %s AND cod_unidade = %s
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                estoque.quantidade,
                estoque.lote,
                estoque.cod_anvisa,
                estoque.cod_unidade
            ))
        conn.commit()
        return {'status': 'success', 'message': 'Medicamento no estoque atualizado com sucesso.'}
    except Exception as e:
        conn.rollback()
        return {'status': 'error', 'message': str(e)}

# ==== Functions de renderização
def render_unidades(unidades: list[UnidadeSaude]):
    # Print header
    print(f"{'Código':<10} {'Nome':<30} {'Telefone':<15} {'Tipo':<25} {'Rua':<30} {'Número':<10} {'Bairro':<20} {'CEP':<10}")
    print("="*150)
    # Print each unidade
    for un in unidades:
        print(f"{un.cod:<10} {un.nome:<30} {un.telefone:<15} {un.tipo:<25} {un.rua:<30} {un.numero:<10} {un.bairro:<20} {un.cep:<10}")

def render_medicamentos(medicamentos: list[Medicamento]):
    # Print header
    print(f"{'Código ANVISA':<15} {'Nome Comercial':<30} {'Fabricante':<20} {'Apresentação':<30} {'Forma de Administração':<30} {'Princípio Ativo':<30}")
    print("="*150)
    # Print each medicamento
    for med in medicamentos:
        print(f"{med.cod_anvisa:<15} {med.nome_comercial:<30} {med.fabricante:<20} {med.apresentacao:<30} {med.forma_administracao:<30} {med.principio_ativo:<30}")

def render_estoque_medicamentos(estoque: list[EstoqueMedicamento]):
    # Print header
    print(f"{'Lote':<10} {'Código ANVISA':<15} {'Código Unidade':<15} {'Validade':<15} {'Quantidade':<10}")
    print("="*70)
    # Print each estoque medicamento
    for item in estoque:
        print(f"{item.lote:<10} {item.cod_anvisa:<15} {item.cod_unidade:<15} {item.validade:<15} {item.quantidade:<10}")

# ==== Console menu functions
def menu_unidades_get():
    unidades = get_unidades()
    if not unidades:
        print("Nenhuma unidade de saúde encontrada.")
        return
    
    render_unidades(unidades)

def menu_unidades_add():
    print("==== Adicionar nova Unidade de Saúde ====")
    cod_unidade = input("Código da unidade de saúde: ")
    nome_unidade = input("Nome da unidade de saúde: ")
    tel_unidade = input("Telefone da unidade de saúde: ")
    tipo_unidade = input("Tipo da unidade de saúde: ")
    rua_end_unidade = input("Rua da unidade de saúde: ")
    num_end_unidade = input("Número da unidade de saúde: ")
    bairro_end_unidade = input("Bairro da unidade de saúde: ")
    cep_end_unidade = input("CEP da unidade de saúde: ")
    
    nova_unidade = UnidadeSaude(cod_unidade, nome_unidade, tel_unidade, tipo_unidade, rua_end_unidade, num_end_unidade, bairro_end_unidade, cep_end_unidade)
    result = post_unidade(nova_unidade)
    
    if result['status'] == 'success':
        print(result['message'])
    else:
        print(f"Erro ao adicionar unidade de saúde: {result['message']}")

def menu_unidades_update():
    cod_unidade = input("Código da unidade de saúde a ser atualizada: ")
    unidade = get_unidade(cod_unidade)
    if not unidade:
        print("Unidade não encontrada.")
        return
    
    print(f"Unidade encontrada: {unidade.nome} - {unidade.tipo}")
    
    nome_unidade = input("Novo nome da unidade de saúde (deixe em branco para não alterar): ") or unidade.nome
    tel_unidade = input("Novo telefone da unidade de saúde (deixe em branco para não alterar): ") or unidade.telefone
    tipo_unidade = input("Novo tipo da unidade de saúde (deixe em branco para não alterar): ") or unidade.tipo
    rua_end_unidade = input("Nova rua da unidade de saúde (deixe em branco para não alterar): ") or unidade.rua
    num_end_unidade = input("Novo número da unidade de saúde (deixe em branco para não alterar): ") or unidade.numero
    bairro_end_unidade = input("Novo bairro da unidade de saúde (deixe em branco para não alterar): ") or unidade.bairro
    cep_end_unidade = input("Novo CEP da unidade de saúde (deixe em branco para não alterar): ") or unidade.cep
    
    nova_unidade = UnidadeSaude(cod_unidade, nome_unidade, tel_unidade, tipo_unidade, rua_end_unidade, num_end_unidade, bairro_end_unidade, cep_end_unidade)
    
    result = update_unidade(nova_unidade)
    
    if result['status'] == 'success':
        print(result['message'])
    else:
        print(f"Erro ao atualizar unidade de saúde: {result['message']}")

def menu_unidades_delete():
    cod_unidade = input("Código da unidade de saúde a ser deletada: ")
    unidade = get_unidade(cod_unidade)
    if not unidade:
        print("Unidade não encontrada.")
        return
    
    confirm = input(f"Tem certeza que deseja deletar a unidade {unidade.nome} (s/n)? ")
    if confirm.lower() != 's':
        print("Operação cancelada.")
        return
    
    result = delete_unidade(cod_unidade)
    
    if result['status'] == 'error':
        print(f"Erro ao deletar unidade de saúde: {result['message']}")
        return
    
    print(f"Unidade {unidade.nome} deletada com sucesso.")

def menu_medicamentos_estoque_get():
    cod_unidade = input("Código da unidade de saúde: ")
    unidade = get_unidade(cod_unidade)
    if not unidade:
        print("Unidade não encontrada.")
        return
    
    print(f"Unidade encontrada: {unidade.nome} - {unidade.tipo}")
    estoque = get_estoque_medicamentos(cod_unidade)
    
    if not estoque:
        print("Nenhum medicamento encontrado no estoque desta unidade.")
        return
    
    render_estoque_medicamentos(estoque)

def menu_medicamentos_estoque_add():
    cod_unidade = input("Código da unidade de saúde: ")
    unidade = get_unidade(cod_unidade)
    if not unidade:
        print("Unidade não encontrada.")
        return
    
    lote = input("Lote do medicamento: ")
    cod_anvisa = input("Código ANVISA do medicamento: ")
    validade = input("Validade do medicamento (YYYY-MM-DD): ")
    quantidade = int(input("Quantidade no estoque: "))
    
    novo_estoque = EstoqueMedicamento(lote, cod_anvisa, cod_unidade, validade, quantidade)
    result = post_estoque_medicamento(novo_estoque)
    
    if result['status'] == 'success':
        print(result['message'])
    else:
        print(f"Erro ao adicionar medicamento ao estoque: {result['message']}")

def menu_medicamentos_get():
    medicamentos = get_medicamentos()
    if not medicamentos:
        print("Nenhum medicamento encontrado.")
        return
    
    render_medicamentos(medicamentos)

def menu_medicamentos_add():
    print("==== Adicionar novo Medicamento ====")
    cod_anvisa = input("Código ANVISA do medicamento: ")            
    nome_comercial = input("Nome comercial: ")
    fabricante = input("Fabricante: ")
    apresentacao = input("Apresentação: ")
    forma_administracao = input("Forma de administração: ")
    principio_ativo = input("Princípio ativo: ")
    
    novo_medicamento = Medicamento(cod_anvisa, nome_comercial, fabricante, apresentacao, forma_administracao, principio_ativo)
    result = post_medicamento(novo_medicamento)
    
    if result['status'] == 'success':
        print(result['message'])
    else:
        print(f"Erro ao adicionar medicamento: {result['message']}")

def menu_medicamentos_update():
    cod_anvisa = input("Código ANVISA do medicamento a ser atualizado: ")
    medicamento = get_medicamento(cod_anvisa)
    if not medicamento:
        print("Medicamento não encontrado.")
        return
    
    print(f"Medicamento encontrado: {medicamento.nome_comercial} - {medicamento.fabricante}")
    
    nome_comercial = input("Novo nome comercial (deixe em branco para não alterar): ") or medicamento.nome_comercial
    fabricante = input("Novo fabricante (deixe em branco para não alterar): ") or medicamento.fabricante
    apresentacao = input("Nova apresentação (deixe em branco para não alterar): ") or medicamento.apresentacao
    forma_administracao = input("Nova forma de administração (deixe em branco para não alterar): ") or medicamento.forma_administracao
    principio_ativo = input("Novo princípio ativo (deixe em branco para não alterar): ") or medicamento.principio_ativo
    
    novo_medicamento = Medicamento(cod_anvisa, nome_comercial, fabricante, apresentacao, forma_administracao, principio_ativo)
    
    result = update_medicamento(novo_medicamento)
    
    if result['status'] == 'success':
        print(result['message'])
    else:
        print(f"Erro ao atualizar medicamento: {result['message']}")

def menu_medicamentos_delete():
    cod_anvisa = input("Código ANVISA do medicamento a ser deletado: ")
    medicamento = get_medicamento(cod_anvisa)
    if not medicamento:
        print("Medicamento não encontrado.")
        return
    
    confirm = input(f"Tem certeza que deseja deletar o medicamento {medicamento.nome_comercial} (s/n)? ")
    if confirm.lower() != 's':
        print("Operação cancelada.")
        return
    
    result = delete_medicamento(cod_anvisa)
    
    if result['status'] == 'error':
        print(f"Erro ao deletar medicamento: {result['message']}")
        return
    
    print(f"Medicamento {medicamento.nome_comercial} deletado com sucesso.")

def menu_medicamentos_estoque_subtract():
    cod_unidade = input("Código da unidade de saúde: ")
    unidade = get_unidade(cod_unidade)
    if not unidade:
        print("Unidade não encontrada.")
        return
    
    lote = input("Lote do medicamento: ")
    cod_anvisa = input("Código ANVISA do medicamento: ")
    quantidade = int(input("Quantidade a ser diminuída do estoque: "))
    
    estoque = get_estoque_medicamento(cod_unidade, lote, cod_anvisa)
    if not estoque:
        print("Medicamento não encontrado no estoque desta unidade.")
        return
    
    if estoque.quantidade < quantidade:
        print("Quantidade a ser diminuída é maior que a quantidade disponível no estoque.")
        return
    
    estoque.quantidade -= quantidade
    
    result = update_estoque_medicamento(estoque)
    
    if result['status'] == 'success':
        print(result['message'])
        
    else:
        print(f"Erro ao diminuir medicamento do estoque: {result['message']}")

cases = {
    '1': menu_unidades_get,
    '2': menu_unidades_add,
    '3': menu_unidades_update,
    '4': menu_unidades_delete,
    '5': menu_medicamentos_get,
    '6': menu_medicamentos_add,
    '7': menu_medicamentos_update,
    '8': menu_medicamentos_delete,
    '9': menu_medicamentos_estoque_get,
    '10': menu_medicamentos_estoque_add,
    '11': menu_medicamentos_estoque_subtract,
}

# Console menu interface
def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Listar Unidades de Saúde")
        print("2. Adicionar Unidade de Saúde")
        print("3. Alterar Unidade de Saúde")
        print("4. Deletar Unidade de Saúde")
        print("5. Listar Medicamentos")
        print("6. Adicionar novo Medicamento")
        print("7. Alterar Medicamento")
        print("8. Deletar Medicamento")
        print("9. Listar Estoque de Medicamento por Unidade")
        print("10. Adicionar novo Medicamento ao Estoque de uma Unidade")
        print("11. Diminuir Medicamento do Estoque de uma Unidade")
        print("0. Sair")
        
        print("")
        choice = input("Escolha uma opção: ")
        print("")
        
        if choice == '0':
            print("Saindo do programa...")
            break
        
        if choice in cases:
            cases[choice]()
        else:
            print("Opção inválida. Tente novamente.")
            
if __name__ == "__main__":
    main_menu()
    
conn.close()
