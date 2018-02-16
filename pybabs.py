#!/usr/bin/python3

from random import randint

class UnitTooBigException(Exception):
    pass


class UnitTooSmallException(Exception):
    pass


class WrongUnitQuality(Exception):
    pass


class Platoon:

    class Infantry_Unit:

        def __init__(self, name, platoon, quality):
            self.destroyed = False
            self.officer = True
            self.pins = 0
            self.name = name
            self.platoon = platoon
            if quality in ['Inexperienced', 'Regular', 'Veteran']:
                self.quality = quality
            else:
                raise WrongUnitQuality
            self.order = None

        def str_size(self):
            return '{:>2}/{:>2}'.format(self.size, self.initial_size)

        def fire(self, unit):
            self.order = 'fire'
            dificulty = 3 + self.pins
            hits = 0
            for i in range(self.size):
                if dificulty <= 6 and randint(1, 7) >= dificulty:
                    hits += 1
                elif randint(1, 7) == 6 and randint(1, 7) == 6:
                    hits += 1
            if hits > 0:
                kills = unit.wound(hits)
                print(str(hits) + ' hits -> ' + str(kills) + ' kills')
            else:
                print('0 hits')

        def wound(self, hits):
            self.pins += 1
            kills = 0
            for i in range(hits):
                roll = randint(1, 7)
                if (self.quality == 'Inexperienced' and roll >= 3) or (self.quality == 'Regular' and roll >= 4) or (self.quality == 'Veteran' and roll >= 5):
                    self.size -= 1
                    kills += 1
                    if self.size == 0:
                        self.destroyed = True
                        return kills
            return kills

    class Infantry_Squad(Infantry_Unit):

        def __init__(self, name, platoon, quality, miniatur_cost, size, min_size, max_size):
            super(Platoon.Infantry_Squad, self).__init__(name, platoon, quality)
            if min_size <= size <= max_size:
                self.size = size
            elif size < min_size:
                raise(UnitTooSmallException)
            else:
                raise(UnitTooBigException)
            self.initial_size = self.size
            self.cost = size * miniatur_cost

    class HQ(Infantry_Unit):

        def __init__(self,  name, platoon, quality, officer_cost, soldiers, soldier_cost):
            super(Platoon.HQ, self).__init__(name, platoon, quality)
            if soldiers < 0:
                raise(UnitTooSmallException)
            elif soldiers > 2:
                raise(UnitTooBigException)
            self.size = 1 + soldiers
            self.initial_size = self.size
            self.cost = officer_cost + soldiers * soldier_cost

    def __init__(self, name):
        self.name = name
        self.infantry_squads = {}
        self.hq = {}
        self.victory_points = 0

    def __str__(self):
        format_string = '\n{:<20} | {:<13} | {:<5} | {:>4} | {:<7} | {:<10} | {:<9} | {:>6}'
        out = '= ' + self.name + ' ='
        out += format_string.format('name', 'quality', 'size', 'pins', 'officer', 'last order', 'destroyed', 'points')
        if len(self.hq):
            for name, unit in self.hq.items():
                out += format_string.format(name, unit.quality, unit.str_size(), unit.pins, str(unit.officer),
                                            str(unit.order), str(unit.destroyed), unit.cost)
        if len(self.infantry_squads):
            for name, unit in self.infantry_squads.items():
                out += format_string.format(name, unit.quality, unit.str_size(), unit.pins, str(unit.officer),
                                            str(unit.order), str(unit.destroyed), unit.cost)
        out += '\nPoints: ' + str(self.points())
        return out

    def points(self):
        points = 0
        for hq in self.hq.values():
            points += hq.cost
        for squad in self.infantry_squads.values():
            points += squad.cost
        return points

    def add_hq(self, name, quality, officer_cost, soldiers, soldier_cost):
        self.hq[name] = self.HQ(name, self.name, quality, officer_cost, soldiers, soldier_cost)

    def add_infantry_squad(self, name, quality, miniature_cost, size, min_size, max_size):
        self.infantry_squads[name] = self.Infantry_Squad(name, self.name, quality, miniature_cost, size, min_size,
                                                         max_size)


platoon1 = Platoon('Platoon 1')
platoon1.add_hq('First Lieutenant', 'Veteran', 90, 2, 13)
platoon1.add_infantry_squad('1st Squad', 'Veteran', 13, 10, 5, 10)
platoon1.add_infantry_squad('2nd Squad', 'Veteran', 13, 10, 5, 10)
platoon2 = Platoon('Platoon 2')
platoon2.add_hq('First Lieutenant', 'Veteran', 90, 2, 13)
platoon2.add_infantry_squad('1st Squad', 'Veteran', 13, 10, 5, 10)
platoon2.add_infantry_squad('2nd Squad', 'Veteran', 13, 10, 5, 10)

print(platoon1)
print('')
print(platoon2)
print('')

while not platoon2.infantry_squads['1st Squad'].destroyed:
    platoon1.infantry_squads['1st Squad'].fire(platoon2.infantry_squads['1st Squad'])

print('')
# print('\n==========\n')
print(platoon1)
print('')
print(platoon2)
