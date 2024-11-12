from random import randint, choice


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.stunned = False

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        if self.stunned:
            print(f'{self.name} is stunned and misses a turn!')
            self.stunned = False
            return

        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.__defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    @property
    def defence(self):
        return self.__defence

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes):
        crit = self.damage * randint(2, 5)
        boss.health -= crit
        print(f'Warrior {self.name} hit critically {crit} to boss.')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')

    def apply_super_power(self, boss, heroes):
        boost = randint(1,15)
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.damage += boost
                print(f'Wizard {self.name} boosted the damage by {boost} to {hero.name}')
class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_DAMAGE_AND_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} to boss.')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points

class Witcher(Hero):
    def __init__(self, name,health, damage=0):
        super().__init__(name, health, damage, 'SACRIFICE')
        self.__has_sacrificed = False

    def apply_super_power(self, boss, heroes):
        if self.__has_sacrificed:
            return

        for hero in heroes:
            if hero.health <= 0:
                print(f'Witcher {self.name} sacrificed himself to revive {hero.name}')
                hero.health = self.health
                self.health = 0
                self.__has_sacrificed = True
                break

class Hacker(Hero):
    def __init__(self,name, health,damage):
        super().__init__(name, health, damage, 'TREATMENT_FROM_THE_BOSS_TO_THE_HERO')
        self.__round_counter = 0

    def apply_super_power(self, boss, heroes):
        self.__round_counter += 1

        if self.__round_counter % 2 == 0:
            stolen_health = randint(50, 150)
            boss.health -= stolen_health
            if boss.health < 0:
                boss.health = 0

            heroes_ = [hero for hero in heroes if hero.health >0 and hero != self]
            if heroes_:
                chosen_hero = choice(heroes_)
                chosen_hero.health += stolen_health
                print(f'Hacker {self.name} stole {stolen_health} HP from the boss and heal {chosen_hero.name} ')

class Thor(Hero):
    def __init__(self,name,health,damage):
        super().__init__(name,health,damage, 'STUN')
        self.__stun_chance = 0.3

    def apply_super_power(self, boss, heroes):
        if randint (1,100) <= self.__stun_chance * 100:
            boss.stunned = True
            print(f'{self.name} stunned the boss for 1 turn!')
        else:
            print(f'{self.name} missed the stun')

class Saitama(Hero):
    def __init__(self,name,health,damage):
        super().__init__(name,health,damage, 'ONE_PUNCH')

    def apply_super_power(self, boss, heroes):
        boss.health = 0
        print(f'{self.name} destroys the {boss.name} with ONE PUNCH! ')

class King(Hero):
    def __init__(self, name, health, damage=0):
        super().__init__(name,health,damage,'SAITAMA')
        self.__saitama_chance = 0.1

    def apply_super_power(self, boss, heroes):
        if randint(1,100) <= self.__saitama_chance * 100:
            saitama = Saitama(name='Saitama', health=1000, damage=10000)
            print(f'King {self.name} summoned Saitama!')
            saitama.apply_super_power(boss,heroes)
        else:
            print(f'King {self.name} failed to summon Saitama')



round_number = 0


def show_statistics(boss, heroes):
    print(f'ROUND - {round_number} ------------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    boss = Boss(name='Dragon', health=3000, damage=50)
    warrior_1 = Warrior(name='Mario', health=100, damage=10)
    warrior_2 = Warrior(name='Ben', health=280, damage=15)
    magic = Magic(name='Merlin', health=290, damage=10)
    berserk = Berserk(name='Guts', health=260, damage=5)
    doc = Medic(name='Aibolit', health=250, damage=5, heal_points=15)
    assistant = Medic(name='Kristin', health=300, damage=5, heal_points=5)
    witcher = Witcher(name='Dura4ok', health=200)
    hacker = Hacker(name='Snowden', health=1000, damage=0)
    thor = Thor(name='Thor', health=250, damage=50)
    king = King(name='Arthur', health=300)
    heroes_list = [warrior_1, magic,doc,king ,warrior_2, hacker, thor, witcher, berserk, assistant]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
