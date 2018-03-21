"""
WumpusWorldParser.py takes a graphical world, and converts it to an encoding for the wumpus simulator.
"""

import os
import sys
import argparse


# Orientations: Defines orientations within the world
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3


class Knowledge(object):
    def __init__(self):
        self.world_size = 0
        self.wumpus_rotations = []
        self.tiles = []

    def initate_tiles(self):
        for i in range(self.world_size):
            row = []
            for j in range(self.world_size):
                row.append(Tile(i + 1, j + 1))
            self.tiles.append(row)

    def validate(self):
        validated = True
        if self.world_size is None or self.world_size < 2:
            print("Validation Error: world size is less than 2")
            validated = False

        wumpus_count = 0
        gold_count = 0
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.tiles[row][col].wumpus is not None:
                    wumpus_count += 1
                if self.tiles[row][col].gold is not None:
                    gold_count += 1

        if len(self.wumpus_rotations) != wumpus_count:
            print("Validation Error: number of wumpus_rotations does not match wumpus count")
            validated = False

        if wumpus_count != gold_count:
            print("Validation Error: number of wumpus locations does not match gold locations")
            validated = False

        return validated

    def write(self, output):
        if not self.validate():
            print("\nValidation failed, not writing output to file.")
            sys.exit(1)

        with open(file=output, mode="w") as outfile:
            outfile.write("size {}\n".format(self.world_size))

            self._write_wumpus_count(outfile=outfile)
            self._write_wumpus(outfile=outfile)
            self._write_wumpus_rotations(outfile=outfile)
            self._write_gold(outfile=outfile)
            self._write_pit(outfile=outfile)
            self._write_walls(outfile=outfile)

    def _write_wumpus_count(self, outfile):
        count = 0
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.tiles[row][col].wumpus is not None:
                    count += 1
        outfile.write("wumpus_count {}\n".format(count))

    def _write_wumpus_rotations(self, outfile):
        for idx in range(len(self.wumpus_rotations)):
            outfile.write("wumpus_rotation {} {}\n".format(idx + 1, self.wumpus_rotations[idx]))

    def _write_wumpus(self, outfile):
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.tiles[row][col].wumpus is not None:
                    outfile.write("wumpus {} {} {}\n".format(self.tiles[row][col].wumpus, row + 1, col + 1))

    def _write_gold(self, outfile):
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.tiles[row][col].gold is not None:
                    outfile.write("gold {} {} {}\n".format(self.tiles[row][col].gold, row + 1, col + 1))

    def _write_pit(self, outfile):
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.tiles[row][col].pit:
                    outfile.write("pit {} {}\n".format(row + 1, col + 1))

    def _write_walls(self, outfile):
        for row in range(self.world_size):
            for col in range(self.world_size):
                if self.tiles[row][col].wall_top:
                    outfile.write("wall {} {} {}\n".format(UP, row + 1, col + 1))
                if self.tiles[row][col].wall_right:
                    outfile.write("wall {} {} {}\n".format(RIGHT, row + 1, col + 1))
                if self.tiles[row][col].wall_bottom:
                    outfile.write("wall {} {} {}\n".format(DOWN, row + 1, col + 1))
                if self.tiles[row][col].wall_left:
                    outfile.write("wall {} {} {}\n".format(LEFT, row + 1, col + 1))


class Tile(object):
    def __init__(self, x, y):
        self.location_x = x
        self.location_y = y
        self.wumpus = None
        self.gold = None
        self.agent = False
        self.pit = False

        self.wall_top = False
        self.wall_right = False
        self.wall_bottom = False
        self.wall_left = False


def read_lines(filename):
    with open(file=filename, mode="r") as infile:
        lines = infile.readlines()

    if len(lines) < 3:
        print("Error: Invalid world file; lines < 3.")
        sys.exit(1)
    return lines


def process_header(knowledge, lines):
    count = 1  # count is incremented for every line found
    size_line = lines[0].strip()

    tokens = size_line.split(" ")
    if len(tokens) == 2 and tokens[0] == "size":
        try:
            knowledge.world_size = int(tokens[1])
        except ValueError:
            print("Header ValueError: expected size 'integer', found '{}'".format(tokens[1]))
            sys.exit(1)
    else:
        print("Header Error: expected 'size', found '{}'".format(tokens[0]))
        sys.exit(1)

    while lines[count].strip() != "":
        if "+" in lines[count].strip():
            print("Header Error: expected 'wumpus_rotation', found '{}'".format(tokens[0]))
            sys.exit(1)

        tokens = lines[count].split(' ')

        if len(tokens) == 3 and tokens[0] == "wumpus_rotation":
            if int(tokens[1]) != count:
                print("Header Error: wumpus_rotation index does not follow pattern, should increment by 1,")
                print(" (starting with 1).  There must be an index for each wumpus and they must be listed in order.")
                sys.exit(1)

            if tokens[2].strip() == "static":
                knowledge.wumpus_rotations.append(0)
            elif tokens[2].strip() == "clockwise":
                knowledge.wumpus_rotations.append(1)
            elif tokens[2].strip() == "counter-clockwise":
                knowledge.wumpus_rotations.append(2)
            else:
                print("Header TypeError: expected rotation type, found '{}'".format(tokens[2]))
                print("  Allowed header types: static, clockwise, or counter-clockwise")
                sys.exit(1)
        else:
            print("Header Error: expected 'wumpus_rotation', found '{}'".format(tokens[0]))
            sys.exit(1)

        count += 1

    return lines[count + 1:]


