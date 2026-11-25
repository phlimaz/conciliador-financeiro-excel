# 💼 Conciliador Financeiro e Contábil

Sistema em Python para conciliação e auditoria automatizada de lançamentos financeiros entre extratos bancários e sistemas contábeis.

---

## 🎯 Objetivo de Negócio
Substituir a conferência manual de lançamentos por uma rotina automatizada e auditável, garantindo precisão centavo a centavo e identificando inconsistências em segundos.

---

## 🛠️ Principais Recursos
- **Matching Inteligente:** Cruzamento por identificador de documento, data e valor.
- **Detecção de Divergências:** Identifica variações de valores entre as fontes.
- **Identificação de Pendências:** Aponta registros órfãos em cada uma das bases.
- **Exportação Formatada:** Gera relatório consolidado em formato CSV.
- **Testes Unitários:** Suite de testes automatizados integrada com GitHub Actions (CI).

---

## 📂 Estrutura do Repositório
```
conciliador-financeiro-excel/
├── .github/workflows/
│   └── ci.yml               # Execução de testes contínuos no GitHub
├── src/
│   ├── __init__.py
│   └── conciliador.py       # Motor principal de conciliação
├── tests/
│   └── test_conciliador.py  # Testes unitários com unittest
├── main.py                  # Script executável de demonstração
├── .gitignore
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior instalado.

### Executando a Demonstração
```bash
python main.py
```

### Executando os Testes Automatizados
```bash
python -m unittest discover tests
```

---

👤 **Autor:** Luís Philipe ([@phlimaz](https://github.com/phlimaz))
