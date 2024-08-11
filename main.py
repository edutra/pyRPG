import pygame
import sys
# import tkinter as tk
# from tkinter import simpledialog
import random
from character import Personagem
from structure import Estrutura
from objects import ObjetoInterativo
from ground import Chao
from saver import Saver

# Configurações iniciais
WIDTH_SCREEN = 800
HEIGHT_SCREEN = 600
SIZE_CELL = 40
COLOR_BACKGROUND = (50, 50, 50)
COLOR_GRID = (100, 100, 100)
COLOR_PLAYER = (0, 255, 0)
COLOR_ENEMY = (255, 0, 0)
COLOR_WALL = (139, 69, 19)
COLOR_DOOR = (184, 134, 11)
COLOR_CHEST = (139, 69, 19)
COLOR_GRASS = (136, 153, 102)
COLOR_PEDRA = (146,142,133)
COLOR_LAVA = (255, 69, 0)
COLOR_AGUA = (0, 191, 255)
COLOR_MENU = (200, 200, 200)
COLOR_TEXT = (255, 255, 255)
COLOR_INPUT_BG = (200, 200, 200)
WIDTH_MENU = 200

# Inicializa o pygame
pygame.init()

# Cria a screen principal com a opção de redimensionamento
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)
pygame.display.set_caption("Mapa de RPG de Mesa")



class MapaRPG:
    def __init__(self):
        self.andares = {}
        self.floor_number = 0
        self.init_floor(self.floor_number)
        self.personagens = []
        self.estruturas = []
        self.objetos_interativos = []
        # self.chao = self.inicializar_chao()
        self.inimigos = []

    def init_floor(self, floor_number):
        if floor_number not in self.andares:
            self.andares[floor_number] = {
                "chao": {},
                "estruturas": [],
                "objetos_interativos": [],
                "personagens": [],
                "inimigos": []
            }
            self.inicializar_chao(floor_number)

    def inicializar_chao(self, floor_number):
        chao = {}
        for x in range(0, WIDTH_SCREEN - WIDTH_MENU, SIZE_CELL):
            for y in range(0, HEIGHT_SCREEN, SIZE_CELL):
                posicao_grid = (x + SIZE_CELL // 2, y + SIZE_CELL // 2)
                chao[posicao_grid] = Chao("grama", posicao_grid, COLOR_GRASS)
        self.andares[floor_number]["chao"] = chao
        return chao
    
    def mudar_andar(self, numero_andar):
        print(numero_andar)
        if numero_andar not in self.andares:
            self.init_floor(numero_andar)
        self.floor_number = numero_andar
    
    def adicionar_personagem(self, personagem):
        self.andares[self.floor_number]["personagens"].append(personagem)

    def adicionar_inimigo(self, inimigo):
        self.andares[self.floor_number]["inimigos"].append(inimigo)
    
    def adicionar_estrutura(self, estrutura):
        self.andares[self.floor_number]["estruturas"].append(estrutura)
    
    def adicionar_objeto_interativo(self, objeto):
        self.andares[self.floor_number]["objetos_interativos"].append(objeto)
    
    def modificar_chao(self, posicao_grid, tipo):
        cor = ''
        if tipo == "lava": 
            cor = COLOR_LAVA
        elif tipo == "agua":
            cor = COLOR_AGUA
        elif tipo == "grama":
            cor = COLOR_GRASS
        elif tipo == "pedra":
            cor = COLOR_PEDRA

        novo_chao = Chao(tipo, posicao_grid, cor)
        self.andares[self.floor_number]["chao"][posicao_grid] = novo_chao    
    def desenhar(self, screen):
        andar = self.andares[self.floor_number]
        for chao in andar["chao"].values():
            chao.desenhar(screen)
        for estrutura in andar["estruturas"]:
            estrutura.desenhar(screen)
        for objeto in andar["objetos_interativos"]:
            objeto.desenhar(screen)
        for personagem in andar["personagens"]:
            personagem.desenhar(screen)
        for inimigo in andar["inimigos"]:
            inimigo.desenhar(screen)    

    def desenhar_grid(self, screen):
        for x in range(0, WIDTH_SCREEN - WIDTH_MENU, SIZE_CELL):
            pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, HEIGHT_SCREEN))
        for y in range(0, HEIGHT_SCREEN, SIZE_CELL):
            pygame.draw.line(screen, COLOR_GRID, (0, y), (WIDTH_SCREEN - WIDTH_MENU, y))

    def save(self, screen):
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
                        pygame.display.update()
                    else:
                        input_text += evento.unicode

            # screen.fill(COLOR_BACKGROUND)
            txt_surface = fonte.render(input_text, True, COLOR_TEXT)
            largura_box = max(200, txt_surface.get_width()+10)
            input_box.w = largura_box

            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, COLOR_INPUT_BG, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

    def load(self, screen):
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
                        print("teste ")
                    else:
                        input_text += evento.unicode

            # screen.fill(COLOR_BACKGROUND)
            txt_surface = fonte.render(input_text, True, COLOR_TEXT)
            largura_box = max(200, txt_surface.get_width()+10)
            input_box.w = largura_box

            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, COLOR_INPUT_BG, input_box, 2)

            pygame.display.flip()
            clock.tick(30)
 


