#!/usr/bin/env python3

import json
from character import Personagem
from structure import Estrutura
from objects import ObjetoInterativo
from ground import Chao



class Saver:
    @staticmethod
    def salvar_mapa(path, chars, structures, objects, floor, enemies):
        data = {
            "chars": [char.to_dict() for char in chars],
            "structures": [structures.to_dict() for structures in structures],
            "objects": [objectEntity.to_dict() for objectEntity in objects],
            "floor": [tile.to_dict() for tile in floor.values()],
            "enemies": [enemy.to_dict() for enemy in enemies]
        }
        with open(path, 'w') as arquivo:
            json.dump(data, arquivo, indent=4)
        print(f"Mapa salvo em {path}.")

    @staticmethod
    def carregar_mapa(path):
        with open(path, 'r') as arquivo:
            data = json.load(arquivo)
        
        chars = [] if len(data["chars"]) == 0 else [Personagem.from_dict(char) for char in data["chars"]],
        structures = [Estrutura.from_dict(e) for e in data["structures"]]
        objects = [ObjetoInterativo.from_dict(o) for o in data["objects"]]
        floor = {tuple(c["posicao"]): Chao.from_dict(c) for c in data["floor"]}
        enemies =  [] if len(data["enemies"]) == 0 else [Personagem.from_dict(char) for char in data["enemies"]],
        print(f"Mapa carregado de {path}.")

        print(chars)
        print(structures)
        print(objects)
        print(enemies)

        return chars, structures, objects, floor, enemies