def process_world(knowledge, lines):
    knowledge.initate_tiles()  # Generate the initial world tiles

    if len(lines) != (knowledge.world_size * 3 + 1):
        print("Processing Error: the world file not seem to have the correct size (rows) as specified in the header.")
        sys.exit(1)

    for row in range(knowledge.world_size):
        top_wall = lines[row * 3]
        top_inner = lines[row * 3 + 1]
        bottom_inner = lines[row * 3 + 2]
        bottom_wall = lines[row * 3 + 3]

        row_idx = knowledge.world_size - row - 1

        for col in range(knowledge.world_size):
            col_top_wall = top_wall[(col * 6):(col * 6 + 7)]
            col_top_inner = top_inner[(col * 6):(col * 6 + 7)]
            col_bottom_inner = bottom_inner[(col * 6):(col * 6 + 7)]
            col_bottom_wall = bottom_wall[(col * 6):(col * 6 + 7)]

            tile = knowledge.tiles[col][row_idx]  # there is a current bug in positioning the tiles, these need reversal

            print("Processing wumpus tile=({}, {})".format(col + 1, row_idx + 1))

            if check_top_wall(line=col_top_wall):
                tile.wall_top = True

            if check_right_wall(top=col_top_inner, bottom=col_bottom_inner):
                tile.wall_right = True

            if check_bottom_wall(line=col_bottom_wall):
                tile.wall_bottom = True

            if check_left_wall(top=col_top_inner, bottom=col_bottom_inner):
                tile.wall_left = True

            if check_pit(line=col_top_inner):
                tile.pit = True

            tile.gold = check_gold(top=col_top_inner, bottom=col_bottom_inner)
            tile.wumpus = check_wumpus(top=col_top_inner, bottom=col_bottom_inner)


def check_top_wall(line):
    if len(line) == 7:
        if line[1:6] == "-----":
            return True
        elif line[1:6] == "     ":
            return False
        else:
            print("Processing Error: Unrecognized symbol(s), expecting top wall, found '{}'.".format(line[1:7]))
            sys.exit(1)
    else:
        print("Processing Error: Top wall substring length != 7")
        sys.exit(1)


def check_bottom_wall(line):
    if len(line) == 7:
        if line[1:6] == "-----":
            return True
        elif line[1:6] == "     ":
            return False
        else:
            print("Processing Error: Unrecognized symbol(s), expecting bottom wall.")
            sys.exit(1)
    else:
        print("Processing Error: Bottom wall substring length != 7.")
        sys.exit(1)


def check_left_wall(top, bottom):
    if len(top) == 7 and len(bottom) == 7:
        if top[0] == '|' and bottom[0] == '|':
            return True
        elif top[0] == '|' or bottom[0] == '|':
            print("Processing Error: top or bottom do not have match left walls.")
            sys.exit(1)
        else:
            return False
    else:
        print("Processing Error: Inner contents substring length != 7.")


def check_right_wall(top, bottom):
    if len(top) == 7 and len(bottom) == 7:
        if top[6] == '|' and bottom[6] == '|':
            return True
        elif top[6] == '|' or bottom[6] == '|':
            print("Processing Error: top or bottom do not have matching right walls.")
            sys.exit(1)
        else:
            return False
    else:
        print("Processing Error: Inner contents substring length != 7.")


def check_gold(top, bottom):
    if len(top) == 7 and len(bottom) == 7:
        if top[3] == 'G':
            if bottom[1:6] == "     ":
                return None
            try:
                return int(bottom[1:6].strip())
            except ValueError:
                print("Processing ValueError: expected integer or empty for 'G' tile, found '{}'".format(bottom[1:6]))
                sys.exit(1)
        elif top[3] == ' ':
            return None
        else:
            print("Processing Error: expected 'G' or empty, found '{}'".format(top[1]))
            sys.exit(1)
    else:
        print("Processing Error: Line substring length != 7")
        sys.exit(1)


def check_pit(line):
    if len(line) == 7:
        if line[5] == 'P':
            return True
        elif line[5] == ' ':
            return False
        else:
            print("Processing Error: expected 'P' or empty, found '{}'".format(line[5]))
            sys.exit(1)
    else:
        print("Processing Error: Line substring length != 7")
        sys.exit(1)


def check_wumpus(top, bottom):
    if len(top) == 7 and len(bottom) == 7:
        if top[1] == 'W':
            if bottom[1:6] == "     ":
                return None
            try:
                return int(bottom[1:6].strip())
            except ValueError:
                print("Processing ValueError: expected integer or empty for 'W' tile, found '{}'".format(bottom[1:6]))
                sys.exit(1)
        elif top[1] == ' ':
            return None
        else:
            print("Processing Error: expected 'W' or empty, found '{}'".format(top[1]))
            sys.exit(1)
    else:
        print("Processing Error: Line substring length != 7")
        sys.exit(1)


def main(args):
    knowledge = Knowledge()
    lines = read_lines(args.file)

    remaining_lines = process_header(knowledge=knowledge, lines=lines)
    process_world(knowledge=knowledge, lines=remaining_lines)

    print()
    print("Processing completed, writing encoding to file '{}'...".format(args.output))
    knowledge.write(args.output)

    print()
    print("Done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parser to convert a graphical ascii art world for Wumpsim encoding")
    parser.add_argument('file', type=str)
    parser.add_argument('output', type=str)
    parser.add_argument('--force', action="store_true")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        raise parser.error("'{}' file does not exist.".format(args.file))

    if os.path.isfile(args.output):
        if args.force:
            print("Warning: deleting existing output file '{}'.".format(args.output))
            os.remove(args.output)
        else:
            raise parser.error("'{}' output file already exists; use '--force' to delete existing.".format(args.output))

    main(args)
