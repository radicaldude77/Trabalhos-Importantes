import csv
import os

CSV_FILE = "gey.csv"
registro = []

def carregar_registros():
    if not os.path.exists(CSV_FILE):#verifica o aquivo existe
        return
    with open(CSV_FILE, newline='', encoding='utf-8') as f:#newline evita quebra de linhas e o encoding é para ler letras acentuadas
        reader = csv.DictReader(f)#transforma cada linha em um dicionário
        registro.clear()#serve para evitar duplicação de dados ao carregar
        for row in reader:#integra os dicionarios lidos do csv
            try:
                row["valor"] = float(row["valor"])#tenta converter para numero o valor string
            except Exception:
                row["valor"] = 0.0#se falhar ele adiciona 0 para nao dar falha (pro usuario)
            registro.append(row)#adiciona o dicionario na lista registro

def salvar_registros():

    fieldnames = ["descricao", "valor", "categoria", "tipo"]# e so o cabeçalho do csv 
    with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:#
        writer = csv.DictWriter(f, fieldnames=fieldnames)       #basicamente abre o arquivo salva o cabeçalho e os itens mudando o valor para string
        writer.writeheader()                                    #
        for item in registro:#exibe as opções e retorna uma opção valida
            row = {
                "descricao": item["descricao"],
                "valor": f"{item['valor']:.2f}",
                "categoria": item["categoria"],
                "tipo": item["tipo"]
            }
            writer.writerow(row)

def menu():
    while True:
        print("\n==== CONTROLE FINANCEIRO ====")
        print("1 - Registrar movimento")
        print("2 - Listar movimentos")
        print("3 - Saldo atual")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha in ("0", "1", "2", "3"):
            return escolha
        print("Opção inválida. Tente novamente.")

def registrar_movimento():
    descricao = input("Digite a descrição do movimento:\n").strip().upper()#usuario digita a descricao do movimento
    while True:
        try:
            valor = float(input("Digite o valor do movimento:\n"))
            if valor <= 0:
                print("O valor deve ser positivo.")
                continue
            break
        except ValueError:
            print("Valor inválido. Tente novamente.")

    tiposcategoria = [
        "despesa fixa",
        "despesa variável",
        "receita operacional",
        "receita extra",
        "investimento",
        "custo de produção"
    ]

    print("\nCategorias:")
    for i, categoria in enumerate(tiposcategoria, start=1):#Imprime as categorias de forma numeradas
        print(f"{i} - {categoria}")
    while True:
        try:
            idx = int(input("Escolha o número da categoria: ").strip())
            if 1 <= idx <= len(tiposcategoria):
                categoria = tiposcategoria[idx - 1]
                break
            print("Número de categoria inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

    while True:
        tipo = input("É saída (S) ou entrada (E)? [S/E]: ").strip().upper()#basicamente ele vai perguntar se é positivo ou negativo
        if tipo in ("S", "E"):
            break
        print("Resposta inválida. Digite S para saída ou E para entrada.")

    valor_assinado = -valor if tipo == "S" else valor

    registro.append({
        "descricao": descricao,
        "valor": valor_assinado,
        "categoria": categoria,
        "tipo": "Saída" if tipo == "S" else "Entrada"
    })
    salvar_registros()
    print("Movimento registrado com sucesso.")

def listar_movimentos():
    if not registro:
        print("Nenhum movimento registrado.")
        return
    print("\n==== MOVIMENTOS ====")
    for i, movimento in enumerate(registro, start=1):#percorre cada item de registro com índice começando em 1.
        sinal = "-" if float(movimento["valor"]) < 0 else "+"#converte o ["valor"] para float e testa se é negativo.
        print(f"{i}. {movimento['descricao']} | {movimento['categoria']} | {movimento['tipo']} | {sinal}R$ {abs(float(movimento['valor'])):.2f}")

def calcular_saldo():
    saldo = sum(float(item["valor"]) for item in registro)
    print(f"\nSaldo atual: R$ {saldo:.2f}")

def main():#agrupa inicialização e loop de interação
    carregar_registros()
    while True:
        escolha = menu()#inicia o loop infinito do menu ate q a pessoa escolha sair
        if escolha == "0":
            print("Saindo...")
            break
        elif escolha == "1":
            registrar_movimento()
        elif escolha == "2":
            listar_movimentos()
        elif escolha == "3":
            calcular_saldo()

if __name__ == "__main__":#garante que o main so rode se for o arquivo executado diretamente
    main()

menu()