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


## GET /medicamentos
def get_medicamentos():
    df = pd.read_sql_query(
        'SELECT * FROM medicamento',
        conn)
    medicamentos = df.to_dict(orient='records')
    return [Medicamento(**med) for med in medicamentos]

## POST /medicamentos
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

## GET /unidades
def get_unidades():
    df = pd.read_sql_query(
        'SELECT * FROM unidadesaude',
        conn)
    unidades = df.to_dict(orient='records')
    return [UnidadeSaude(**un) for un in unidades]

## POST /unidades
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

## GET /unidades/<cod_unidade>
def get_unidade(cod_unidade):
    df = pd.read_sql_query(
        'SELECT * FROM unidadesaude WHERE cod_unidade = %s',
        conn,
        params=(cod_unidade,))
    if df.empty:
        return None
    
    unidade = UnidadeSaude(**df.iloc[0].to_dict())
    return unidade

## GET /unidades/<cod_unidade>/medicamentos
def get_estoque_medicamentos(cod_unidade):
    df = pd.read_sql_query(
        'SELECT * FROM medicamentoestocado WHERE cod_unidade = %s',
        conn,
        params=(cod_unidade,))
    if df.empty:
        return []
    
    estoque = df.to_dict(orient='records')
    return [EstoqueMedicamento(**item) for item in estoque]

## POST /unidades/<cod_unidade>/medicamentos
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

## ==== Functions de renderização
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

## Console menu interface
def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Listar Unidades de Saúde")
        print("2. Adicionar Unidade de Saúde")
        print("3. Listar Medicamentos")
        print("4. Adicionar novo Medicamento")
        print("5. Listar Estoque de Medicamento por Unidade")
        print("6. Adicionar novo Medicamento ao Estoque de uma Unidade")
        print("0. Sair")
        print("="*70)
        
        choice = input("Escolha uma opção: ")
        print("")
        
        if choice == '1':
            unidades = get_unidades()
            render_unidades(unidades)
            
        elif choice == '2':
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
                break

        elif choice == '3':
            medicamentos = get_medicamentos()
            render_medicamentos(medicamentos)

        elif choice == '4':
            print("==== Adicionar novo Medicamento ====")
            print("Código ANVISA: ")
            cod_anvisa = input("Código ANVISA do medicamento: ")            
            print("Nome comercial: ")            
            nome_comercial = input("Nome comercial: ")
            print("Fabricante: ")
            fabricante = input("Fabricante: ")
            print("Apresentação: ")
            apresentacao = input("Apresentação: ")
            print("Forma de administração: ")
            forma_administracao = input("Forma de administração: ")
            print("Princípio ativo: ")
            principio_ativo = input("Princípio ativo: ")
            novo_medicamento = Medicamento(cod_anvisa, nome_comercial, fabricante, apresentacao, forma_administracao, principio_ativo)
            result = post_medicamento(novo_medicamento)
            
            if result['status'] == 'success':
                print(result['message'])
            else:
                print(f"Erro ao adicionar vacina: {result['message']}")
                break

        elif choice == '5':
            print("==== Listar Estoque de Medicamentos por Unidade ====")
            cod_unidade = input("Código da unidade de saúde: ")
            unidade = get_unidade(cod_unidade)
            if not unidade:
                print("Unidade não encontrada.")
                continue
            print(f"Unidade encontrada: {unidade.nome} - {unidade.tipo}")
            estoque = get_estoque_medicamentos(cod_unidade)
            if not estoque:
                print("Nenhum medicamento encontrado no estoque desta unidade.")
            else:
                render_estoque_medicamentos(estoque)
            
        elif choice == '6':
            print("==== Adicionar novo Medicamento ao Estoque de uma Unidade ====")
            cod_unidade = input("Código da unidade de saúde: ")
            unidade = get_unidade(cod_unidade)
            if not unidade:
                print("Unidade não encontrada.")
                continue
            
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
            
        elif choice == '0':
            break
        
        else:
            print("Opção inválida, tente novamente.")
            
            
if __name__ == "__main__":
    main_menu()
    
conn.close()
