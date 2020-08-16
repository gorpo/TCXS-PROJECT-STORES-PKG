import  os
import pathlib
import sqlite3
from bs4 import BeautifulSoup


#variavies iniciais
dados = open('base.html', 'r', encoding="utf-8").read()
dados= BeautifulSoup(dados, 'html5lib')
key_titulo = dados.find_all('p', {'class':'textoJogoPS3'})
key_imagem = dados.find_all('img')
key_links = dados.find_all('button', {'class':'botaoDownloadPS3'})
key_contentID = dados.find_all('button', {'class':'botaoDownloadPS3'})



titulos = []
for titulo in key_titulo:
    titulo = str(titulo).split("<br/>")[0].split("Jogo:  ")[1]
    titulos.append(titulo)
    #print(titulo)

imagens = []
for imagem in key_imagem:
    try:
        imagem = str(imagem).split('ps3/')[1].replace('"/>', '')
        imagens.append(imagem)
        #print(imagem)
    except Exception as e:
        pass

links = []
for link in key_links:
    link = str(link).split("href='")[1].split("';")[0]
    links.append(link)
    #print(link)


ids = []
for id in key_contentID:
    try:
        id = str(id).split("href='")[1].split("';")[0].split('/')[5].split('.')[0]
        ids.append(id)
        #print(id)
    except Exception as e:
        #print(e)
        ids.append('ARRUMAR')


dicionario_jogos = list(zip(list(titulos), list(imagens), list(links), list(ids)))#--


with open(f"{imagens[0][0:-4]}.xml",'a') as arquivo:
    texto0 = """<XMBML version="1.0">
    <View id="tcxs_items">
        <Attributes>"""
    arquivo.write(texto0)

    for i in  range(len(links)):
        titulo = titulos[0]
        imagem = imagens[0]
        link = links[i]
        contentId = ids[i]
        print(imagem, titulo, link, contentId)
        texto1 = f"""
            <!-- id:{i} | PlayStation PS3 | TCXS PROJECT 2020 | {titulo.upper()} -->
            <Table key="tcxs_{i}">
                <Pair key="icon"><String>/dev_hdd0/game/HENBSTORE/USRDIR/IMAGES/ps3/{imagem}</String></Pair>
                <Pair key="title"><String>Jogo: {titulo}</String></Pair>
                <Pair key="info"><String>Idioma do Jogo: INGLES | DUBLADO/LEGENDADO)</String></Pair>
            </Table>"""
        arquivo.write(texto1)

    texto2 = """
        </Attributes>
        <Items>"""
    arquivo.write(texto2)

    for i in range(len(links)):
        texto3 = f"""
                <Query class="type:x-xmb/folder-pixmap" key="tcxs_{i}" attr="tcxs_{i}" src="#tcxs_{i}_link" />"""
        arquivo.write(texto3)

    texto4 = """
		</Items>
	</View>"""
    arquivo.write(texto4)
    for i in  range(len(links)):
        titulo = titulos[0]
        imagem = imagens[0]
        link = links[i]
        contentId = ids[i]
        print(imagem, titulo, link, contentId)


        texto5 = f"""
        <View id="tcxs_{i}_link">
            <Attributes>
                <Table key="tcxs_download{i}">
                    <Pair key="info"><String>net_package_install</String></Pair>
                    <Pair key="pkg_src"><String>{link}</String></Pair>
                    <Pair key="pkg_src_qa"><String>{link}</String></Pair>
                    <Pair key="content_name"><String>tool_pkg_install_pc</String></Pair>
                    <Pair key="content_id"><String>{contentId}</String></Pair>
                    <Pair key="prod_pict_path"><String>/dev_hdd0/game/HENBSTORE/USRDIR/IMAGES/ps3/{imagem}</String></Pair>
                </Table>
            </Attributes>
            <Items><Item class="type:x-xmb/xmlnpsignup" key="tcxs_download{i}" attr="tcxs_download{i}" /></Items>
        </View>"""
        arquivo.write(texto5)

    arquivo.write('</XMBML>')

arquivo.close()


