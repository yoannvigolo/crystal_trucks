import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Crystals VS Trucks"


class CrystalsVsTrucksGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.nb_trucks = 0
        self.grid_width = 0
        self.grid_height = 0
        self.grid = []
        self.cell_width = 1
        self.cell_height = 1
        self.commands = []
        self.trucks = []

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def read_config_file(self, filepath):
        in_grid = False
        with open(filepath, encoding="utf-8") as file:
            for line in file:
                if in_grid and not line.startswith("### End Grid ###"):
                    self.grid.append([])
                    for char in line.strip():
                        if char == " ":
                            self.grid[-1].append(0)
                        else:
                            self.grid[-1].append(int(char))
                    for x in range(len(self.grid[-1]), self.width):
                        self.grid[-1].append(0)
                elif line.startswith("### End Grid ###"):
                    in_grid = False
                elif line.startswith("trucks: "):
                    self.nb_trucks = int(line.split()[-1])
                    for truck_id in range(self.nb_trucks):
                        self.trucks.append([0, truck_id])
                elif line.startswith("width: "):
                    self.grid_width = int(line.split()[-1])
                    self.cell_width = SCREEN_WIDTH // self.grid_width
                elif line.startswith("height: "):
                    self.grid_height = int(line.split()[-1])
                    self.cell_height = SCREEN_HEIGHT // self.grid_height
                elif line.startswith("### Grid ###"):
                    in_grid = True
                else:
                    parts = line.split()
                    if len(parts) < 2 or parts[1] not in ("DIG", "MOVE", "WAIT"):
                        print("ignore", line, end="")
                    else:
                        self.commands.append(" ".join(parts))

    def position_to_px(self, x, y):
        return (x + 0.5) * self.cell_width, (y + 0.5) * self.cell_height

    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        # Create your sprites and sprite lists here
        self.truck_list = arcade.SpriteList()
        for truck_x, truck_y in self.trucks:
            truck_sprite = arcade.Sprite("./towtruck.png", 1)
            x, y = self.position_to_px(truck_x, truck_y)
            truck_sprite.center_x = x - truck_sprite.width // 2 + 10
            truck_sprite.center_y = y - truck_sprite.height // 2 - 10
            self.truck_list.append(truck_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x]:
                    arcade.draw_text(
                        str(self.grid[y][x]),
                        x * self.cell_width,
                        y * self.cell_height,
                        arcade.color.BLACK,
                        font_size=20,
                        font_name="Kenney Pixel Square",
                    )

        self.truck_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """Main function"""
    game = CrystalsVsTrucksGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.read_config_file("seed4.sample.txt")  # TODO use argparse
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
