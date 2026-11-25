"""
Motor de Conciliação Financeira e Contábil
Autor: Luís Philipe (@phlimaz)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import csv
from pathlib import Path


@dataclass
class Lancamento:
    id_origem: str
    data: str
    descricao: str
    valor: float
    documento: str = ""

    def __post_init__(self):
        # Garante precisão monetária de 2 casas decimais
        self.valor = round(float(self.valor), 2)


class ConciliadorFinanceiro:
    """Realiza matching cruzado entre duas fontes de lançamentos financeiros."""

    def __init__(self, tolerancia_centavos: float = 0.00):
        self.tolerancia = tolerancia_centavos

    def conciliar(self, fonte_a: List[Lancamento], fonte_b: List[Lancamento]) -> Dict:
        """
        Cruza registros da Fonte A com a Fonte B.
        Identifica: CONCILIADO, DIVERGENCIA e PENDENTE.
        """
        resultado = []
        b_disponiveis = list(fonte_b)
        
        # 1. Matching exato (Documento + Valor)
        for item_a in fonte_a:
            encontrado = None
            
            # Tenta encontrar match por documento se existir
            if item_a.documento:
                for item_b in b_disponiveis:
                    if item_a.documento == item_b.documento:
                        encontrado = item_b
                        break
            
            # Se não achou por doc, tenta por valor e data
            if not encontrado:
                for item_b in b_disponiveis:
                    diferenca = abs(item_a.valor - item_b.valor)
                    if item_a.data == item_b.data and diferenca <= self.tolerancia:
                        encontrado = item_b
                        break

            if encontrado:
                b_disponiveis.remove(encontrado)
                dif = round(item_a.valor - encontrado.valor, 2)
                status = "CONCILIADO" if abs(dif) == 0.0 else "DIVERGENCIA"
                
                resultado.append({
                    "id_a": item_a.id_origem,
                    "data": item_a.data,
                    "descricao_a": item_a.descricao,
                    "valor_a": item_a.valor,
                    "id_b": encontrado.id_origem,
                    "descricao_b": encontrado.descricao,
                    "valor_b": encontrado.valor,
                    "diferenca": dif,
                    "status": status
                })
            else:
                resultado.append({
                    "id_a": item_a.id_origem,
                    "data": item_a.data,
                    "descricao_a": item_a.descricao,
                    "valor_a": item_a.valor,
                    "id_b": "-",
                    "descricao_b": "-",
                    "valor_b": 0.00,
                    "diferenca": item_a.valor,
                    "status": "PENDENTE_FONTE_B"
                })

        # Itens que sobraram na Fonte B sem par na Fonte A
        for item_b in b_disponiveis:
            resultado.append({
                "id_a": "-",
                "data": item_b.data,
                "descricao_a": "-",
                "valor_a": 0.00,
                "id_b": item_b.id_origem,
                "descricao_b": item_b.descricao,
                "valor_b": item_b.valor,
                "diferenca": round(-item_b.valor, 2),
                "status": "PENDENTE_FONTE_A"
            })

        # Estatísticas Consolidadas
        total_itens = len(resultado)
        conciliados = sum(1 for r in resultado if r["status"] == "CONCILIADO")
        divergencias = sum(1 for r in resultado if r["status"] == "DIVERGENCIA")
        pendentes = total_itens - conciliados - divergencias
        taxa_sucesso = (conciliados / total_itens * 100) if total_itens > 0 else 0.0

        return {
            "resumo": {
                "total_registros": total_itens,
                "conciliados": conciliados,
                "divergencias": divergencias,
                "pendentes": pendentes,
                "taxa_conciliacao_pct": round(taxa_sucesso, 1)
            },
            "itens": resultado
        }

    def exportar_csv(self, resultado: Dict, caminho_saida: str) -> Path:
        """Exporta os resultados detalhados para arquivo CSV formatado."""
        arquivo = Path(caminho_saida).resolve()
        
        campos = [
            "id_a", "data", "descricao_a", "valor_a",
            "id_b", "descricao_b", "valor_b", "diferenca", "status"
        ]

        with open(arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writeheader()
            for linha in resultado["itens"]:
                writer.writerow(linha)

        return arquivo
