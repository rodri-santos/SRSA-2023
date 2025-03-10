# Descrição do projeto

Desenvolvido num grupo de 2 com Mafalda Duarte.

Neste projeto recebemos dados de vários sensores ligados a um Raspberry Pi, com informações sobre a temperatura, a luminosidade, a pressão, a humidade do ar e a energia consumida tanto em peak hours como em off-peak hours. 

Estes dados vão ser publicados para um MQTT broker, onde este efetua uma ligação entre o publisher e o subscriber.

Guardamos os nossos dados numa database do InfluxDB Cloud2.0 onde vamos ter vários measurements, um para cada variável enviada pelos sensores.

Estabelecemos uma ligação entre o Grafana e o InfluxDB para que seja possível visualizarmos a informação, pelo que utilizámos 3 dashboards do Grafana. 

As dashboards mostram a seguinte informação:
- Summary dashboard: vista geral da informação que está a ser recebida num gráfico time series; 
- Detailed dashboard: apresentamos o último valor de cada variável em gráficos stat, os healthy intervals num gráfico gauge e o histórico dos valores recebidos num gráfico time series juntamente com as moving averages;
- Energy dashboard: visualizar a energia consumida, a variação ao longo do tempo e o custo associado, tudo num gráfico time series.
