

class Level:
    def __init__(self, level, action_arr):
        self.level = level
        self.action_arr = action_arr
        self.spawn_counter = 0
        self.spawn_index = 0

    def have_all_spawned(self):
        if self.spawn_index >= len(self.action_arr):
            return True
        else:
            return False

    def spawn_enemies(self, game):
        if self.spawn_index >= len(self.action_arr):
            # all enemies have been spawned => do nothing
            return
        if self.spawn_counter <= 0:
            # time to do something
            new_action = self.action_arr[self.spawn_index]
            if isinstance(new_action, int):
                # time to wait
                self.spawn_counter = new_action
            else:
                #time to add enemy to the game
                new_enemy = new_action
                new_enemy.set_game(game)
                game.append_enemy(new_enemy)
            self.spawn_index += 1
        else:
            self.spawn_counter -= 1
