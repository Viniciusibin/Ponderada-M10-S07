# Relatório Técnico — Instrumentação de Pipeline CI/CD

**Aluno:** Vinicius Ibiapina  
**Módulo:** M10 — Sprint 07  
**Repositório:** https://github.com/H3-Solar-Org/Ponderada-M10-S07  
**Pipeline:** [.github/workflows/ci.yml](.github/workflows/ci.yml)

---

## 1. Objetivo e Hipóteses Iniciais

O experimento tem como objetivo instrumentar um pipeline de CI/CD no GitHub Actions, coletar métricas reais de execução e analisar comportamento, desempenho e gargalos.

### Hipóteses iniciais

| # | Hipótese |
|---|----------|
| H1 | O cache de dependências pip reduzirá o tempo de instalação em pelo menos 50% |
| H2 | A execução paralela dos jobs de lint e test reduzirá o tempo total do workflow |
| H3 | A etapa de instalação de dependências será o principal gargalo em execuções sem cache |
| H4 | Testes lentos (sleep) aumentarão o tempo de forma linear e previsível |

---

## 2. Descrição do Projeto

Projeto Python com uma calculadora simples (`src/calculator.py`) contendo ~15 funções matemáticas cobertas por testes unitários com `pytest`.

**Pipeline (jobs):**
1. **Lint** — `flake8` para análise estática
2. **Test** — `pytest` com relatório JUnit XML e cobertura
3. **Collect Metrics** — coleta metadados e faz upload de artifact

---

## 3. Variações Controladas

| # | Commit | Tipo | Descrição | Resultado esperado |
|---|--------|------|-----------|-------------------|
| 1 | — | Baseline | Setup inicial, todos os testes passam, sem cache | Sucesso |
| 2 | — | Cache ON | Ativa cache de pip no workflow | Sucesso, mais rápido |
| 3 | — | Falha de teste | Assertion errada em test_basic.py | Falha no job test |
| 4 | — | Correção | Reverte assertion errada | Sucesso |
| 5 | — | +50 testes | Adiciona 50 testes parametrizados | Sucesso, mais lento |
| 6 | — | Teste lento | `time.sleep(5)` em um teste | Sucesso, muito lento |
| 7 | — | Remove slow test | Remove o sleep | Sucesso, tempo normal |
| 8 | — | Falha de lint | Linha >88 chars no código | Falha no job lint |
| 9 | — | Correção lint | Corrige a linha longa | Sucesso |
| 10 | — | Jobs paralelos | lint e test rodam em paralelo | Sucesso, mais rápido |
| 11 | — | Jobs sequenciais | Volta a sequencial | Sucesso, mais lento |
| 12 | — | Cache OFF | Desativa cache novamente | Sucesso, mais lento |

> **Nota:** os hashes dos commits serão preenchidos após a execução.

---

## 4. Execuções Reais no GitHub Actions

> **Esta seção será preenchida após as 12 execuções.**

| Run # | Run ID | Commit | Status | Duração total |
|-------|--------|--------|--------|--------------|
| 1 | — | — | — | — |
| 2 | — | — | — | — |
| ... | | | | |

**Links das execuções:**  
https://github.com/H3-Solar-Org/Ponderada-M10-S07/actions

---

## 5. Métricas Coletadas

> **Esta seção será preenchida após rodar `collect_metrics.py`.**

Arquivo: `data/metrics.csv`

| Coluna | Descrição |
|--------|-----------|
| `run_id` | ID numérico do GitHub Actions run |
| `commit_sha` | Hash curto do commit |
| `commit_message` | Mensagem do commit |
| `status` | `success` / `failure` |
| `workflow_duration` | Tempo total do workflow em segundos |
| `job_name` | Nome do job (Lint / Test / Collect Metrics) |
| `job_duration` | Duração do job em segundos |
| `test_count` | Número de testes executados |
| `test_failures` | Número de testes com falha |
| `test_duration` | Tempo de execução dos testes |
| `timestamp` | Data e hora da execução (UTC) |

---

## 6. Gráficos

> Os gráficos serão gerados com `python scripts/generate_graphs.py` após a coleta de dados.

| Gráfico | Arquivo |
|---------|---------|
| Tempo total do pipeline por execução | `graphs/graph_01_pipeline_duration.png` |
| Tempo por job em cada execução | `graphs/graph_02_job_duration.png` |
| Taxa de sucesso e falha | `graphs/graph_03_success_rate.png` |
| Quantidade de testes × duração | `graphs/graph_04_tests_vs_duration.png` |

---

## 7. Análise dos Resultados

> **Esta seção será preenchida com dados reais após as execuções.**

### 7.1 Qual etapa mais contribuiu para o tempo total?

_A ser preenchido._

### 7.2 Houve diferença significativa com e sem cache?

_A ser preenchido — comparar execuções #1 (sem cache) vs #2 (com cache) e #12 (sem cache novamente)._

### 7.3 O paralelismo reduziu o tempo total?

_A ser preenchido — comparar execuções #10 (paralelo) vs #11 (sequencial)._

### 7.4 Quais falhas foram mais frequentes?

_A ser preenchido._

### 7.5 O pipeline fornece feedback rápido o suficiente?

_A ser preenchido._

### 7.6 Que melhorias poderiam ser feitas?

_A ser preenchido._

### 7.7 Quais limitações existem nos dados coletados?

- O tempo de fila do GitHub Actions não é diretamente controlável e varia conforme a carga.
- A granularidade de steps individuais exige API calls adicionais por cada job.
- Artefatos de métricas dependem de o job `collect-metrics` ter sucesso — em falhas de lint, o test não roda e portanto o artifact pode estar vazio.

### 7.8 Como essa análise apoia decisões de engenharia?

_A ser preenchido._

---

## 8. Resultados Inesperados

> **Esta seção será preenchida com análise de pelo menos 2 resultados inesperados.**

---

## 9. Comparação Hipótese × Resultado

| Hipótese | Resultado observado | Confirmada? |
|----------|---------------------|-------------|
| H1 — cache reduz ≥50% do tempo de instalação | _a preencher_ | — |
| H2 — paralelismo reduz tempo total | _a preencher_ | — |
| H3 — instalação é o principal gargalo sem cache | _a preencher_ | — |
| H4 — teste lento aumenta tempo linearmente | _a preencher_ | — |

---

## 10. Limitações do Experimento

- Variabilidade da infraestrutura do GitHub Actions (runners compartilhados)
- Tamanho pequeno do projeto limita o impacto real de cache e paralelismo
- Apenas 12 execuções — base estatística pequena
- Não foram testados cenários de rede lenta ou falha de infraestrutura
- O runner `ubuntu-latest` pode mudar de versão sem aviso

---

## 11. Como Reproduzir

```bash
# Clonar o repositório
git clone https://github.com/H3-Solar-Org/Ponderada-M10-S07.git
cd Ponderada-M10-S07

# Instalar dependências
pip install -r requirements-dev.txt

# Rodar lint localmente
flake8 src/ tests/ --max-line-length=88

# Rodar testes localmente
mkdir -p results
pytest tests/ -v --junitxml=results/junit.xml --cov=src

# Coletar métricas (requer GitHub PAT com scope 'repo')
export GITHUB_TOKEN=ghp_SEU_TOKEN_AQUI
python scripts/collect_metrics.py --repo H3-Solar-Org/Ponderada-M10-S07

# Gerar gráficos
python scripts/generate_graphs.py
```

As execuções do pipeline são disparadas automaticamente a cada push para `main`.
