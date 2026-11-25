"""
Script Principal de Demonstração da Conciliação Financeira
Autor: Luís Philipe (@phlimaz)
"""

from src.conciliador import ConciliadorFinanceiro, Lancamento


def main():
    print("=" * 65)
    print(" 💼 SISTEMA DE CONCILIAÇÃO FINANCEIRA AUTOMATIZADA")
    print("=" * 65)

    # Simulação da Fonte A (Ex: Extrato Bancário)
    extrato_banco = [
        Lancamento("EXT-001", "25/11/2026", "Pagamento Fornecedor Alpha", 4520.80, "DOC-8821"),
        Lancamento("EXT-002", "25/11/2026", "Tarifa Manutencao de Conta", 79.90, "DOC-1002"),
        Lancamento("EXT-003", "25/11/2026", "Recebimento Cliente Beta", 12500.00, "DOC-9914"),
        Lancamento("EXT-004", "25/11/2026", "Estorno Cobranca Indevida", 150.00, "DOC-4411"),
    ]

    # Simulação da Fonte B (Ex: Razão Contábil / ERP Interno)
    razao_contabil = [
        Lancamento("RZ-101", "25/11/2026", "Fornecedor Alpha S/A", 4520.80, "DOC-8821"),
        Lancamento("RZ-102", "25/11/2026", "Tarifa Bancaria Mensal", 79.95, "DOC-1002"), # Divergência de 5 centavos
        Lancamento("RZ-103", "25/11/2026", "Cliente Beta Comercio", 12500.00, "DOC-9914"),
        Lancamento("RZ-104", "25/11/2026", "Despesa Material Escritorio", 230.00, "DOC-7711"), # Pendência
    ]

    conciliador = ConciliadorFinanceiro(tolerancia_centavos=0.00)
    resultado = conciliador.conciliar(extrato_banco, razao_contabil)
    resumo = resultado["resumo"]

    print("\n📊 RESUMO DO PROCESSAMENTO:")
    print(f" • Total de Lançamentos Analisados : {resumo['total_registros']}")
    print(f" • Lançamentos 100% Conciliados    : {resumo['conciliados']} ✅")
    print(f" • Divergências de Valores         : {resumo['divergencias']} ⚠️")
    print(f" • Lançamentos Pendentes           : {resumo['pendentes']} ❌")
    print(f" • Taxa de Sucesso da Conciliação  : {resumo['taxa_conciliacao_pct']}%")

    print("\n🔍 DETALHE DOS ITENS COM DIVERGÊNCIA OU PENDÊNCIA:")
    print("-" * 65)
    for item in resultado["itens"]:
        if item["status"] != "CONCILIADO":
            print(f"[{item['status']}]")
            print(f"   Fonte A: {item['descricao_a']} | R$ {item['valor_a']}")
            print(f"   Fonte B: {item['descricao_b']} | R$ {item['valor_b']}")
            print(f"   Diferença: R$ {item['diferenca']}")
            print("-" * 65)

    caminho_csv = conciliador.exportar_csv(resultado, "relatorio_conciliacao.csv")
    print(f"\n💾 Relatório detalhado exportado com sucesso em: {caminho_csv.name}")
    print("=" * 65)


if __name__ == "__main__":
    main()
