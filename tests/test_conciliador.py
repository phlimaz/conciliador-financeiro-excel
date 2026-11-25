"""
Testes unitários automatizados para o motor de conciliação financeira.
"""

import unittest
from src.conciliador import ConciliadorFinanceiro, Lancamento


class TestConciliadorFinanceiro(unittest.TestCase):

    def setUp(self):
        self.conciliador = ConciliadorFinanceiro(tolerancia_centavos=0.05)

    def test_conciliacao_exata_por_documento(self):
        fonte_a = [Lancamento("A1", "2026-11-01", "Pgto Fornecedor X", 1500.50, "DOC123")]
        fonte_b = [Lancamento("B1", "2026-11-01", "Fornecedor X Ltda", 1500.50, "DOC123")]

        resultado = self.conciliador.conciliar(fonte_a, fonte_b)
        
        self.assertEqual(resultado["resumo"]["conciliados"], 1)
        self.assertEqual(resultado["resumo"]["divergencias"], 0)
        self.assertEqual(resultado["resumo"]["taxa_conciliacao_pct"], 100.0)

    def test_deteccao_de_divergencia_de_centavos(self):
        conciliador_estrito = ConciliadorFinanceiro(tolerancia_centavos=0.00)
        fonte_a = [Lancamento("A2", "2026-11-02", "Tarifa Bancaria", 25.50, "DOC999")]
        fonte_b = [Lancamento("B2", "2026-11-02", "Tarifa Bancaria", 25.52, "DOC999")]

        resultado = conciliador_estrito.conciliar(fonte_a, fonte_b)
        
        self.assertEqual(resultado["resumo"]["divergencias"], 1)
        self.assertEqual(resultado["itens"][0]["status"], "DIVERGENCIA")
        self.assertEqual(resultado["itens"][0]["diferenca"], -0.02)

    def test_lancamento_pendente(self):
        fonte_a = [Lancamento("A3", "2026-11-03", "Pix Recebido", 350.00)]
        fonte_b = []

        resultado = self.conciliador.conciliar(fonte_a, fonte_b)
        
        self.assertEqual(resultado["resumo"]["pendentes"], 1)
        self.assertEqual(resultado["itens"][0]["status"], "PENDENTE_FONTE_B")


if __name__ == "__main__":
    unittest.main()
