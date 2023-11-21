# 1º Projeto de Insight: House Rocket

## Orientações

Acesse o meu [Linked-in](https://www.linkedin.com/in/gabriel-nobre-a0084682/)

Todo contexto de negócio envolvendo este projeto é fictício. A base de dados foi extratida do [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction) e desenvolvida com a ajuda da [Comunidade DS](https://www.comunidadedatascience.com/).

Acesse também os links:
1. ~[Projeto em Produção com Streamlit e Heroku.]~ Devido o Heroku descontinuar o serviço gratuito, o projeto foi migrado para o próprio serviço do Streamlit.
2. [Projeto em Produção no Streamlit.](https://gabrielnbr-insight-1-house-rocket-app-hrapp-kge8fd.streamlit.app/)
3. [Artigo no Medium contando como foi minha experiência.](https://medium.com/@gabrielnobregalvao/1%C2%BA-projeto-de-insight-house-rocket-a67b83107098)

## 1. Negócio

A empresa House Rocket tem como negócio principal a compra, reforma e venda de imóveis nos EUA. Com isto, este projeto foi desenvolvido para auxiliar o time de negócio a encontrar o melhor momento de compra e venda dos imóveis.

Com este projeto eles poderão definir os valores de aporte para comprar as casas, quantas devem ser compradas, quais casas comprar e em qual localização, por quanto vender e qual será o lucro presumido.

### 1.1. Questões de negócio

Pnsando na tomada de decisão do time de negócios, podemos consideramos 2 condições:

1. O time de negócio precisa ter uma ação rápida ao analizar quais casas comprar.
2. Uma vez comprada essas casas qual seria o melhor momento para vendê-las.

Desta forma temos as duas __questões de negócio__:

1. Quais são os melhores imóveis e por quanto comprar?
2. Qual o melhor período de venda dos imóveis e por quanto vender?

### 1.2. Base de dados

A base de dados fornecida ao time de dados possue 21436 linhas com as descrições das casas, sendo esses 19 atributos.

As colunas da base de dados foram traduzidas para português, ficando da seguinte forma:

| Nome da coluna | Tradução | Descrição |
| ----------- | -------- | --------- |
| id | id | ID exclusivo para cada casa vendida |
| date | data_venda | Data da venda da casa |
| price | preco | Preço de cada casa vendida |
| bedrooms | quartos | Número de quartos |
| bedrooms | banheiros | Número de banheiros, onde 0,5 representa um quarto com vaso sanitário, mas sem chuveiro |
| sqft_living | m2_construido_total | Metragem quadrada do espaço interior dos apartamentos |
| sqft_lot | m2_terreno_total | Metragem quadrada do espaço terrestre |
| floors | andares | Número de andares |
| waterfront | vista_agua | Variável fictícia para saber se o apartamento estava com vista para a orla ou não |
| view | vista_geral | Índice de 0 a 4 de quão boa era a vista do imóvel. 0 é a pior vista e 4 é a melhor vista |
| condition | condicao | Índice de 1 a 5 sobre a condição do apartamento. 1 é a pior condição e 5 é a melhor |
| grade | design_construcao | Índice de 1 a 13, onde 1-3 fica aquém da construção e design de edifícios, 7 tem um nível médio de construção e design e 11-13 tem um alto nível de construção e design. |
| sqft_above | m2_construidos_chao | Metragem quadrada do espaço interno da habitação que está acima do nível do solo |
| sqft_basement | m2_porao | Metragem quadrada do espaço interno da habitação que está abaixo do nível do solo |
| yr_built | ano_construído | Ano em que a casa foi construída |
| yr_renovated | ano_reformado | Ano da última reforma da casa |
| zipcode | cep | Em que área de código postal a casa está |
| lat | latitude | latitude |
| long | longitude | longitude |
| sqft_living15 | nao_traduzido | Metragem quadrada do espaço habitacional interior para os 15 vizinhos mais próximos |
| sqft_lot15 | nao_traduzido | A metragem quadrada dos lotes dos 15 vizinhos mais próximos |

## 2. Premissas

Pensando em como resolver os problemas de negócio foram assumidas as seguintes premissas:

1. ID duplicados serão deletados.
2. O design de construção foi considerado bom quando o indicador era superior a 10.
3. As colunas sqft_living15 e sqft_lot15 não foram consideradas para o projeto.
4. Para definição da compra dos imóvel foram utilizadas duas condições:
   1. O imóvel deve está em boa condição de compra. O indicador é representado pela coluna condição, sendo considerado as condições boas como 4 e 5.
   2. O valor de compra do imóvel deve ser menor do que a média em relação aos imóveis mais próximos, desta forma o CEP foi utilizado como medida de proximidade.
5. Para definição da venda dos imóveis foram utilizadas duas condições:
   1. O valor referente a sazonalidade. Os 4 periodos do ano, inverno verão, outono, primareva.
   2. A média de preço em relação aos imóveis mais próximos, o CEP.
   3. O valor venal do imóvel será de __30%__ quando o valor atual dele for __menor__ do que a média da região + sazonalidade.
   4. O valor venal do imóvel será de __10%__ quando o valor atual dele for __maior__ do que a média da região +sazonalidade.

## 3. Planejamento da Solução

1. Os dados foram entregues em formato .csv e serão mantidos desta forma para análise.
2. As ferramentas utilizadas foram:
   1. A IDE VScode.
   2. Jupter Notebook.
   3. Linguagem Python.
3. Explorar de dados:
   1. Bucando identificar dados nulos, faltantes ou outliers.
   2. Criação de estrutura estatística para visualiação mais clara dos dados.
   3. Criação de hipóteses visando o melhor entendimento do negócio.
   4. Criação de novas features para auxiliar no entendimento e resolução das hipóteses e questões de negócio.
4. Realizar o deploy da solução de dados.

## 4. Resultados da Análise

Durante a exploração de dados foi realizado um overview com um histograma de todas as variáveis para perceber o que poderia ser trabalho e quais hipóteses poderiam ser geradas.

Desta forma, foram pensadas em 8 hipóteses que poderiam ajudar e ampliar as perguntas de negócio.

Por fim, foi percebido a necessidade de criar novas features, sendo elas:

| Nome_Feature | Descrição |
| ----------- | --------- |
| construcao_1955 | Indica se a construcão foi feita antes ou depois de 1955. Para construções a baixo de 1955 o valor é 1, se não o valor é 0.|
| sem_porao | Indica se o imóvel tem porão ou não. Para imóveis com porão o valor é 1 e sem porão o valor é 0. |
| ano_venda | Indica exclusivamente o ano de venda do imóvel. |
| mes | Indica, de forma númeral, cada mês de venda do imóvel |
| estações | Indica as 4 estções do ano, de forma nominal, sendo: primavera entre o mês 3 e 5, verão entre o mês 6 e 8, outono entre o mês 9 e 11, por fim, inverno no mês 12, 1 e 2 |
| boa_condição | Indica a boa condição do imóvel através da coluna condição. Foi definido que um local em boas condições deve ter 4 pontos ou mais na coluna condição, se tiver 3 pontos ou menos, não está em boa condição |
| bom_nivel_construcao | Indica o bom nível de construcão do imóvel através da coluna nivel_construcao. Foi definido que um bom nível de construcão deve ter 10 pontos ou mais na coluna nivel_construcao, se tiver 9 pontos ou menos, não está em um bom nível de construcão |

Com as fetures em desenvolvidas, foi o momento de remontar o quadro estatístico:

| Coluna | Media | Std | Min | 25% | Median | 75% | Max | Skew | Kurtosis |
| ------ | ----- | --- | --- | --- | ------ | --- | --- | ---- | -------- |
| preco | 540529.2872 | 367689.2965 | 75000.0000 | 322150.0000 | 450000.0000 | 645000.0000 | 7700000.0000 | 4.0285 | 34.6191 |
| quartos | 3.3702 | 0.9069 | 0.0000 | 3.0000 | 3.0000 | 4.0000 | 11.0000 | 0.5180 | 1.8528 |
| banheiros | 2.1173 | 0.7699 | 0.0000 | 1.7500 | 2.2500 | 2.5000 | 8.0000 | 0.5102 | 1.2915 |
| m2_construido_total | 193.4896 | 85.3915 | 26.9419 | 132.8513 | 178.3738 | 236.9028 | 1257.9072 | 1.4710 | 5.2491 |
| m2_terreno_total | 1406.1468 | 3859.0641 | 48.3096 | 468.2313 | 707.3637 | 993.7141 | 153416.2712 | 13.0437 | 284.0835 |
| andares | 1.4962 | 0.5404 | 1.0000 | 1.0000 | 1.5000 | 2.0000  | 3.5000 | 0.6105 | -0.4908 |
| vista_agua | 0.0076 | 0.0869 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 11.3373 | 126.5467 |
| vista_geral | 0.2351 | 0.7671 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 4.0000 | 3.3867 | 10.8305 |
| condicao | 3.4104 | 0.6502 | 1.0000 | 3.0000 | 3.0000 | 4.0000 | 5.0000 | 1.0362 | 0.5175 |
| nivel_construcao | 7.6617 | 1.1743 | 1.0000 | 7.0000 | 7.0000 | 8.0000 | 13.0000 | 0.7704 | 1.1903 |
| m2_construidos_chao | 166.3857 | 77.0191 | 26.9419 | 111.4836 | 144.9287 | 206.2447 | 874.2176 | 1.4442 | 3.3951 |
| m2_porao | 27.1040 | 41.1358 | 0.0000 | 0.0000 | 0.0000 | 52.0257 | 447.7927 | 1.5769 | 2.7120 |
| ano_construido | 1971.0984 | 29.3853 | 1900.0000 | 1952.0000 | 1975.0000 | 1997.0000 | 2015.0000 | -0.4746 | -0.6543 |
| ano_reformado | 84.7298 | 402.4310 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 2015.0000 | 4.5395 | 18.6107 |
| cep | 98077.8623 | 53.4694 | 98001.0000 | 98033.0000 | 98065.0000 | 98117.0000 | 98199.0000 | 0.4081 | -0.8497 |
| construcao_1955 | 0.2842 | 0.4510 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9570 | -1.0842 |
| sem_porao | 0.3928 | 0.4884 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.4389 | -1.8076 |
| ano_venda | 2014.3189 | 0.4661 | 2014.0000 | 2014.0000 | 2014.0000 | 2015.0000 | 2015.0000 | 0.7770 | -1.3964 |
| mes | 6.5908 | 3.1082 | 1.0000 | 4.0000 | 6.0000 | 9.0000 | 12.0000 | 0.0558 | -1.0020 |
| boa_condicao | 0.3420 | 0.4744 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 0.6660 | -1.5566 |
| bom_nivel_construcao | 0.0759 | 0.2649 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 3.2017 | 8.2515 |

Após a construção do quadro, foi plotado novamente os histogramas com todas as variáveis, afim de fechar o ciclo inicial de exploração dos dados e passar para as hipótes e questões de negócio.

![Histograma](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Histograma.png)

Após o processe de entendimento dos dados fomos as respostas das hipóteses:

| Hipótese | Resultado | Gráfico |
| -------- | --------- | ------- |
| H1: Imóveis que possuem vista para água são pelo menos 30% mais caros, na média. | H1 é verdadeira, pois os imóveis com vista para a água, em média, são 212.42% mais caros. | ![h1](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h1.png) |
| H2: Imóveis com data de construção menor do que 1955, são 50% mais baratos na média. | H2 é falsa, pois os imóveis anteriores a 1955, são em média 0.62% mais caros. | ![h2](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h2.png) |
| H3: Imóveis sem porão possuem m2_construcao_total 50% maiores do que com porão, na média. | H3 é falsa, pois os imóveis sem porão são, em média, -18.56% maiores do que imóveis com porão. | ![h3](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h3.png) |
| H4: O Crescimento do preço dos imóveis YoY (Year over Year) é de 10%, em média. | H4 é falsa, pois o crescimento dos preços dos imóveis YoY, em média, é de 0.05% | ![h4](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h4.png) |
| H5: Imóveis com 3 banheiros tem um crescimento médio no Preço MoM (Month of Month) de 15%. | H5 é falsa, os imóveis não possuem um crescimento MoM de 15%, pois ele prossui uma variação média no período de 1.07% | ![h5](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h5.png) |
| H6: Imóveis no inverno são, em média, são 20% mais baratos do que o resto do ano. | H6 é falsa, pois em média o valor dos imóveis no inverno é -4.62% em comparação ao resto do ano. | ![h6](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h6.png) |
| H7: Pelo menos 80% dos imóveis com condição 4 e 5 tem níveis de construção 7 ou mais. | H7 é verdadeira, pois os imóveis com boa condição representão 85.68%. Sendo o total de imóveis em boa condção: 7332 e os imóveis com nível de construção 7 ou mais: 6282. | ![h7](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h7.png) |
| H8: Pelo menos 80% dos imóveis com vista para água possuem nível de construção 10 ou mais. | H8 é falsa, pois os imóveis com boa condição representão 36.20%. Sendo o total de imóveis em boa condção: 163 e os imóveis com nível de construção 10 ou mais: 59. | ![h8](https://github.com/Gabrielnbr/Insight_1_house_rocket/blob/main/Image/Hipoteses/h8.png) |

## 5. Resultados Financeiros

Após todo o processo de exploração de dados, a partir das premissas e das questões de negõcio, chegamos as seguintes valores financeiros:

### Compra

Para a compra de imóveis foram selecionados 3.777 unidades.

O valor total do aporte para adiquirir todos os imóveis selecionados é de R$ 1.483.908.213,00

O valor total de economia ao adiquirir todos os imóveis selecionados é de R$ 376.310.918,50

## Venda

Para a venda dos imóveis, foi levado em consideração somente as 3.777 unidades possíveis de compra.

A lucratividade total estimada é de: 426.715.962,90

A lucratividade por sazonalidade estimada é de:
| estacoes | lucro_venda |
| -------- | ----------- |
| inverno | 68.919.033,30 |
| outono | 100.162.214,60 |
| primavera | 119.287.887,80 |
| verao | 138.346.827,20 |
