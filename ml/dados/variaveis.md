# Variáveis usadas: PNAD Contínua 2025, 4º trimestre (módulo TIC)

Fonte das posições: `input_PNADC_trimestre4_20251010.txt`. Fonte das categorias: `dicionario_PNADC_microdados_trimestre4_20260702.xls`. Os dois arquivos foram conferidos entre si: têm as mesmas 1.229 variáveis, com as mesmas posições e tamanhos. Cada registro tem 7.362 caracteres.

O módulo TIC de pessoas (Parte Suplementar 07) é respondido por **moradores de 10 anos ou mais** e vale de 2016 a 2025. O script `dados/extrair_pnadc.py` mantém só quem tem **60 anos ou mais** e respondeu a `S07001`.

**Peso:** `V1028` (peso do domicílio e das pessoas, com calibração). Não use `V1036`, que é o peso do morador selecionado do módulo de Sensação de Segurança e não serve para o TIC.

**Chave do domicílio:** `UPA` + `V1008` + `V1014`.

## Alvo

| Código | Pos. | Pergunta | Categorias | Uso |
|---|---|---|---|---|
| S07001 | 508 | Nos últimos três meses, utilizou a Internet em algum local? | 1 Sim · 2 Não | `desconectado = 1` quando S07001 = 2 |

## Variáveis explicativas (entram no modelo)

| Código | Pos. | Descrição | Categorias / formato |
|---|---|---|---|
| V2009 | 104 | Idade | anos (também vira `faixa_etaria`) |
| V2007 | 95 | Sexo | 1 Homem · 2 Mulher |
| V2010 | 107 | Cor ou raça | 1 Branca · 2 Preta · 3 Amarela · 4 Parda · 5 Indígena · 9 Ignorado |
| UF | 6 | Unidade da Federação | código IBGE (também vira `regiao`) |
| V1022 | 33 | Situação do domicílio | 1 Urbana · 2 Rural (vira `urbano`) |
| V1023 | 34 | Tipo de área | 1 Capital · 2 Resto da RM · 3 Resto da RIDE · 4 Resto da UF |
| V3001 | 108 | Sabe ler e escrever | 1 Sim · 2 Não |
| VD3004 | 1116 | Nível de instrução | 1 Sem instrução … 7 Superior completo |
| VD3005 | 1117 | Anos de estudo | 0 a 16 |
| VDI5008 | 1271 | Renda domiciliar per capita (habitual) | R$; 99999999 = ignorado (vira vazio) |
| VI5004A | 425 | Recebe aposentadoria ou pensão | 1 Sim · 2 Não · 9 Ignorado |
| VD4001 / VD4002 | 1120 / 1121 | Força de trabalho / ocupação | VD4002 = 1 → trabalha; vazio para quem está fora da força de trabalho |
| V2005 | 93 | Condição no domicílio | 01 Responsável · 02/03 Cônjuge · 08 Pai/mãe · 09 Sogro(a) · … |
| VD2004 | 1113 | Espécie da unidade doméstica | 1 Unipessoal (vira `mora_sozinho`) · 2 Nuclear · 3 Estendida · 4 Composta |
| VD2003 | 1111 | Número de componentes do domicílio | 1 a 30 |
| S07006 | 540 | Tem celular para uso pessoal | 1 Sim · 2 Não |
| S01028 | 491 | Domicílio tem microcomputador | 1 Sim · 2 Não |
| S01030C | 506 | Sinal de celular funciona no domicílio | 1 Sim · 2 Não · 3 Não sabe |

### Derivadas pelo script (domicílio, sem contar a própria pessoa)

| Coluna | O que é | Por que importa para o Me Conta |
|---|---|---|
| `outros_usam_internet` | nº de outros moradores (10+) que usam internet | Há alguém em casa que pode ensinar |
| `tem_outro_usuario_internet` | 1 se `outros_usam_internet` > 0 | Idem, em versão sim/não |
| `tem_jovem_10a29` | 1 se mora alguém de 10 a 29 anos | Presença de neto ou jovem no domicílio |
| `tem_jovem_que_usa_internet` | 1 se esse jovem usa internet | O "neto professor" do modo "Ensine sua avó" |
| `outros_com_celular` | `S01021` menos o celular da própria pessoa | Acesso a aparelho em casa |
| `mora_sozinho`, `urbano`, `faixa_etaria`, `regiao` | recodificações de VD2004, V1022, V2009, UF | |

## Só para análise descritiva (NÃO entram no modelo)

Essas perguntas só são feitas para quem usa, ou só para quem não usa, a internet. Colocá-las no modelo entregaria a resposta (vazamento de dados).

| Código | Pos. | Pergunta | Quem responde | Para que serve |
|---|---|---|---|---|
| S07005A | 534 | Principal motivo de não ter usado a internet | só quem não usou | 1 Serviço caro · 2 Equipamento caro · 3 Indisponível · 4 Falta de necessidade · 5 Falta de tempo · 6 **Não sabia usar** · 7 Privacidade/segurança · 8 Outro. Justifica o modo "Ensine sua avó" |
| S07005B2 | 536 | Enviou/recebeu mensagens por WhatsApp, Telegram etc. | só quem não usou | Idosos que usam WhatsApp mas não se veem como "usuários de internet" |
| S07001A | 509 | Frequência de uso da internet | só quem usou | Perfil dos idosos conectados |
| S07007 | 541 | O celular pessoal tem acesso à internet | só quem tem celular | Quase igual ao alvo |
| S07008A | 543 | Motivo de não ter celular | só quem não tem | Descritivo |
| S01029 | 493 | Algum morador tem internet no domicílio | todos | Para quem mora sozinho, é praticamente o próprio alvo. Pode entrar num teste de sensibilidade |
| S01030D | 507 | Motivo de o domicílio não ter internet | só domicílios sem internet | Descritivo |
| S07009 | 544 | Informante do módulo (a própria pessoa, outro morador…) | todos | Controle de qualidade da resposta |

## Identificação e desenho amostral (guardadas, não entram no modelo)

`Ano`, `Trimestre`, `Capital` (35 = município de São Paulo, útil para o recorte do piloto em Pirituba), `RM_RIDE`, `UPA`, `Estrato`, `V1008`, `V1014`, `V2003`, `V1028`, `chave_domicilio`.
