#!/usr/bin/python3

class UnitTooBigException(Exception):
    pass


class UnitTooSmallException(Exception):
    pass


class Platoon:

    class Infantry_Unit:

        def __init__(self, quality):
            self.destroyed = False
            self.officer = True
            self.pins = 0
            self.quality = quality


    class Infantry_Squad(Infantry_Unit):

        def __init__(self, quality, miniatur_cost, size, min_size, max_size):
            super(Platoon.Infantry_Squad, self).__init__(quality)
            if min_size <= size <= max_size:
                self.size = size
            elif size < min_size:
                raise(UnitTooSmallException)
            else:
                raise(UnitTooBigException)
            self.initial_size = self.size
            self.cost = size * miniatur_cost


    class HQ(Infantry_Unit):

        def __init__(self, quality, officer_cost, soldiers, soldier_cost):
            super(Platoon.HQ, self).__init__(quality)
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
        out = '= ' + self.name + ' ='
        if len(self.hq):
            out += '\nHQ: ' + str(self.hq.keys())
        if len(self.infantry_squads):
            out += '\nSquads: ' + str(self.infantry_squads.keys())
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
        self.hq[name] = self.HQ(quality, officer_cost, soldiers, soldier_cost)


    def add_infantry_squad(self, name, quality, miniature_cost, size, min_size, max_size):
        self.infantry_squads[name] = self.Infantry_Squad(quality, miniature_cost, size, min_size, max_size)


platoon = Platoon('Platoon 1')
platoon.add_hq('First Lieutenant', 'Veteran', 90, 2, 13)
platoon.add_infantry_squad('1st Squad', 'Veteran', 13, 10, 5, 10)
platoon.add_infantry_squad('2nd Squad', 'Veteran', 13, 10, 5, 10)
print(platoon)
