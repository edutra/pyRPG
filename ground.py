#!/usr/bin/env python3

import json
import pygame

TAMANHO_CELULA = 40
class Chao:
    def __init__(self, tipo, posicao, cor):
        self.tipo = tipo
        self.posicao = posicao
        self.cor = cor
        self.altura = TAMANHO_CELULA
        self.largura = TAMANHO_CELULA
    def desenhar(self, tela):
        image = None
        if self.tipo == 'grama':
                image = pygame.transform.scale(pygame.image.load('assets/grass.png').convert_alpha(), (self.largura, self.altura))
        elif self.tipo == 'agua':
                 image = pygame.transform.scale(pygame.image.load('assets/water.png').convert_alpha(), (self.largura, self.altura))
        elif self.tipo == 'lava':
                 image = pygame.transform.scale(pygame.image.load('assets/lava.png').convert_alpha(), (self.largura, self.altura))
        elif self.tipo == 'pedra':
                 image = pygame.transform.scale(pygame.image.load('assets/stone.png').convert_alpha(), (self.largura, self.altura))

        tela.blit(image, (self.posicao[0] - self.largura // 2, self.posicao[1] - self.altura // 2))
    def to_dict(self):
        return {
            "tipo": self.tipo,
            "posicao": self.posicao,
            "cor": self.cor,
        }

    @staticmethod
    def from_dict(data):
        return Chao(data["tipo"], tuple(data["posicao"]), data["cor"])
