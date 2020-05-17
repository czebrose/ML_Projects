import util
from util import Direction
from location import Location


NORTH_SOUTH_ROAD_EMPTY_IMG = util.load_img("road_northsouth.png")
EAST_WEST_ROAD_EMPTY_IMG = util.load_img("road_eastwest.png")


class Road(Location):
    def get_direction(self, owner):
        if self.unit_in_loc is None:
            return None
        unit_direction = self.unit_in_loc.direction
        start_node_direction = self.get_node_direction(unit_direction, owner)
        end_node_direction = self.get_node_direction(Location.reverse_direction(unit_direction), owner)

        dir_options = []
        if unit_direction is not None:
            dir_options.append(unit_direction)
        if start_node_direction is not None:
            dir_options.append(start_node_direction)
        if end_node_direction is not None:
            dir_options.append(end_node_direction)

        if len(dir_options) <= 0:
            return None
        elif len(dir_options) == 1:
            return dir_options[0]
        elif len(dir_options) == 2:
            if dir_options[0] == unit_direction:
                return dir_options[1]
            return dir_options[0]
        else:
            if dir_options[0] == dir_options[1]:
                return dir_options[0]
            elif dir_options[0] == dir_options[2]:
                return dir_options[0]
            elif dir_options[1] == dir_options[2]:
                return dir_options[1]
            else:
                return start_node_direction

    def get_node_direction(self, direction, owner):
        n = self.get_next_node(direction)
        if n is None:
            return None
        rev_direction = Location.reverse_direction(direction)
        if n.exit_direction[owner] == rev_direction:
            return rev_direction
        else:
            return direction

    def draw(self, win):
        pixel_x = self.x * util.NODE_WIDTH
        pixel_y = self.y * util.NODE_WIDTH
        if self.neighbors[Direction.NORTH] is not None:
            win.blit(NORTH_SOUTH_ROAD_EMPTY_IMG, (pixel_x, pixel_y))
        else:
            win.blit(EAST_WEST_ROAD_EMPTY_IMG, (pixel_x, pixel_y))
        if self.unit_in_loc is not None:
            self.unit_in_loc.draw(win, (pixel_x, pixel_y))
