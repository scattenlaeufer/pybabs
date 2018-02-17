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
            if quality == 'Inexperienced':
                self.wound_base = 3
                self.moral_base = 8
            elif quality == 'Regular':
                self.wound_base = 4
                self.moral_base = 9
            elif quality == 'Veteran':
                self.wound_base = 5
                self.moral_base = 10
            else:
                raise WrongUnitQuality
            self.quality = quality
            self.order = None

        def str_size(self):
            return '{:>2}/{:>2}'.format(self.size, self.initial_size)

        def fire(self, unit, verbose=False):
            self.order = 'fire'
            difficulty = 3 + self.pins
            if unit.size <= 2:
                difficulty += 1
            hits = 0
            for i in range(self.size):
                if difficulty <= 6 and randint(1, 6) >= difficulty:
                    hits += 1
                elif randint(1, 6) == 6 and randint(1, 6) == 6:
                    hits += 1
            if hits > 0:
                kills, exceptional_damage, moral_check = unit.wound(hits)
            if verbose:
                out = self.platoon + ' ' + self.name + ' shoots at ' + unit.platoon + ' ' + unit.name + ': '
                if hits > 0:
                    out += str(hits) + ' hits -> ' + str(kills) + ' kills'
                    if exceptional_damage > 0:
                        out += ' & ' + str(exceptional_damage) + ' exceptional damage scored'
                    if moral_check == 1:
                        out += ', moral check succeeded'
                    elif moral_check == -1:
                        out += ', moral check failed'
                    if unit.destroyed:
                        out += ', unit destroyed!'
                else:
                    out += '0 hits'
                print(out)

        def order_test(self):
            difficulty = self.moral_base - self.pins
            if not self.officer:
                difficulty -= 1
            roll = randint(1, 6) + randint(1, 6)
            if roll == 2:
                self.pins = self.pins - (1 + randint(1, 6))
                if self.pins < 0:
                    self.pins = 0
                return True
            elif roll <= difficulty:
                return True
            else:
                return False

        def wound(self, hits):
            self.pins += 1
            start_size = self.size
            kills = 0
            exceptional_damage = 0
            moral_check = 0
            for i in range(hits):
                roll = randint(1, 6)
                if roll >= self.wound_base:
                    if (roll == 6 and randint(1, 6) == 6):
                        exceptional_damage += 1
                        self.officer = False
                    if self.size == 1:
                        self.officer = False
                    self.size -= 1
                    kills += 1
                    if self.size == 0:
                        self.destroyed = True
                        return kills, exceptional_demage, moral_check
            if self.size <= start_size/2:
                if self.order_test():
                    moral_check = 1
                else:
                    moral_check = -1
                    self.destroyed = True
                    self.size = 0
                    self.officer = False
            return kills, exceptional_damage, moral_check

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
    platoon1.infantry_squads['1st Squad'].fire(platoon2.infantry_squads['1st Squad'], True)

print('')
# print('\n==========\n')
print(platoon1)
print('')
print(platoon2)