def ajustar_para_grid(posicao):
    x, y = posicao
    x = (x // SIZE_CELL) * SIZE_CELL + SIZE_CELL // 2
    y = (y // SIZE_CELL) * SIZE_CELL + SIZE_CELL // 2
    return (x, y)

# Função para desenhar o menu
def desenhar_menu(screen, submenu=None):
    pygame.draw.rect(screen, COLOR_MENU, (WIDTH_SCREEN - WIDTH_MENU, 0, WIDTH_MENU, HEIGHT_SCREEN))
    fonte = pygame.font.SysFont(None, 36)
    texto_player = fonte.render('Adicionar Player', True, (0, 0, 0))
    texto_inimigo = fonte.render('Adicionar Inimigo', True, (0, 0, 0))
    texto_estrutura = fonte.render('Adicionar Estrutura', True, (0, 0, 0))
    texto_objeto = fonte.render('Adicionar Objeto', True, (0, 0, 0))
    texto_chao = fonte.render('Modificar Chão', True, (0, 0, 0))
    texto_remover = fonte.render('Remover', True, (0, 0, 0))
    
    screen.blit(texto_player, (WIDTH_SCREEN - WIDTH_MENU + 20, 20))
    screen.blit(texto_inimigo, (WIDTH_SCREEN - WIDTH_MENU + 20, 80))
    screen.blit(texto_estrutura, (WIDTH_SCREEN - WIDTH_MENU + 20, 140))
    screen.blit(texto_objeto, (WIDTH_SCREEN - WIDTH_MENU + 20, 200))
    screen.blit(texto_chao, (WIDTH_SCREEN - WIDTH_MENU + 20, 260))
    screen.blit(texto_remover, (WIDTH_SCREEN - WIDTH_MENU + 20, 320))
    
    if submenu == "estrutura":
        texto_parede = fonte.render('Adicionar Parede', True, (0, 0, 0))
        texto_porta = fonte.render('Adicionar Porta', True, (0, 0, 0))
        screen.blit(texto_parede, (WIDTH_SCREEN - WIDTH_MENU + 20, 380))
        screen.blit(texto_porta, (WIDTH_SCREEN - WIDTH_MENU + 20, 440))
    elif submenu == "objeto":
        texto_bau = fonte.render('Adicionar Baú', True, (0, 0, 0))
        screen.blit(texto_bau, (WIDTH_SCREEN - WIDTH_MENU + 20, 380))
    elif submenu == "chao":
        texto_lava = fonte.render('Lava', True, (0, 0, 0))
        texto_agua = fonte.render('Água', True, (0, 0, 0))
        texto_grama = fonte.render('Grama', True, (0, 0, 0))
        texto_pedra = fonte.render('Pedra', True, (0, 0, 0))
        screen.blit(texto_lava, (WIDTH_SCREEN - WIDTH_MENU + 20, 380))
        screen.blit(texto_agua, (WIDTH_SCREEN - WIDTH_MENU + 20, 440))
        screen.blit(texto_grama, (WIDTH_SCREEN - WIDTH_MENU + 20, 500))
        screen.blit(texto_pedra, (WIDTH_SCREEN - WIDTH_MENU + 20, 560))


# Função para detectar clique no menu
def checar_clique_menu(posicao_mouse, submenu=None):
    if posicao_mouse[0] > WIDTH_SCREEN - WIDTH_MENU:
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

                    mapa.adicionar_personagem(Personagem(input_text, posicao_grid, COLOR_PLAYER))
                    active = False
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += evento.unicode

        # screen.fill(COLOR_BACKGROUND)
        txt_surface = fonte.render(input_text, True, COLOR_TEXT)
        largura_box = max(200, txt_surface.get_width()+10)
        input_box.w = largura_box

        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, COLOR_INPUT_BG, input_box, 2)

        pygame.display.flip()
        clock.tick(30)




def rolar_dado(screen):
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

        # screen.fill(COLOR_BACKGROUND)
        txt_surface = fonte.render(input_text, True, COLOR_TEXT)
        largura_box = max(200, txt_surface.get_width()+10)
        input_box.w = largura_box

        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, COLOR_INPUT_BG, input_box, 2)

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
        # Atualiza as dimensões da screen
        WIDTH_SCREEN, HEIGHT_SCREEN = evento.size
        screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)
        mapa.inicializar_chao()

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
                create_character(posicao_grid)
                # mapa.adicionar_personagem(Personagem(f"Jogador{len(mapa.personagens) + 1}", posicao_grid, COLOR_PLAYER))
                modo = None
            elif modo == "inimigo":
                mapa.adicionar_inimigo(Personagem(f"Inimigo{len(mapa.inimigos) + 1}", posicao_grid, COLOR_ENEMY))
                modo = None
            elif modo == "parede":
                mapa.adicionar_estrutura(Estrutura("Parede", posicao_grid, COLOR_WALL))
            elif modo == "porta":
                mapa.adicionar_estrutura(Estrutura("Porta", posicao_grid, COLOR_DOOR))
                modo = None
            elif modo == "bau":
                mapa.adicionar_objeto_interativo(ObjetoInterativo("Baú", posicao_grid, COLOR_CHEST))
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
            rolar_dado(screen)
        elif evento.key == pygame.K_c:
            modo = "player"
        elif evento.key == pygame.K_e:
            modo = "inimigo"
        elif evento.key == pygame.K_s:
            mapa.save(screen)
        elif evento.key == pygame.K_l:
            mapa.load(screen)
        elif evento.key == pygame.K_x:
            remover_estrutura_ou_objeto(mapa, posicao_grid)
        elif evento.key == pygame.K_UP:  # Muda para andar superior
            mapa.mudar_andar(mapa.floor_number + 1)
        elif evento.key == pygame.K_DOWN:  # Muda para andar inferior
            mapa.mudar_andar(mapa.floor_number - 1)


    # Preenche o fundo
    screen.fill(COLOR_BACKGROUND)
       
    # Desenha os personagens, estruturas e objetos interativos
    mapa.desenhar(screen)
     
    # Desenha o grid
    mapa.desenhar_grid(screen)

    # Desenha o menu
    desenhar_menu(screen, submenu_ativo)
    
    # Atualiza a screen
    pygame.display.flip()

