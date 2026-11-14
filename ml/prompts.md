# Uso de IA generativa

Usei o **Claude (Anthropic)** como assistente durante o desenvolvimento desta parte. Este arquivo registra para que ele
foi usado, os principais pedidos feitos e o que ficou sob minha responsabilidade.

## O que ficou comigo

* A escolha da pergunta de ML ("Quais idosos têm mais chance de estar desconectados da internet?"), da base (PNAD
  Contínua 2025, módulo TIC) e do alvo (`S07001` = 2), ligados ao degrau Conectar do Me Conta.
* A execução do notebook no Google Colab (GPU T4) e a conferência das saídas.
* A leitura crítica de cada versão: o que manter, o que cortar e o que corrigir.
* A redação da introdução do notebook, que depois foi revisada com ajuda da IA.

## Principais pedidos, por etapa

| Etapa | O que pedi | Como usei a resposta |
|---|---|---|
| Dados | Ler o arquivo de input e o dicionário da PNAD Contínua e localizar as variáveis do módulo TIC, do domicílio e do peso amostral. | Conferi as posições com o dicionário antes de usar. |
| Extração | Escrever um script que leia os microdados de largura fixa direto do `.zip`, monte as variáveis do domicílio e filtre as pessoas de 60+. | Virou o `dados/extrair_pnadc.py`; os totais foram comparados com a divulgação oficial do IBGE (74,5% de idosos usuários). |
| Notebook | Montar o notebook com exploração, preparação sem vazamento, MLP em PyTorch, busca de hiperparâmetros com validação cruzada por domicílio, comparação com modelos de referência e conclusão ligada ao app. | Usei notebooks de referência em PyTorch como base de estilo e rodei tudo no Colab. |
| Colab | Explicar como rodar no Colab com os dados no Google Drive e corrigir o erro de caminho do script de extração. | Ajustei a célula de montagem do Drive. |
| Revisão | Simular a avaliação do projeto por um avaliador de IA & ML, apontando falhas de método, de interpretação e de reprodutibilidade. | Cada rodada de correções foi aplicada no notebook e rodada de novo. Exemplos: regra do 1 erro-padrão na escolha da rede, métricas ponderadas pela população, intervalos de confiança por bootstrap, separação entre quem não tem acesso e quem tem acesso e não usa. |
| Textos | Escrever o relatório, os READMEs e a documentação das variáveis a partir das saídas do notebook. | Regra que segui: todo número no texto sai de uma saída do notebook. Onde o valor dependia de uma nova execução, ficou um marcador até rodar. |
| Organização | Organizar a pasta do repositório (`ml/`, `dados/`, `.gitignore`, `requirements.txt`). | Estrutura descrita no README da raiz. |

## Cuidados

* Nenhum dado pessoal foi enviado à IA: só a documentação pública do IBGE, o código e as saídas agregadas do notebook.
* Os números do relatório não foram gerados pela IA: vêm das saídas do notebook executado.
* A pergunta, a base e o alvo ficaram fixos em todas as revisões.
