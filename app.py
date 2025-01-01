from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random


def gerar_caracteres_captcha(tamanho=6, incluir_especiais=True):
    caracteres = "ABCÇDEFGHJKMNPQRSTUVWXYZabcçdefghjkmnpqrstuvwxyz2346789"
    if incluir_especiais:
      caracteres += "#$%&*@" #ou outros que vc preferir
    return "".join(random.choice(caracteres) for _ in range(tamanho))

def gerar_caracteres_fake_captcha(tamanho=6, incluir_especiais=True):
    caracteres = ""
    if incluir_especiais:
      caracteres += "℉©™®℃" #ou outros que vc preferir
    return "".join(random.choice(caracteres) for _ in range(tamanho))

def texto_com_posicoes_aleatorias(texto, fonte, largura, altura, cor=(0, 0, 0)):

    img_final = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)) # Imagem final transparente

    posicoes = []
    x_atual = 10 # Posição inicial X (margem esquerda)
    for caractere in texto:
        bbox = ImageDraw.Draw(Image.new("RGBA", (0, 0))).textbbox((0, 0), caractere, font=fonte)
        largura_caractere = bbox[2] - bbox[0]
        altura_caractere = bbox[3] - bbox[0]

        # Cálculo corrigido da posição Y
        y_max = altura - altura_caractere
        y_caractere = random.randint(0, y_max) if y_max > 0 else 0

        img_caractere = Image.new("RGBA", (largura_caractere, altura_caractere), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_caractere)
        draw.text((0, 0), caractere, font=fonte, fill=cor)

        img_final.paste(img_caractere, (x_atual, y_caractere), img_caractere)

        # Atualiza a posição X para o próximo caractere, adicionando um pequeno espaço
        x_atual += largura_caractere + random.randint(2, 8)  # Espaçamento aleatório entre letras

    return img_final

def texto_fake_com_posicoes_aleatorias(texto, fonte, largura, altura, cor=(0, 0, 0)):

    img_final = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)) # Imagem final transparente

    posicoes = []
    x_atual = 10 # Posição inicial X (margem esquerda)
    for caractere in texto:
        bbox = ImageDraw.Draw(Image.new("RGBA", (0, 0))).textbbox((0, 0), caractere, font=fonte)
        largura_caractere = bbox[2] - bbox[0]
        altura_caractere = bbox[3] - bbox[0]

        # Gera uma posição Y aleatória para CADA caractere
        # y_caractere = random.randint(0, altura - altura_caractere) if altura > altura_caractere else 0

        # Cálculo corrigido da posição Y
        y_max = altura - altura_caractere
        y_caractere = random.randint(0, y_max) if y_max > 0 else 0

        img_caractere = Image.new("RGBA", (largura_caractere, altura_caractere), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_caractere)
        draw.text((0, 0), caractere, font=fonte, fill=cor)

        img_final.paste(img_caractere, (x_atual, y_caractere), img_caractere)

        # Atualiza a posição X para o próximo caractere, adicionando um pequeno espaço
        x_atual += largura_caractere + random.randint(3, 9)  # Espaçamento aleatório entre letras

    return img_final

def adicionar_ruido(imagem, quantidade_pontos=500, cor_min=(0, 0, 0), cor_max=(255, 255, 255)):
    draw = ImageDraw.Draw(imagem)
    largura, altura = imagem.size
    for _ in range(quantidade_pontos):
        x = random.randint(0, largura - 1)
        y = random.randint(0, altura - 1)
        cor = (
            random.randint(cor_min[0], cor_max[0]),
            random.randint(cor_min[1], cor_max[1]),
            random.randint(cor_min[2], cor_max[2]),
        )
        draw.point((x, y), fill=cor)
    return imagem

def adicionar_linhas(imagem):
    draw = ImageDraw.Draw(imagem)
    largura, altura = imagem.size
    for _ in range(random.randint(7, 15)):  # Adiciona entre 2 e 5 linhas
        x1 = random.randint(0, largura)
        y1 = random.randint(0, altura)
        x2 = random.randint(0, largura)
        y2 = random.randint(0, altura)
        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=1)
    return imagem

def adicionar_ruido_sal_pimenta(imagem, probabilidade=0.03):
    imagem_np = np.array(imagem)
    altura, largura, canais = imagem_np.shape
    for y in range(altura):
        for x in range(largura):
            if random.random() < probabilidade:
                if random.random() < 0.5:
                    imagem_np[y, x] = [255, 255, 255] #sal
                else:
                    imagem_np[y, x] = [0, 0, 0] #pimenta
    return Image.fromarray(imagem_np)

def adicionar_ruido_gaussiano(imagem, intensidade=1):
    try:
        # Converte a imagem para um array NumPy
        imagem_np = np.array(imagem)

        # Obtém as dimensões da imagem e o número de canais de cor
        altura, largura, canais = imagem_np.shape

        # Gera ruído gaussiano com média 0 e desvio padrão 'intensidade'
        ruido = np.random.normal(0, intensidade, (altura, largura, canais)).astype(np.uint8)

        # Adiciona o ruído à imagem
        imagem_com_ruido = np.clip(imagem_np + ruido, 0, 255).astype(np.uint8) #climp garante que os valores dos pixels fiquem entre 0 e 255

        # Converte o array NumPy de volta para um objeto PIL Image
        imagem_com_ruido_pil = Image.fromarray(imagem_com_ruido)

        return imagem_com_ruido_pil
    except Exception as e:
        print(f"Erro ao adicionar ruído gaussiano: {e}")
        return None

# Parametros
altura = 100
largura = 200
fonte = ImageFont.truetype("sources/DejaVuSans.ttf", 30)
# Gera um texto aleatório para o CAPTCHA
texto = gerar_caracteres_captcha(6)
texto_fake = gerar_caracteres_fake_captcha(4)

print(f"Texto Captcha: {texto}")
print(f"Texto Fake Captcha: {texto_fake}")

# Calcula o tamanho necessário para a imagem base (com margem)
largura_necessaria = largura + 20
altura_necessaria = altura + 20

imagem_texto_valido = texto_com_posicoes_aleatorias(texto, fonte, largura, altura)

imagem_texto_fake = texto_fake_com_posicoes_aleatorias(texto_fake, fonte, largura, altura, cor=(223, 45, 128))

imagem_base = Image.new('RGB', (largura_necessaria, altura_necessaria), (255, 255, 255))
 
imagem_base.paste(imagem_texto_valido, (0,0), imagem_texto_valido)

# Adiciona ruído à imagem base

#imagem_base.paste(imagem_texto_fake, (0,0), imagem_texto_fake)

imagem_base = adicionar_linhas(imagem_base)

#imagem_base = adicionar_ruido_sal_pimenta(imagem_base)

imagem_base = adicionar_ruido_gaussiano(imagem_base)

imagem_base = adicionar_ruido(imagem_base, quantidade_pontos=5000)

# Gera a imagem final
imagem_base.save("captcha.png")

