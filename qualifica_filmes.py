import requests
from bs4 import BeautifulSoup

class AdoroCinema:
    def extrairNomeFilme(self, filme):
        url = "https://www.adorocinema.com/filmes/" + filme +'/'
        htmlFilme = requests.get(url).text
        bsS = BeautifulSoup(htmlFilme, 'html.parser')
        nome = bsS.find('div', class_="titlebar-title titlebar-title-lg").get_text(strip=True)
        return nome
    

    def extrairSinopseFilme (self, filme):      
        url = "https://www.adorocinema.com/filmes/" + filme +'/'
        htmlFilme = requests.get(url).text
        bsS = BeautifulSoup(htmlFilme, 'html.parser')
        sinopse = bsS.find('div', class_="content-txt").get_text(strip=True)
        return sinopse
    
    def salvarSinopseFilme(self, filme, sinopse):
        arq_saida = open(filme+'_sinopse.txt', 'w',encoding='utf-8')
        for line in sinopse:
            arq_saida.write(line)
        arq_saida.close()

    def extrairComentariosFilme(self, filme, n):
        comentarios = []
        for i in range(1,n+1):
            url = 'http://www.adorocinema.com/filmes/' + filme + '/criticas/espectadores/?page=' + str(i)
            htmlComentarios = requests.get(url).text
            bsC = BeautifulSoup(htmlComentarios, 'html.parser')
            comentarios_com_tags = bsC.find_all('div', class_="content-txt review-card-content")
            for comentario_com_tag in comentarios_com_tags:
                comentarios.append(comentario_com_tag.get_text().strip())
        return comentarios

    def salvarComentariosFilme(self, filme, comentarios):
        arq_saida = open(filme+'_comentarios.txt', 'w', encoding='utf-8')
        for comentario in comentarios:
            arq_saida.write(comentario + '\n')
        arq_saida.close()
    
    # Função que recebe o nome do arquivo de comentários do filme, lê cada line do arquivo e
    # Verifica se contém words positivas ou negativas a partir de listas predefinidas de words.
    def contabilizaPositivoNegativo(self, filme):
        # Abre o arquivo para leitura
        with open(filme + '_comentarios.txt', 'r', encoding='utf-8') as arq_entrada:
            # Inicialize contadores
            positives = 0
            negatives = 0
            totalComents = 0

            # Lista de words positivas e negativas
            words_positives = ["bom", "ótimo", "excelente", "fascinante", "inspirador", "emocionante", "comovente", "divertido", "engraçado", "hilário", "sensacional", "fantástico", "maravilhoso", "arrebatador", "brilhante", "notável", "empolgante", "encantador", "Incrível", "bela", "belo", "belíssimo", "belíssima", "lindo", "linda", "maravilhoso", "maravilhosa", "ótimo", "ótima", "ótimo", "ótima", "excelente", "arrebatador","brilhante","notável","empolgante","encantador", "incrível"]
            words_negatives = ["ruim", "péssimo", "horrível","terrível","desapontante","fraco","previsível","chato","confuso","medíocre","doloroso","insuportável","ridículo","desastroso","desagradável","desanimador","desapontante","desconfortável"]

            # Loop pelas lines do arquivo
            for line in arq_entrada:
                # Transforme a line em minúsculas para evitar problemas de capitalização
                line = line.lower()
                totalComents += 1
                # Verifique words positivas
                for word in words_positives:
                    if word in line:
                        positives += 1
                        break  # Saia do loop interno se uma word positiva for encontrada

                # Verifique words negativas
                for word in words_negatives:
                    if word in line:
                        negatives += 1
                        break  # Saia do loop interno se uma word negativa for encontrada

        # Retorne os resultados
        return positives, negatives, totalComents


filme = input('Digite o código do filme, conforme listado na barra de endereço do site https://www.adorocinema.com/: ')
n = int(input('Digite quantas páginas de comentários você deseja consultar: '))
crawler = AdoroCinema()

sinopse = crawler.extrairSinopseFilme(filme)
crawler.salvarSinopseFilme(filme, sinopse)

comentarios = crawler.extrairComentariosFilme(filme, n)
crawler.salvarComentariosFilme(filme, comentarios)

positives, negatives, totalComents = crawler.contabilizaPositivoNegativo(filme)

percentPositives = positives / totalComents

percentNegatives = negatives / totalComents
print('')
print(f"nome do filme: {crawler.extrairNomeFilme(filme)}")
print(f"total de comentários lidos: {totalComents}")
print(f"words positivas: {positives} (percentual: {percentPositives:.2%})")
print(f"words negativas: {negatives} (percentual: {percentNegatives:.2%})")
print('Programa executado com sucesso. Consulte os arquivos gerados com a sinopse e os comentários do filme.')