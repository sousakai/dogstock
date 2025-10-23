from sqlalchemy import inspect
from database import engine  # importa sua conexão já configurada

insp = inspect(engine)

# Lista todas as tabelas no banco
##print("Tabelas:", insp.get_table_names())

# Mostra as colunas da tabela forncedores
print("\nColunas da tabela 'fornecedores':")
for coluna in insp.get_columns("movimentacoes"):
    print(
        f"Nome: {coluna['name']}, "
        f"Tipo: {coluna['type']}, "
        f"Nulo: {coluna['nullable']}, "
        f"PK: {coluna.get('primary_key', False)}"
    )