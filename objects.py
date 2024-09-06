#!/usr/bin/env python3

import json
import pygame

TAMANHO_CELULA = 40

class ObjetoInterativo:
    def __init__(self, nome, posicao, cor):
        self.nome = nome
        self.posicao = posicao
        self.cor = cor
        self.largura = TAMANHO_CELULA - 10
        self.altura = TAMANHO_CELULA - 10

    def desenhar(self, tela):
        image = pygame.transform.scale(pygame.image.load('assets/chest_1.png').convert_alpha(), (self.largura, self.altura))
        tela.blit(image, (self.posicao[0] - self.largura // 2, self.posicao[1] - self.altura // 2))

    def to_dict(self):
        return {
            "nome": self.nome,
            "posicao": self.posicao,
            "cor": self.cor,
        }

    @staticmethod
    def from_dict(data):
        return ObjetoInterativo(data["nome"], tuple(data["posicao"]), data["cor"])
