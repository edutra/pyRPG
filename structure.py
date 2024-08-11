#!/usr/bin/env python3

import pygame
import json

TAMANHO_CELULA = 40

class Estrutura:
    def __init__(self, nome, posicao, cor):
        self.nome = nome
        self.posicao = posicao
        self.cor = cor
        self.largura = TAMANHO_CELULA
        self.altura = TAMANHO_CELULA

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, pygame.Rect(self.posicao[0] - self.largura // 2, self.posicao[1] - self.altura // 2, self.largura, self.altura))

    def to_dict(self):
        return {
            "nome": self.nome,
            "posicao": self.posicao,
            "cor": self.cor,
        }

    @staticmethod
    def from_dict(data):
        return Estrutura(data["nome"], tuple(data["posicao"]), data["cor"])
