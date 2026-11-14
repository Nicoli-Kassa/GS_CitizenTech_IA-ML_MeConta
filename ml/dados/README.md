# Dados: PNAD Contínua 2025, módulo TIC (IBGE)

Dados **reais e públicos** usados no modelo de IA & ML do Me Conta.

## Fonte

* **Pesquisa:** IBGE, Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua).
* **Recorte:** microdados anuais do **4º trimestre de 2025**, com o módulo suplementar de **Tecnologia da Informação e
  Comunicação (TIC)**.
* **Publicação dos microdados:** 02/07/2026.
* **Pasta no FTP do IBGE:**
  <https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Trimestre/Trimestre_4/>
* **Divulgação oficial dos resultados (Agência IBGE de Notícias):**
  [Proporção de usuários da internet no país ultrapassou 90% da população de 10 anos ou mais, em 2025](https://agenciadenoticias.ibge.gov.br/pt/agencia-noticias/47408-proporcao-de-usuarios-da-internet-no-pais-ultrapassou-90-da-populacao-de-10-anos-ou-mais-em-2025.html).
  Ela traz os números usados para conferir esta base: 74,5% dos idosos usaram a internet em 2025 (70,1% em 2024) e,
  entre os idosos que não usaram, 66,5% apontaram não saber usar como principal motivo. Os 25,5% de idosos desconectados
  calculados aqui (9,1 milhões de pessoas) são o complemento desses 74,5%.

| Arquivo | Pasta no FTP | Para que serve |
|---|---|---|
| `PNADC_2025_trimestre4_20260702.zip` | `Dados/` | Microdados em largura fixa (um registro por pessoa) |
| `input_PNADC_trimestre4_20251010.txt` | `Documentacao/` | Posição e tamanho de cada variável no registro |
| `dicionario_PNADC_microdados_trimestre4_20260702.xls` | `Documentacao/` | Descrição e categorias de cada variável |

Os microdados do IBGE são anonimizados: não há nome, endereço ou documento das pessoas entrevistadas.

## Estrutura desta pasta

```
dados/
├── README.md                 ← este arquivo
├── variaveis.md              ← variáveis usadas, posições, categorias e papel no modelo
├── extrair_pnadc.py          ← gera a base processada a partir dos arquivos do IBGE
├── figuras/                  ← gráficos salvos pelo notebook (os do relatório saem daqui)
├── brutos/                   ← arquivos do IBGE (fora do Git; baixar do FTP)
│   ├── PNADC_2025_trimestre4_20260702.zip
│   └── input_PNADC_trimestre4_20251010.txt
└── processados/
    └── pnadc2025_tic_60mais.parquet   ← base usada pelo notebook
```

A pasta `brutos/` não vai para o repositório, porque os arquivos são grandes e podem ser baixados do IBGE a qualquer
momento. O `.parquet` processado vai, para que o notebook rode sem precisar repetir a extração.

## Como reproduzir

1. Baixe do FTP o `.zip` de microdados e o `input_...txt` e coloque os dois em `dados/brutos/`, sem descompactar.
2. Na pasta `ml/`, rode:

   ```bash
   pip install -r requirements.txt
   python dados/extrair_pnadc.py
   ```

   No Google Colab, a primeira célula do notebook faz esse passo sozinha, se o `.parquet` ainda não existir.
3. O script gera `dados/processados/pnadc2025_tic_60mais.parquet` (e uma cópia em `.csv`, que fica fora do Git).

## O que o script `extrair_pnadc.py` faz

1. Lê as posições das variáveis no `input_...txt`. O input e o dicionário foram conferidos entre si: ambos têm as mesmas
   1.229 variáveis, nas mesmas posições, em registros de 7.362 caracteres.
2. Lê o arquivo de microdados **direto de dentro do `.zip`**, linha por linha, sem descompactar no disco.
3. Para **todos** os moradores, conta por domicílio quantas pessoas de 10 anos ou mais usam a internet, quantas têm de 10 a
   29 anos e quantas dessas usam a internet. A chave do domicílio é `UPA + V1008 + V1014`.
4. Mantém só as pessoas de **60 anos ou mais** e junta a elas as contagens do domicílio, **descontando a própria pessoa**.
5. Cria o alvo e as variáveis derivadas, remove quem não respondeu à pergunta do alvo e salva o resultado.

## Base processada: `pnadc2025_tic_60mais.parquet`

| Característica | Valor |
|---|---|
| Linhas (pessoas de 60+) | 96.531 |
| Domicílios | 71.022 |
| População representada (soma dos pesos) | 35,7 milhões |
| Colunas | 52 |
| Alvo | `desconectado` = 1 quando `S07001` = 2 ("não usou a internet nos últimos três meses") |
| Peso amostral | `V1028` |
| Desconectados (ponderado) | 25,5% = 9,1 milhões (o complemento dos 74,5% de idosos usuários da [divulgação do IBGE](https://agenciadenoticias.ibge.gov.br/pt/agencia-noticias/47408-proporcao-de-usuarios-da-internet-no-pais-ultrapassou-90-da-populacao-de-10-anos-ou-mais-em-2025.html)) |

As colunas estão em quatro grupos:

* **Identificação e desenho amostral:** `Ano`, `Trimestre`, `UF`, `Capital`, `RM_RIDE`, `UPA`, `Estrato`, `V1008`,
  `V1014`, `V2003`, `V1028` e `chave_domicilio`.
* **Variáveis originais da PNAD:** pessoa, domicílio, renda e as perguntas de TIC.
* **Derivadas pelo script:**
  * `desconectado` (alvo);
  * do domicílio, sem contar a própria pessoa: `outros_usam_internet`, `tem_outro_usuario_internet`,
    `tem_jovem_10a29`, `tem_jovem_que_usa_internet` e `outros_com_celular`;
  * recodificações: `mora_sozinho`, `urbano`, `faixa_etaria` e `regiao`.
* **Só para a análise exploratória:** perguntas feitas apenas a quem usou a internet ou apenas a quem não usou (por exemplo,
  `S07005A`, o motivo de não usar). Elas **não entram no modelo**, para evitar vazamento de dados.

A descrição completa de cada variável, com o código, a posição, as categorias e o papel no modelo, está em
[`variaveis.md`](variaveis.md).

## Peso amostral

Cada pessoa da amostra representa milhares de brasileiros. A análise exploratória e os números da conclusão usam o peso
`V1028`, para valerem para a população. O modelo é treinado sem peso. Não use o `V1036`: ele é o peso do morador
selecionado do módulo de Segurança e não serve para o módulo TIC.
