import requests
import json
import re
from bs4 import BeautifulSoup

class AdoroCinema:
    def extrairmovieName(self, movie):
        url = "https://www.adorocinema.com/movies/" + movie +'/'
        htmlmovie = requests.get(url).text
        bsS = BeautifulSoup(htmlmovie, 'html.parser')
        nome = bsS.find('div', class_="titlebar-title titlebar-title-lg").get_text(strip=True)
        return nome 
    

    def extrairSinopsemovie (self, movie):      
        url = "https://www.adorocinema.com/movies/" + movie +'/'
        htmlmovie = requests.get(url).text
        bsS = BeautifulSoup(htmlmovie, 'html.parser')
        sinopse = bsS.find('div', class_="content-txt").get_text(strip=True)
        return sinopse
    
    def salvarSinopsemovie(self, movie, sinopse):
        arq_saida = open(movie+'_sinopse.txt', 'w',encoding='utf-8')
        for line in sinopse:
            arq_saida.write(line)
        arq_saida.close()

    def extrairComentariosmovie(self, movie, n):
        comentarios = []
        for i in range(1,n+1):
            url = 'http://www.adorocinema.com/movies/' + movie + '/criticas/espectadores/?page=' + str(i)
            htmlComentarios = requests.get(url).text
            bsC = BeautifulSoup(htmlComentarios, 'html.parser')
            comentarios_com_tags = bsC.find_all('div', class_="content-txt review-card-content")
            for comentario_com_tag in comentarios_com_tags:
                comentarios.append(comentario_com_tag.get_text().strip())
        return comentarios

    def salvarComentariosmovie(self, movie, comentarios):
        arq_saida = open(movie+'_comentarios.txt', 'w', encoding='utf-8')
        for comentario in comentarios:
            arq_saida.write(comentario + '\n')
        arq_saida.close()
    
    # Função que recebe o nome do arquivo de comentários do filme, lê cada line do arquivo e
    # Verifica se contém words positivas ou negativas a partir de listas predefinidas de words.
    def countPositiveNegative(self, movie):
        # Abre o arquivo para leitura
        with open(movie + '_comentarios.txt', 'r', encoding='utf-8') as arq_entrada:
            # Inicialize contadores
            positives = 0
            negatives = 0
            totalComents = 0

            # Regras do REGEX para localizar palavras positivas ou negativas nos comentários
            padrao_positivo = re.compile(r'\b(bom|ótimo|excelente)\b', re.IGNORECASE)
            padrao_negativo = re.compile(r'\b(ruim|péssimo|horrível)\b', re.IGNORECASE)

            # Loop pelas lines do arquivo
            for line in arq_entrada:
                totalComents += 1
                
                # Verifique words positivas
                if re.search(padrao_positivo, line):
                    positives += 1

                # Verifique words negativas
                if re.search(padrao_negativo, line):
                    negatives += 1
                    
        # Retorne os resultados
        return positives, negatives, totalComents

    def storeResults(self, nome, totalComents, percentPositives, percentNegatives):
        data = {}
        data['nome'] = nome
        data['totalComents'] = totalComents
        data['percentPositives'] = percentPositives
        data['percentNegatives'] = percentNegatives
        try:
            with open('data.json') as results:
                existing_data = json.load(results)
        except:
            existing_data = []

        existing_data.append(data)
        
        with open('data.json', 'w', encoding='utf-8') as results:
            json.dump(existing_data, results, ensure_ascii=False, indent=4)



movie = input('Digite o código do movie, conforme listado na barra de endereço do site https://www.adorocinema.com/: ')
n = int(input('Digite quantas páginas de comentários você deseja consultar: '))
crawler = AdoroCinema()

movieName = crawler.extrairmovieName(movie)

sinopse = crawler.extrairSinopsemovie(movie)
crawler.salvarSinopsemovie(movie, sinopse)

comentarios = crawler.extrairComentariosmovie(movie, n)
crawler.salvarComentariosmovie(movie, comentarios)

positives, negatives, totalComents = crawler.countPositiveNegative(movie)

percentPositives = positives / totalComents

percentNegatives = negatives / totalComents
print('')
print(f"nome do movie: {movieName}")
print(f"total de comentários lidos: {totalComents}")
print(f"words positivas: {positives} (percentual: {percentPositives:.2%})")
print(f"words negativas: {negatives} (percentual: {percentNegatives:.2%})")
print('Programa executado com sucesso. Consulte os arquivos gerados com a sinopse e os comentários do movie.')

crawler.storeResults(movieName, totalComents, percentPositives, percentNegatives)