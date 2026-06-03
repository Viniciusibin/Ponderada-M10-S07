# Ponderada M10-S07 — Instrumentação de Pipeline CI/CD

Experimento prático de medição e análise de um pipeline CI/CD no GitHub Actions. O projeto coleta métricas reais de 12 execuções com variações controladas, gera gráficos e produz análise crítica de desempenho e gargalos.

## Estrutura do projeto

```
├── .github/workflows/ci.yml   # Pipeline: Lint → Test → Collect Metrics
├── src/
│   └── calculator.py          # App Python com 15 funções matemáticas
├── tests/
│   ├── test_basic.py          # 45 testes unitários baseline
│   ├── test_advanced.py       # Testes de variações
│   └── test_bulk.py           # 50 testes parametrizados (variação #5)
├── scripts/
│   ├── collect_metrics.py     # Coleta dados via GitHub API → CSV
│   ├── collect_run_metadata.py# Roda dentro do Actions, salva artifact
│   └── generate_graphs.py     # Gera 4 gráficos com matplotlib
├── data/
│   ├── metrics.csv            # Métricas por run e por job
│   └── metrics_jobs.csv       # Duração detalhada por job
├── graphs/                    # Gráficos gerados
└── REPORT.md                  # Relatório técnico completo
```

## Pipeline CI/CD

O workflow `.github/workflows/ci.yml` executa automaticamente a cada push em `main` com três jobs:

```
Lint  ──►  Test  ──►  Collect Metrics
(flake8)  (pytest)    (artifact upload)
```

**Etapas:**
- Checkout do código
- Setup Python 3.11 com cache de pip
- Instalação de dependências (`requirements-dev.txt`)
- Lint com `flake8`
- Testes com `pytest --junitxml --cov`
- Upload do relatório JUnit como artifact
- Coleta de metadados do run (test count, status, duração)

## Variações experimentais (12 runs)

| # | Variação | Resultado |
|---|----------|-----------|
| 1 | Baseline — cache ON, 49 testes | ✅ 115s |
| 2 | Cache OFF | ✅ 116s |
| 3 | Teste falhando (assertion errada) | ❌ 122s |
| 4 | Correção do teste | ✅ 143s |
| 5 | +50 testes parametrizados (99 total) | ✅ 124s |
| 6 | Teste lento — `sleep(10)` | ✅ 163s |
| 7 | Remove teste lento | ✅ 156s |
| 8 | Falha de lint (linha >88 chars) | ❌ 119s |
| 9 | Correção do lint | ✅ 146s |
| 10 | Jobs lint e test em **paralelo** | ✅ 121s |
| 11 | Jobs lint e test **sequenciais** | ✅ 146s |
| 12 | Cache ON com hit real | ✅ 144s |

## Gráficos gerados

| Gráfico | Descrição |
|---------|-----------|
| ![graph_01](graphs/graph_01_pipeline_duration.png) | Tempo total por execução |
| ![graph_02](graphs/graph_02_job_duration.png) | Duração por job |
| ![graph_03](graphs/graph_03_success_rate.png) | Taxa de sucesso/falha |
| ![graph_04](graphs/graph_04_tests_vs_duration.png) | Testes × duração |

## Como reproduzir

```bash
# 1. Clonar e instalar dependências
git clone https://github.com/Viniciusibin/Ponderada-M10-S07.git
cd Ponderada-M10-S07
pip install -r requirements-dev.txt

# 2. Rodar lint e testes localmente
flake8 src/ tests/ --max-line-length=88
mkdir -p results
pytest tests/ -v --junitxml=results/junit.xml --cov=src

# 3. Coletar métricas via API (requer GitHub PAT com scope 'repo')
export GITHUB_TOKEN=ghp_SEU_TOKEN
python scripts/collect_metrics.py --repo Viniciusibin/Ponderada-M10-S07

# 4. Gerar gráficos
python scripts/generate_graphs.py
```

## Principais achados

- **Paralelismo** entre lint e test reduziu o tempo total em ~25s (17%)
- **Cache de pip** não gerou ganho mensurável para projetos com poucas dependências
- **Falha de lint** bloqueia o job de test, zerando o feedback dos testes
- **Teste com `sleep(10)`** adicionou ~40s ao pipeline (10s do sleep + overhead do job)

O relatório técnico completo com análise, gráficos e discussão está em [REPORT.md](REPORT.md).

## Execuções no GitHub Actions

Todos os runs reais estão disponíveis em:  
https://github.com/Viniciusibin/Ponderada-M10-S07/actions
