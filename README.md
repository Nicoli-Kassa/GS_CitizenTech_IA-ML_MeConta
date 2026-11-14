# Me Conta · Inteligência Artificial & Machine Learning

**Quais idosos têm mais chance de estar desconectados da internet?**

Global Solution 2026.2 · CitizenTech · **Nicoli Amy Kassa | RM559104**

## Ficha da CitizenTech

| Campo | Resposta |
|---|---|
| **Nome da CitizenTech** | Me Conta |
| **Cidade e bairro** | São Paulo (SP). Bairro piloto: Pirituba, zona norte |
| **Cidadão beneficiado** | Pessoas idosas, com mais de 60 anos, especialmente as que moram sozinhas, e seus netos e filhos. Pelo modo "Ensine sua avó", também os idosos que ainda não usam o celular. |
| **Problema em uma frase** | Os avós guardam receitas, histórias da família e memórias do bairro que ninguém mais tem, mas, quando mandam um "bom dia" no grupo da família, recebem de volta um 👍 e nenhuma pergunta. |
| **A solução** | O Me Conta é um aplicativo que troca o 👍 da família por uma pergunta que só os avós sabem responder. |
| **Como funciona** | O neto escolhe uma pergunta no app. O app abre o WhatsApp com a mensagem pronta. O avô responde por áudio, do jeito que já sabe, e a resposta vira uma página do caderno da família, com áudio, foto e título. |
| **Link do repositório** | `[inserir link do repositório]` |
| **Indicador de impacto** | Conversas de verdade por semana: % de idosos que respondem pelo menos uma pergunta da família por semana. |
| **ODS conectados** | **ODS 10**, meta 10.2 · **ODS 11**, meta 11.4 · **ODS 3**, meta 3.4 |

## O que esta parte faz

O Me Conta só funciona para quem já usa a internet. Para quem ainda está fora, o app tem o degrau **Conectar**: o modo
"Ensine sua avó", em que alguém da família ensina o idoso, passo a passo, até o primeiro áudio enviado.

Este módulo treina uma **rede neural MLP (PyTorch)** com dados **reais e públicos** do IBGE (PNAD Contínua 2025, módulo
TIC) para estimar, a partir do perfil de uma pessoa de 60 anos ou mais, a chance de ela não ter usado a internet nos
últimos três meses. O resultado indica **para quem** o degrau Conectar deve chegar primeiro e **qual ajuda** faz sentido
para cada grupo.

## Principais resultados

* **9,1 milhões de idosos (25,5%)** não usaram a internet nos últimos três meses.
* Eles não formam um grupo só. 5,9 milhões (65% dos desconectados) não têm celular próprio e
  1,4 milhão (16%) têm celular sem internet: para eles, o primeiro passo é acesso
  (aparelho ou plano), por parceria ou doação. Outros 1,8 milhão (19%) já têm celular com
  internet e mesmo assim não usaram: é para esse público que o modo "Ensine sua avó" foi pensado.
* O modelo tem **AUC de 0,943 no teste** (à frente da regressão logística por 0,008 de AUC; IC 95%
  da diferença: 0,0068 a 0,0095). Ponderado pela população, encontra 83% dos idosos
  desconectados, com precisão de 76%.
* O que mais pesa no modelo é ter **celular próprio**: só essa variável já chega a AUC 0,813
  na validação. Morar com alguém conectado está associado a muito menos desconexão, mas não basta: 4,9 milhões de idosos
  desconectados moram com alguém que usa a internet.

Os números saem das saídas do notebook; o relatório resume e discute cada um.

## Estrutura

```
IA&ML/                               ← raiz do repositório
├── README.md                        ← este arquivo
└── ml/
    ├── GS2026_IA_ML_MeConta.ipynb   ← notebook executado: exploração, preparação, modelo, busca, resultados e conclusão
    ├── RELATORIO_ML.md              ← relatório: pergunta, dados, modelo, resultados, limitações e conclusão
    ├── prompts.md                   ← registro do uso de IA generativa no desenvolvimento
    ├── requirements.txt             ← versões das bibliotecas
    ├── .gitignore
    └── dados/
        ├── README.md                ← fonte dos dados, como reproduzir e descrição da base
        ├── variaveis.md             ← cada variável usada: código, posição, categorias e papel no modelo
        ├── extrair_pnadc.py         ← lê os microdados do IBGE e gera a base processada
        ├── figuras/                 ← gráficos salvos pelo notebook
        ├── brutos/                  ← arquivos do IBGE (fora do Git, só o .gitkeep; baixar do FTP)
        └── processados/
            └── pnadc2025_tic_60mais.parquet   ← base usada pelo notebook (96.531 pessoas de 60+)
```

## Como executar

**No computador** (Python 3.13), dentro da pasta `ml/`:

```bash
pip install -r requirements.txt
jupyter notebook GS2026_IA_ML_MeConta.ipynb
```

No Jupyter, use **Kernel → Restart & Run All**. A base processada já está em `ml/dados/processados/`, então não é preciso
baixar nada do IBGE. Para refazer a base desde o início, siga [`ml/dados/README.md`](ml/dados/README.md) e rode
`python dados/extrair_pnadc.py` dentro de `ml/`.

**No Google Colab:** copie a pasta `ml/` para o Google Drive, abra o notebook com o Colab e ajuste `PASTA_DRIVE` na
primeira célula de código. Depois, use **Ambiente de execução → Reiniciar sessão e executar tudo**. Os números
apresentados foram obtidos com GPU T4; em CPU, podem variar na 4ª casa decimal.

A flag `QUICK = True`, na célula de configuração, reduz épocas e folds para um teste rápido do código. Os resultados
apresentados foram obtidos com `QUICK = False`.

## Dados

* **Fonte:** IBGE, PNAD Contínua, microdados anuais do 4º trimestre de 2025, módulo de Tecnologia da Informação e
  Comunicação (publicação de 02/07/2026).
* **Microdados:**
  <https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Trimestre/Trimestre_4/>
* **Divulgação oficial dos resultados:**
  [Agência IBGE de Notícias](https://agenciadenoticias.ibge.gov.br/pt/agencia-noticias/47408-proporcao-de-usuarios-da-internet-no-pais-ultrapassou-90-da-populacao-de-10-anos-ou-mais-em-2025.html)

Os microdados do IBGE são anonimizados. Este módulo não usa nenhum dado pessoal real além deles.

## Entregas

| Entrega | Onde |
|---|---|
| Notebook executado | [`ml/GS2026_IA_ML_MeConta.ipynb`](ml/GS2026_IA_ML_MeConta.ipynb) |
| Relatório | [`ml/RELATORIO_ML.md`](ml/RELATORIO_ML.md) |
| Dados e reprodução | [`ml/dados/README.md`](ml/dados/README.md) |
| Uso de IA generativa | [`ml/prompts.md`](ml/prompts.md) |
| Vídeo (YouTube, não listado) | `[inserir link]` |
