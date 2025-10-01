from Characters.Character import Character


class CharacterGroup:
    def __init__(self):
        self.characters = {}

    def add_character(self, *characters: Character):
        for character in characters:
            self.characters[character.name] = character

    def get_character(self, name: str) -> Character:
        return self.characters.get(name)


