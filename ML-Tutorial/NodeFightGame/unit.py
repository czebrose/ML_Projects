import util
from util import PlayerColor, UnitType, Direction
from types import DynamicClassAttribute


BLUE_PIKEMAN_UNIT_IMG = util.load_img("unit_pikeman_blue.png")
RED_PIKEMAN_UNIT_IMG = util.load_img("unit_pikeman_red.png")
BLUE_ARCHER_UNIT_IMG = util.load_img("unit_archer_blue.png")
RED_ARCHER_UNIT_IMG = util.load_img("unit_archer_red.png")
BLUE_KNIGHT_UNIT_IMG = util.load_img("unit_knight_blue.png")
RED_KNIGHT_UNIT_IMG = util.load_img("unit_knight_red.png")


class Unit:
    def __init__(self, unit_type, owner, direction):
        self.unit_type = unit_type
        self.owner = owner
        self.next_direction = direction
        self.anim_direction = direction
        self.time_to_loc = 0

    @DynamicClassAttribute
    def name(self):
        return [self.unit_type, self.owner, self.next_direction]

    # Returns true if the given enemy type would kill this unit.
    def get_fight_result(self, enemy_type):
        return get_fight_result(self.unit_type, enemy_type)

    def set_direction(self, direction):
        if self.time_to_loc <= 0:
            if self.next_direction:
                self.anim_direction = self.next_direction
            else:
                self.anim_direction = direction
        self.next_direction = direction

    def get_direction(self):
        return self.next_direction

    def loc_changed(self):
        self.time_to_loc = 10

    def adjust_pos(self, pos):
        if self.time_to_loc <= 0:
            self.time_to_loc = 0
            return pos
        x = 0
        y = 0
        if self.anim_direction == Direction.NORTH:
            y = 1
        elif self.anim_direction == Direction.SOUTH:
            y = -1
        elif self.anim_direction == Direction.EAST:
            x = -1
        elif self.anim_direction == Direction.WEST:
            x = 1
        pos_x, pos_y = pos
        pos_x = pos_x + (x * self.time_to_loc * (util.NODE_SIZE / 10))
        pos_y = pos_y + (y * self.time_to_loc * (util.NODE_SIZE / 10))
        self.time_to_loc = self.time_to_loc - 1
        return pos_x, pos_y

    def draw(self, win, pos):
        adjust_pos = self.adjust_pos(pos)

        if self.unit_type == UnitType.PIKEMAN:
            self.draw_unit(win, adjust_pos, RED_PIKEMAN_UNIT_IMG, BLUE_PIKEMAN_UNIT_IMG)
        if self.unit_type == UnitType.ARCHER:
            self.draw_unit(win, adjust_pos, RED_ARCHER_UNIT_IMG, BLUE_ARCHER_UNIT_IMG)
        if self.unit_type == UnitType.KNIGHT:
            self.draw_unit(win, adjust_pos, RED_KNIGHT_UNIT_IMG, BLUE_KNIGHT_UNIT_IMG)

    def draw_unit(self, win, pos, red_img, blue_img):
        if self.owner == PlayerColor.RED:
            win.blit(red_img, pos)
        if self.owner == PlayerColor.BLUE:
            win.blit(blue_img, pos)


def get_fight_result(defender_type, attacker_type):
    if defender_type is UnitType.PIKEMAN:
        return attacker_type is UnitType.PIKEMAN or attacker_type is UnitType.ARCHER
    elif defender_type is UnitType.ARCHER:
        return attacker_type is UnitType.ARCHER or attacker_type is UnitType.KNIGHT
    elif defender_type is UnitType.KNIGHT:
        return attacker_type is UnitType.KNIGHT or attacker_type is UnitType.PIKEMAN
    else:
        return True


# Returns 1, if the defender counters the attacker
# Returns 0, if they are the same unit type
# Returns -1, if the defender is countered by the attacker
def compare_unit_types(defender_type, attacker_type):
    def_kills_att = get_fight_result(attacker_type, defender_type)
    att_kills_def = get_fight_result(defender_type, attacker_type)
    if def_kills_att and att_kills_def:
        return 0
    elif def_kills_att:
        return 1
    else:
        return -1


def resolve_fight_round(round_fighters):
    fight_results = {}
    for color in round_fighters:
        fight_results[color] = False

    while list(fight_results.values()).count(False) > 1:
        results_iter = iter(fight_results)
        color_a = None
        color_b = None
        while color_a is None or color_b is None:
            c = next(results_iter)
            if not fight_results[c]:
                # if this unit is alive
                if not color_a:
                    color_a = c
                elif not color_b:
                    color_b = c
        unit_a = round_fighters[color_a].unit_in_loc
        unit_b = round_fighters[color_b].unit_in_loc
        fight_results[color_a] = unit_a.get_fight_result(unit_b.unit_type)
        fight_results[color_b] = unit_b.get_fight_result(unit_a.unit_type)

    return fight_results
