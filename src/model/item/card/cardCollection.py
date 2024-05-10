from model.item.card.card import Card, CardColor, CardRarity, CardType, CardKeyword, CardTarget

def loadAllCards():
    return {
        card.id: card for card in [
            StrikeCard(),
            DefendCard()
        ]
    }
    

class StrikeCard(Card):
    def __init__(self):
        super().__init__()
        self.id = "strike"
        self.name = "Strike"
        self.description = "Deal %d damage."
        self.energy_cost = 1
        self.rarity = CardRarity.BASIC
        self.card_type = CardType.ATTACK
        self.keywords = []
        self.color = CardColor.ALL
        self.target = CardTarget.SINGLE
        self.attributes = {
            "damage": 6
        }
    
    def onDraw(self, game):
        return self
    def onPlay(self, game, target):
        return target.takeDamage(self.attributes["damage"])
    def onDiscard(self, game):
        return self
    def onExhaust(self, game):
        return self
    
class DefendCard(Card):
    def __init__(self):
        super().__init__()
        self.id = "defend"
        self.name = "Defend"
        self.description = "Gain %d block."
        self.energy_cost = 1
        self.rarity = CardRarity.BASIC
        self.card_type = CardType.SKILL
        self.keywords = []
        self.color = CardColor.ALL
        self.target = CardTarget.SINGLE
        self.attributes = {
            "block": 5
        }
    
    def onDraw(self, game):
        return self
    def onPlay(self, game, target):
        return game.player.gainBlock(self.attributes["block"])
    def onDiscard(self, game):
        return self
    def onExhaust(self, game):
        return self