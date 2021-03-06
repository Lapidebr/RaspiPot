 # This Python file uses the following encoding: utf-8
import time
import random
import datetime
import telepot
import os
import json
import requests
# Carrega as bibliotecas DHT11 
import Adafruit_DHT
import RPi.GPIO as GPIO


versao ="07092018.1"

print(time.strftime("%d/%m/%Y %H:%M:%S"), "Bot de telegran para Raspi versao: ",versao,"Criado por Frederico Oliveira e Lucas Cassiano")

tokenColetaTxt = open('token.txt', 'r')
idToken = tokenColetaTxt.read()

def handle(msg):
    chat_id = msg['chat']['id']
    usuario = msg['chat']['username'] #adicionado outra chamada de informações do telegran, agora o username
    command = msg['text']
    dataMensagem = time.strftime('%d/%m/%Y %H:%M:%S')

    print('Comando executado: ', command)
    
    if (command == '/roll'):
        bot.sendMessage(chat_id, random.randint(1,10))

    elif(command == '/help' or command == '/start'):
        arquivoHelp = open('help.txt', 'r')
        helpLeitura = arquivoHelp.read()
        bot.sendMessage(chat_id, helpLeitura)
        arquivoHelp.close()

    elif (command == '/time'):
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    elif (command == '/cput'):
		os.system("./cput.sh")
		arquivo = open('temp.txt', 'r') #atribuindo o arquivo para a variável
		mensagemTxt = arquivo.read() #armazenando o conteúdo do arquivo em uma variável
		bot.sendMessage(chat_id, mensagemTxt) #Enviado mensagem
		arquivo.close()

    elif (command == '/loop'):
        lines = open('frases.txt').read().splitlines()
        myLines = random.choice(lines)
        bot.sendMessage(chat_id, myLines)
        lines.close()

    elif (command == '/weather'):
       dadosColetados = coletarDadosAtmosfericos()
       bot.sendMessage(chat_id, dadosColetados)

    elif (command == '/currency'):
        mensagemTxt = cotacaoDolar()
        bot.sendMessage(chat_id, mensagemTxt)

    elif (command == '/uptime'):
        os.system("uptime > temp.txt")
        arquivo = open('temp.txt', 'r') 
        mensagemTxt = arquivo.read()
        bot.sendMessage(chat_id, mensagemTxt)
        arquivo.close()
		
    elif (command == '/dht11'):
		bot.sendMessage(chat_id, "Carregando dados do sensor DHT11...")
		sensor = Adafruit_DHT.DHT11 # Define o tipo de sensor
		GPIO.setmode(GPIO.BOARD)
		pino_sensor = 25 # Define o tipo de sensor
		umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor); # Define o tipo de sensor
		if umid is not None and temp is not None:    # Caso leitura esteja ok, mostra os valores na tela
			mensagemTxt = ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}\n").format(temp, umid);
			bot.sendMessage(chat_id, mensagemTxt)
      
    else:
        bot.sendMessage(chat_id, "Comando não cadastrado")
    print(usuario, dataMensagem, '\n')
    GravarLog(dataMensagem, usuario, command)

bot = telepot.Bot(idToken)
bot.message_loop(handle)

print("Aguardando comandos...")
arquivolog = open('log.txt', 'a')
arquivolog.write('\n\n' + time.strftime("%d/%m/%Y %H:%M:%S") +  " Criado por Frederico Oliveira e Lucas Cassiano versão atual: " + versao)#Log inicial
arquivolog.close()

def GravarLog(dataMensagemLog, usuarioLog, commandLog):
    arquivolog = open('log.txt', 'a')
    arquivolog.write('\n'+ dataMensagemLog + ' ' + usuarioLog + ' comando executado: ' + commandLog)
    arquivolog.close()
	
#Coletando dados atmoféricos
def coletarDadosAtmosfericos():
    url = requests.get('https://api.hgbrasil.com/weather/?format=json&cid=BRXX0033')
    resposta = json.loads(url.text)
    
    dadosColetados = ('Cidade: {}\nTemperatura:{}ºC\nCondição Tempo:{}\nPeriodo:{}\nUmidade do ar:{}%\nAmanhecer:{}\nAnoitecer:{}\nGenerate by api.hgbrasil.com/weather at {}-{}'.format(str(resposta['results']['city_name']),str(resposta['results']['temp']),str(resposta['results']['description']),str(resposta['results']['currently']),str(resposta['results']['humidity']),str(resposta['results']['sunrise']),str(resposta['results']['sunset']),str(resposta['results']['date']),str(resposta['results']['time'])))
			
    return (dadosColetados)	

def cotacaoDolar():
	try:
		requisicao = requests.get("https://economia.awesomeapi.com.br/json/all") #atribuindo o JSON para a variável
		resposta = json.loads(requisicao.text) 
		colecttime = (resposta['USD']['create_date']) #coletando timestamp do JSON
		realtime = (colecttime[11:19]) #exibindo somente a hora do timestamp do JSON
		valores = ('Dólar R${}\nEuro R${}\nLibra R${}\nBitcoin R${}\nGenerate by economia.awesomeapi.com.br at {}(USD)'.format(str(resposta['USD']['high']),str(resposta['EUR']['high']),str(resposta['GBP']['high']),str(resposta['BTC']['high']),realtime))		
		return(valores)
	except:
            return("Erro ao acessar a API")
	
while 1:
    time.sleep(10)