# Aula 07: Processos em SD: Migração
	- Referente a: https://github.com/profmathias/cet-100
## Para executar:
Executar o arquivo 'Hub.py', para iniciar o mapeamento da rede, em seguinda, quaisquer quantidades de 'Worker.py' (Testado com até 2 instancias), finalmente executando o 'HUBClient.py'
- O HUB vai retornar para as instancias Clientes os nomes e IPs dos Servers de trabalho conectados ao HUB, permitindo enviar mensagens para os mesmo atrávez do HUB
- Pelo client, após encontrar o HUB e a lista de servidores ter sido enviada, usar "Server[numero] [mensagem]" para enviar ao Server correspondente, a sua mensagem