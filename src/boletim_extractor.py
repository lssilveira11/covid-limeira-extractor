#https://blog.codeexpertslearning.com.br/lendo-imagens-uma-abordagem-%C3%A0-ocr-com-google-tesseract-e-python-ee8e8009f2ab
#https://stackoverflow.com/questions/43403086/opening-image-file-from-url-with-pil-for-text-recognition-with-pytesseract
#https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c
#http://pythonclub.com.br/extraindo-texto-de-imagens-com-python.html

# baixar a imagem do site
import requests
import io
import numpy as np

from PIL import Image
import pytesseract
import cv2

def transform_binimage(img):
  # tipando a leitura para os canais de ordem RGB
  imagem = img.convert('RGB')

  # convertendo em um array editável de numpy[x, y, CANALS]
  npimagem = np.asarray(imagem).astype(np.uint8)  

  # diminuição dos ruidos antes da binarização
  npimagem[:, :, 0] = 0 # zerando o canal R (RED)
  #npimagem[:, :, 1] = 0 # zerando o canal G (GREEN)
  #npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

  # atribuição em escala de cinza
  im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

  # aplicação da truncagem binária para a intensidade
  # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
  # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
  # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
  ret, thresh = cv2.threshold(im, 245, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

  # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
  binimagem = Image.fromarray(thresh) 
  return binimagem

def img_to_text(img):
  text = pytesseract.image_to_string( img, lang='por' )
  return text.strip()

def extract_str(img):
  binimagem = transform_binimage(img)
  img_text = img_to_text(binimagem) 
  return img_text.upper()

def extract_title(img):
  crop = img.crop((0, 0, 810, 70))
  return extract_str(crop)

#*******************************************************************************
def extract_confirmados(img):
  crop = img.crop((60, 196, 162, 248))
  return extract_str(crop)

def extract_obitos_confirmados(img):
  crop = img.crop((320, 197, 413, 222))
  return (extract_str(crop))

def extract_recuperados(img):
  crop = img.crop((320, 226, 413, 251))
  return extract_str(crop)

def extract_internacoes_confirmados(img):
  crop = img.crop((320, 257, 413, 281))
  return extract_str(crop)

def extract_total_notificacoes(img):
  crop = img.crop((315, 110, 412, 136))
  return extract_str(crop)

def extract_descartados(img):
  crop = img.crop((315, 140, 412, 170))
  return extract_str(crop)

def extract_suspeitos(img):
  crop = img.crop((315, 365, 412, 392))
  return extract_str(crop)

def extract_obitos_suspeitos(img):
  crop = img.crop((315, 394, 420, 430))
  return extract_str(crop)

def extract_ocupacao_urc(img):
  crop = img.crop((703, 200, 787, 228))
  return extract_str(crop)

def extract_boletim(img_url):

  response = requests.get(img_url)

  img = Image.open(io.BytesIO(response.content))  

  title = extract_title(img)

  if (title.find("BOLETIM") == -1):
    return None
  return {
    'confirmados': extract_confirmados(img),
    'obitos_confirmados': extract_obitos_confirmados(img),
    'recuperados': extract_recuperados(img),
    'internacoes_confirmados': extract_internacoes_confirmados(img),
    'total_notificacoes': extract_total_notificacoes(img),
    'descartados': extract_descartados(img),
    'suspeitos': extract_suspeitos(img),
    'obitos_suspeitos': extract_obitos_suspeitos(img),
    'ocupacao_urc': extract_ocupacao_urc(img),
  }

  
# TESTES
# boletim
#img_url = 'https://www.limeira.sp.gov.br/sitenovo/admin/uploads/26e89dbee535bcb1c78ee00940d316ef.jpg'
#img_url = 'https://www.limeira.sp.gov.br/sitenovo/admin/uploads/b8825fdf64285502ff6102a3a3290af6.jpg'
# nao boletim
#img_url = 'https://www.limeira.sp.gov.br/sitenovo/admin/uploads/4a5cf931fd8ee3a620969352a4b1737d.jpg'

#print(extract_boletim(img_url))