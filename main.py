import pygame
import sys
# import tkinter as tk
# from tkinter import simpledialog
import random
import json
from character import Personagem
from structure import Estrutura
from objects import ObjetoInterativo
from ground import Chao
from saver import Saver

# Configurações iniciais
LARGURA_TELA = 800
ALTURA_TELA = 600
TAMANHO_CELULA = 40
COR_FUNDO = (50, 50, 50)
COR_GRID = (100, 100, 100)
COR_PLAYER = (0, 255, 0)
COR_INIMIGO = (255, 0, 0)
COR_PAREDE = (139, 69, 19)
COR_PORTA = (184, 134, 11)
COR_BAU = (139, 69, 19)
COR_GRAMA = (136, 153, 102)
COR_PEDRA = (146,142,133)
COR_LAVA = (255, 69, 0)
COR_AGUA = (0, 191, 255)
COR_MENU = (200, 200, 200)
COR_TEXTO = (255, 255, 255)
COR_INPUT_BG = (200, 200, 200)
LARGURA_MENU = 200

# Inicializa o pygame
pygame.init()

# Cria a tela principal com a opção de redimensionamento
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.RESIZABLE)
pygame.display.set_caption("Mapa de RPG de Mesa")



class MapaRPG:
    def __init__(self):
        self.personagens = []
        self.estruturas = []
        self.objetos_interativos = []
        self.chao = self.inicializar_chao()
        self.inimigos = []

    def inicializar_chao(self):
        chao = {}
        for x in range(0, LARGURA_TELA - LARGURA_MENU, TAMANHO_CELULA):
            for y in range(0, ALTURA_TELA, TAMANHO_CELULA):
                posicao_grid = (x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)
                chao[posicao_grid] = Chao("grama", posicao_grid, COR_GRAMA)
        return chao
    
    def adicionar_personagem(self, personagem):
        self.personagens.append(personagem)

    def adicionar_inimigo(self, inimigo):
        self.inimigos.append(inimigo)
    
    def adicionar_estrutura(self, estrutura):
        self.estruturas.append(estrutura)
    
    def adicionar_objeto_interativo(self, objeto):
        self.objetos_interativos.append(objeto)
    
    def modificar_chao(self, posicao_grid, tipo):
        cor = ''
        if tipo == "lava": 
            cor = COR_LAVA
        elif tipo == "agua":
            cor = COR_AGUA
        elif tipo == "grama":
            cor = COR_GRAMA
        elif tipo == "pedra":
            cor = COR_PEDRA

        self.chao[posicao_grid] = Chao(tipo, posicao_grid, cor)
    
    def desenhar(self, tela):
        for chao in self.chao.values():
            chao.desenhar(tela)
        for estrutura in self.estruturas:
            estrutura.desenhar(tela)
        for objeto in self.objetos_interativos:
            objeto.desenhar(tela)
        for personagem in self.personagens:
            personagem.desenhar(tela)
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
    
    def desenhar_grid(self, tela):
        for x in range(0, LARGURA_TELA - LARGURA_MENU, TAMANHO_CELULA):
            pygame.draw.line(tela, COR_GRID, (x, 0), (x, ALTURA_TELA))
        for y in range(0, ALTURA_TELA, TAMANHO_CELULA):
            pygame.draw.line(tela, COR_GRID, (0, y), (LARGURA_TELA - LARGURA_MENU, y))

    def save(self, tela):
        input_box = pygame.Rect(100, 100, 140, 32)
        fonte = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_text = ''
        active = True

        while active:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        Saver.salvar_mapa(input_text, self.personagens, self.estruturas, self.objetos_interativos, self.chao, self.inimigos) 
                        active = False
                    elif evento.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += evento.unicode

            # tela.fill(COR_FUNDO)
            txt_surface = fonte.render(input_text, True, COR_TEXTO)
            largura_box = max(200, txt_surface.get_width()+10)
            input_box.w = largura_box

            tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(tela, COR_INPUT_BG, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

    def load(self, tela):
        input_box = pygame.Rect(100, 100, 140, 32)
        fonte = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_text = ''
        active = True

        while active:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        chars, self.estruturas, self.objetos_interativos, self.chao, inimigos =Saver.carregar_mapa(input_text)

                        self.personagens = chars[0]
                        self.inimigos = inimigos[0]

                        active = False
                    elif evento.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += evento.unicode

            # tela.fill(COR_FUNDO)
            txt_surface = fonte.render(input_text, True, COR_TEXTO)
            largura_box = max(200, txt_surface.get_width()+10)
            input_box.w = largura_box

            tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(tela, COR_INPUT_BG, input_box, 2)

            pygame.display.flip()
            clock.tick(30)
 


def ajustar_para_grid(posicao):
    x, y = posicao
    x = (x // TAMANHO_CELULA) * TAMANHO_CELULA + TAMANHO_CELULA // 2
    y = (y // TAMANHO_CELULA) * TAMANHO_CELULA + TAMANHO_CELULA // 2
    return (x, y)

# Função para desenhar o menu
def desenhar_menu(tela, submenu=None):
    pygame.draw.rect(tela, COR_MENU, (LARGURA_TELA - LARGURA_MENU, 0, LARGURA_MENU, ALTURA_TELA))
    fonte = pygame.font.SysFont(None, 36)
    texto_player = fonte.render('Adicionar Player', True, (0, 0, 0))
    texto_inimigo = fonte.render('Adicionar Inimigo', True, (0, 0, 0))
    texto_estrutura = fonte.render('Adicionar Estrutura', True, (0, 0, 0))
    texto_objeto = fonte.render('Adicionar Objeto', True, (0, 0, 0))
    texto_chao = fonte.render('Modificar Chão', True, (0, 0, 0))
    texto_remover = fonte.render('Remover', True, (0, 0, 0))
    
    tela.blit(texto_player, (LARGURA_TELA - LARGURA_MENU + 20, 20))
    tela.blit(texto_inimigo, (LARGURA_TELA - LARGURA_MENU + 20, 80))
    tela.blit(texto_estrutura, (LARGURA_TELA - LARGURA_MENU + 20, 140))
    tela.blit(texto_objeto, (LARGURA_TELA - LARGURA_MENU + 20, 200))
    tela.blit(texto_chao, (LARGURA_TELA - LARGURA_MENU + 20, 260))
    tela.blit(texto_remover, (LARGURA_TELA - LARGURA_MENU + 20, 320))
    
    if submenu == "estrutura":
        texto_parede = fonte.render('Adicionar Parede', True, (0, 0, 0))
        texto_porta = fonte.render('Adicionar Porta', True, (0, 0, 0))
        tela.blit(texto_parede, (LARGURA_TELA - LARGURA_MENU + 20, 380))
        tela.blit(texto_porta, (LARGURA_TELA - LARGURA_MENU + 20, 440))
    elif submenu == "objeto":
        texto_bau = fonte.render('Adicionar Baú', True, (0, 0, 0))
        tela.blit(texto_bau, (LARGURA_TELA - LARGURA_MENU + 20, 380))
    elif submenu == "chao":
        texto_lava = fonte.render('Lava', True, (0, 0, 0))
        texto_agua = fonte.render('Água', True, (0, 0, 0))
        texto_grama = fonte.render('Grama', True, (0, 0, 0))
        texto_pedra = fonte.render('Pedra', True, (0, 0, 0))
        tela.blit(texto_lava, (LARGURA_TELA - LARGURA_MENU + 20, 380))
        tela.blit(texto_agua, (LARGURA_TELA - LARGURA_MENU + 20, 440))
        tela.blit(texto_grama, (LARGURA_TELA - LARGURA_MENU + 20, 500))
        tela.blit(texto_pedra, (LARGURA_TELA - LARGURA_MENU + 20, 560))


# Função para detectar clique no menu
def checar_clique_menu(posicao_mouse, submenu=None):
    if posicao_mouse[0] > LARGURA_TELA - LARGURA_MENU:
        if 20 <= posicao_mouse[1] <= 70:
            return "player"
        elif 80 <= posicao_mouse[1] <= 130:
            return "inimigo"
        elif 140 <= posicao_mouse[1] <= 190:
            return "estrutura"
        elif 200 <= posicao_mouse[1] <= 250:
            return "objeto"
        elif 260 <= posicao_mouse[1] <= 310:
            return "chao"
        elif 320 <= posicao_mouse[1] <= 370:  # Novo caso para remover
            return "remover"
        elif submenu == "estrutura":
            if 380 <= posicao_mouse[1] <= 430:
                return "parede"
            elif 440 <= posicao_mouse[1] <= 490:
                return "porta"
        elif submenu == "objeto":
            if 380 <= posicao_mouse[1] <= 430:
                return "bau"
        elif submenu == "chao":
            if 380 <= posicao_mouse[1] <= 430:
                return "lava"
            elif 440 <= posicao_mouse[1] <= 490:
                return "agua"
            elif 500 <= posicao_mouse[1] <= 550:
                return "grama"
            elif 560 <= posicao_mouse[1] <= 610:
                return "pedra"


    return None

def remover_estrutura_ou_objeto(mapa, posicao_mouse):
    posicao_grid = ajustar_para_grid(posicao_mouse)
    # Remove estruturas ou objetos na posição clicada
    mapa.estruturas = [estrutura for estrutura in mapa.estruturas if estrutura.posicao != posicao_grid]
    mapa.objetos_interativos = [objeto for objeto in mapa.objetos_interativos if objeto.posicao != posicao_grid]
    mapa.personagens = [personagem for personagem in mapa.personagens if personagem.posicao != posicao_grid]
    mapa.inimigos = [inimigo for inimigo in mapa.inimigos if inimigo.posicao != posicao_grid]

def create_character(position_grid, is_player = True):
    input_box = pygame.Rect(100, 100, 140, 32)
    fonte = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_text = ''
    active = True

    while active:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:

                    mapa.adicionar_personagem(Personagem(input_text, posicao_grid, COR_PLAYER))
                    active = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += evento.unicode

        # tela.fill(COR_FUNDO)
        txt_surface = fonte.render(input_text, True, COR_TEXTO)
        largura_box = max(200, txt_surface.get_width()+10)
        input_box.w = largura_box

        tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(tela, COR_INPUT_BG, input_box, 2)

        pygame.display.flip()
        clock.tick(30)




def rolar_dado(tela):
    input_box = pygame.Rect(100, 100, 140, 32)
    fonte = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_text = ''
    active = True

    while active:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if input_text.isdigit() and int(input_text) > 0:
                        resultado = random.randint(1, int(input_text))
                        print(f"Você rolou um dado de {input_text} lados e obteve: {resultado}")
                    else:
                        print("Entrada inválida.")
                    active = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += evento.unicode

        # tela.fill(COR_FUNDO)
        txt_surface = fonte.render(input_text, True, COR_TEXTO)
        largura_box = max(200, txt_surface.get_width()+10)
        input_box.w = largura_box

        tela.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(tela, COR_INPUT_BG, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

# Instancia o mapa
mapa = MapaRPG()

# Controle de arraste e modo
personagem_selecionado = None
modo = None
submenu_ativo = None

# Loop principal do jogo
while True:
    evento = pygame.event.wait()
    if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif evento.type == pygame.VIDEORESIZE:
        # Atualiza as dimensões da tela
        LARGURA_TELA, ALTURA_TELA = evento.size
        tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.RESIZABLE)
    elif evento.type == pygame.MOUSEBUTTONDOWN:
        posicao_mouse = pygame.mouse.get_pos()
        opcao_menu = checar_clique_menu(posicao_mouse, submenu_ativo)

        if opcao_menu:
            if opcao_menu in ["player", "inimigo", "parede", "porta", "bau", "lava", "agua", "grama", "pedra", "remover"]:
                modo = opcao_menu
                submenu_ativo = None
            elif opcao_menu == "estrutura":
                submenu_ativo = "estrutura"
            elif opcao_menu == "objeto":
                submenu_ativo = "objeto"
            elif opcao_menu == "chao":
                submenu_ativo = "chao"
        else:
            posicao_grid = ajustar_para_grid(posicao_mouse)
            if modo == "player":
                mapa.adicionar_personagem(Personagem(f"Jogador{len(mapa.personagens) + 1}", posicao_grid, COR_PLAYER))
                modo = None
            elif modo == "inimigo":
                mapa.adicionar_inimigo(Personagem(f"Inimigo{len(mapa.inimigos) + 1}", posicao_grid, COR_INIMIGO))
                modo = None
            elif modo == "parede":
                mapa.adicionar_estrutura(Estrutura("Parede", posicao_grid, COR_PAREDE))
            elif modo == "porta":
                mapa.adicionar_estrutura(Estrutura("Porta", posicao_grid, COR_PORTA))
                modo = None
            elif modo == "bau":
                mapa.adicionar_objeto_interativo(ObjetoInterativo("Baú", posicao_grid, COR_BAU))
                modo = None
            elif modo in ["lava", "agua", "grama", "pedra"]:
                mapa.modificar_chao(posicao_grid, modo)
            elif modo == "remover":
                remover_estrutura_ou_objeto(mapa, posicao_mouse)
                modo = None
            else:
                for personagem in mapa.personagens + mapa.inimigos:
                    if personagem.checar_clique(posicao_mouse):
                        personagem.arrastando = True
                        personagem_selecionado = personagem
                        break
    elif evento.type == pygame.MOUSEBUTTONUP:
        if evento.button == 3 and modo in ["lava", "agua", "grama", "pedra", "parede"]:  # Botão direito do mouse
            modo = None  # Sai do modo de adicionar parede
        elif personagem_selecionado:
            personagem_selecionado.arrastando = False
            personagem_selecionado.mover(ajustar_para_grid(pygame.mouse.get_pos()))
            personagem_selecionado = None
    elif evento.type == pygame.MOUSEMOTION:
        if personagem_selecionado and personagem_selecionado.arrastando:
            personagem_selecionado.mover(pygame.mouse.get_pos())
    elif evento.type == pygame.KEYDOWN:
        posicao_grid = ajustar_para_grid(pygame.mouse.get_pos())
        if evento.key == pygame.K_z:
            rolar_dado(tela)
        elif evento.key == pygame.K_c:
            create_character(posicao_grid)
        elif evento.key == pygame.K_e:
            mapa.adicionar_inimigo(Personagem(f"Inimigo{len(mapa.inimigos) + 1}", posicao_grid, COR_INIMIGO))
        elif evento.key == pygame.K_s:
            mapa.save(tela)
            # Saver.salvar_mapa("mapa.json", mapa.personagens, mapa.estruturas, mapa.objetos_interativos, mapa.chao, mapa.inimigos)
            # mapa.salvar_mapa("mapa_salvo.json")
        elif evento.key == pygame.K_l:
            mapa.load(tela)
        elif evento.key == pygame.K_x:
            remover_estrutura_ou_objeto(mapa, posicao_grid)

    # Preenche o fundo
    tela.fill(COR_FUNDO)
       
    # Desenha os personagens, estruturas e objetos interativos
    mapa.desenhar(tela)
     
    # Desenha o grid
    mapa.desenhar_grid(tela)

    # Desenha o menu
    desenhar_menu(tela, submenu_ativo)
    
    # Atualiza a tela
    pygame.display.flip()

