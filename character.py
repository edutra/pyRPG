#!/usr/bin/env python3

import json
import pygame

TAMANHO_CELULA = 40
COR_TEXTO = (255, 255, 255)
class Personagem:
    def __init__(self, nome, posicao, cor):
        self.nome = nome
        self.posicao = posicao
        self.cor = cor
        self.raio = TAMANHO_CELULA // 3
        self.arrastando = False
        self.fonte = pygame.font.Font(None, 24)  # Fonte para desenhar o nome

    def desenhar(self, tela):
        # Desenha o círculo que representa o personagem
        pygame.draw.circle(tela, self.cor, self.posicao, self.raio)

        # Renderiza o nome do personagem
        texto_nome = self.fonte.render(self.nome, True, COR_TEXTO)
        pos_texto = (self.posicao[0] - texto_nome.get_width() // 2, self.posicao[1] - self.raio - 20)
        tela.blit(texto_nome, pos_texto)

    def mover(self, nova_posicao):
        self.posicao = nova_posicao

    def checar_clique(self, posicao_mouse):
        dx = self.posicao[0] - posicao_mouse[0]
        dy = self.posicao[1] - posicao_mouse[1]
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        return distancia <= self.raio

    def to_dict(self):
        return {
            "nome": self.nome,
            "posicao": self.posicao,
            "cor": self.cor,
        }

    @staticmethod
    def from_dict(data):
        return Personagem(data["nome"], tuple(data["posicao"]), data["cor"])
