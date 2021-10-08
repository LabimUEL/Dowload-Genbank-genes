import re
### Expressao regular para obter numero de acesso do genoma de onde o gene foi tirado
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
### Gerenciador de navegador
import pyautogui as pya
### Automatizar comandos de teclado e mouse
from subprocess import call
import time
import os
import sys

### Acessar lista de genes
### passar sobre todos em cada linha

nf_genes = []  # Not Found genes
df_genes = []  # Download Failed genes


with open(sys.argv[1]) as lista:
    for l in lista:
        if not l.lstrip().startswith('#'):
            l_strip = l.strip() #retira caracteres especiais das string, evitando problemas
            nav = webdriver.Chrome('/home/labim/Documentos/chromedriver')
            nav.get("https://www.ncbi.nlm.nih.gov/gene/advanced") ### Determina o site para o navegador
            nav.find_element_by_xpath('//*[@id="fv_0"]').send_keys(l_strip)
            nav.find_element_by_xpath('//*[@id="ff_1"]/option[26]').click()
            nav.find_element_by_xpath('//*[@id="fv_1"]').send_keys("bacteria")
            nav.find_element_by_xpath('//*[@id="search"]').click() ### coloca o nome do gene na barra de pesquisa
            ### determina na categoria Organisms o termo bacteria
            try:
                nav.find_element_by_xpath('//*[@id="ui-ncbigrid-7"]/tbody/tr[1]/td[1]/div[2]/a/span').click()
                ### Entra no primeiro gene encontrado da lista de resultados 
            except NoSuchElementException as e:
                print(e)
                print("Gene not found!!", l_strip)
                nf_genes.append(l_strip)
                nav.close()
                continue            
            else:
                acces = nav.find_element_by_xpath('//*[@id="single-gen-accession"]').get_attribute('data-accession')
            ### Este bloco faz com que o codigo reinicie apos um erro neste passo
            num = re.search("[A-Z]+[_][A-Z0-9]*[^.]", acces).group(0)
            quote = "\""+num+"\""
            ### Obtem o numero de acesso da bacteria
            ### Coloca o numero de acesso na variavel acces
            ### Regex retira as outras infos do valor em acces e atribui ao objeto "num"
            ### Adiciona aspas para encaixar no meio do xpath necessário para acessar a pagina de download
            nav.find_element_by_xpath("//*[@id="+quote+"]/div/p/a[2]").click()
            ### Entra na pagina FASTA Nucleotides para baixar a sequencia 
            try:
                nav.find_element_by_xpath('//*[@id="seqsendto"]/a').click()
            except NoSuchElementException as e:
                print(e)
                print("Impossible to download the gene", l_strip)
                df_genes.append(l_strip)
                nav.close()
                continue            
            else:
                time.sleep(2)
            #time.sleep(2)
            nav.find_element_by_xpath('//*[@id="submenu_complete_rec"]/fieldset/ul/li[1]/label').click()
            time.sleep(2)
            nav.find_element_by_xpath('//*[@id="file_format"]/option[4]').click()
            time.sleep(2)
            nav.find_element_by_xpath('//*[@id="submenu_File"]/button').click() ### Baixa a sequencia fasta em Downloads/
            time.sleep(5)
            nav.close()
            
            ### Este bloco adiciona o nome do gene baixado no lugar do seu numero de acesso no cabeçalho
            sequence = open('/home/labim/Downloads/sequence.fasta', "r")
            sequence_out = open('/home/labim/Downloads/sequence_out.fasta', "w")
            for linha in sequence:
                if linha.lstrip().startswith('>'):
                    ID = re.search("[A-Z]+[_][A-Z0-9]*[^.]", str(linha)).group(0)
                    sequence_out.write(linha.replace(str(ID), l_strip+" "))
                else:
                    sequence_out.write(linha)
            sequence.close()
            sequence_out.close()
            
            sequence_out = open('/home/labim/Downloads/sequence_out.fasta')
            for i in sequence_out:
                if i.lstrip().startswith('>'):
                    corte = i.split(", complete sequence")
                    spp = re.search("[A-z]+[ ][a-z]+", str(corte)).group(0)
                    spp_espaco = spp.replace(" ", "_")
                    print(spp_espaco)            
                    novo_nome = l_strip+"_"+spp_espaco
            ### abre o arquivo recem baixado
            ### retira o termo ", complete sequence" da string para não atrapalhar o regex
            ### obtem o nome da bacteria por regex, retira os espaços e substitui por "_"
            ### cria o nome do arquivo com nome do gene e organismo de origem

            os.rename(r'/home/labim/Downloads/sequence_out.fasta',r'/home/labim/Downloads/'+novo_nome+'.fasta')
            cmd = 'mv /home/labim/Downloads/'+novo_nome+'.fasta /home/labim/Documentos/Genes/Mining/'+novo_nome+'.fasta'
            call(cmd, shell=True)
            ### Renomeia o arquivo com o nome do gene e o nome da bacteria e move para uma pasta especifica

            
print("Estes genes nao foram encontrados:")
print(nf_genes)

print("Nao foi possivel baixar estes genes:")
print(df_genes)
        
