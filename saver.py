#!/usr/bin/env python3

import json
from character import Personagem
from structure import Estrutura
from objects import ObjetoInterativo
from ground import Chao

class Saver:
    @staticmethod
    def salvar_mapa(path, level):
        data = {
                "level": {
                        "characters": [char.to_dict() for char in level["characters"]],
                        "structures": [structure.to_dict() for structure in level["structures"]],
                        "objects": [objectEntity.to_dict() for objectEntity in level["objects"]],
                        "ground": [tile.to_dict() for tile in level["ground"].values()],
                        "enemies": [enemy.to_dict() for enemy in level["enemies"]]
                    } 
                }
        with open(path, 'w') as arquivo:
            json.dump(data, arquivo, indent=4)
        print(f"Mapa salvo em {path}.")

    @staticmethod
    def carregar_mapa(path):
        with open(path, 'r') as arquivo:
            data = json.load(arquivo)

        andares = {
                "characters": [Personagem.from_dict(char) for char in data["level"]["characters"]],
                "structures": [Estrutura.from_dict(e) for e in data["level"]["structures"]],
                "objects": [ObjetoInterativo.from_dict(o) for o in data["level"]["objects"]],
                "ground": {tuple(c["posicao"]): Chao.from_dict(c) for c in data["level"]["ground"]},
                "enemies": [Personagem.from_dict(char) for char in data["level"]["enemies"]]
        }

        print(f"Mapa carregado de {path}.")
        return andares
