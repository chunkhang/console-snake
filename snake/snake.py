#!/usr/bin/env python3

import curses
import time
import enum
import random
from contextlib import contextmanager

class Direction(enum.Enum):
   up = 0
   down = 1
   left = 2
   right = 3

def main():
   with wrapper() as screen:
      # Set up screen
      screen_height, screen_width = screen.getmaxyx()
      score = 0
      score_window = curses.newwin(1, screen_width, 0, 0)
      score_window.addstr(' Score:', curses.A_BOLD)
      write_score(score_window, 0, 8, score)
      game_window = curses.newwin(screen_height-2, screen_width, 1, 0)
      game_window.border()
      write_message(game_window, screen_height, screen_width, 
         'Press any arrow key to start')
      info_window = curses.newwin(1, screen_width, screen_height-1, 0)
      info_window.addstr(' Controls: ', curses.A_BOLD)
      info_window.addstr('↑ ↓ ← →')
      info_window.addstr(0, screen_width-26, 'Pause/Resume:', curses.A_BOLD)
      info_window.addstr(0, screen_width-12, 'p')
      info_window.addstr(0, screen_width-8, 'Quit:', curses.A_BOLD)
      info_window.addstr(0, screen_width-2, 'q')
      screen.refresh()
      score_window.refresh()
      game_window.refresh()
      info_window.refresh()

      # Snake
      game_height, game_width = game_window.getmaxyx()
      snake = []
      snake.append({
         'y': int(game_height/2),
         'x': int(game_width/2)
      })
      direction = None

      # Food
      food = generate_food(game_height, game_width)

      # Main loop
      game_over = False
      exit = False
      while True:
         # Get latest key
         key = screen.getch()
         curses.flushinp()

         # Key: q
         if key == ord('q'):
            # Exit
            exit = True
         elif key == ord('p') and direction != None:
            # Pause
            screen.nodelay(False)
            write_message(game_window, screen_height, screen_width, 
               'Game paused')
            game_window.refresh()
            while True:
               key = screen.getch()
               if key == ord('p'):
                  # Unpause
                  break
               elif key == ord('q'):
                  # Exit
                  exit = True
                  break
               time.sleep(0.1)
            screen.nodelay(True)
         # Key: ↑
         elif key == curses.KEY_UP and direction != Direction.down:
            direction = Direction.up
         # Key: ↓
         elif key == curses.KEY_DOWN and direction != Direction.up:
            direction = Direction.down
         # Key: ←
         elif key == curses.KEY_LEFT and direction != Direction.right:
            direction = Direction.left
         # Key: →
         elif key == curses.KEY_RIGHT and direction != Direction.left:
            direction = Direction.right
         if exit:
            break

         # Move snake
         new_head_y = snake[0]['y']
         new_head_x = snake[0]['x']
         if direction == Direction.up:
            new_head_y -= 1
         elif direction == Direction.down:
            new_head_y += 1
         elif direction == Direction.left:
            new_head_x -= 2
         elif direction == Direction.right:
            new_head_x += 2
         snake.insert(0, {
            'y': new_head_y,
            'x': new_head_x
         })
         # Check for food eaten
         if new_head_y == food['y'] and -1 <= new_head_x-food['x'] <= 1:
            curses.beep()
            food = generate_food(game_height, game_width)
            score += 1
         else:
            snake.pop()
         # Check for game over
         if new_head_y <= 0 or new_head_y >= game_height-1 or \
            new_head_x <= 0 or new_head_x >= game_width-1 or \
            collision(new_head_y, new_head_x, snake):
            curses.beep()
            write_message(game_window, screen_height, screen_width, 
               'Game over')
            game_over = True

         # Draw score and game windows
         if direction != None:
            if not game_over:
               game_window.clear()
            game_window.border()
            # Food
            game_window.addstr(food['y'], food['x'], '#')
         # Snake
         if not game_over:
            for block in snake:
               game_window.addstr(block['y'], block['x'], '*')
         # Score
         write_score(score_window, 0, 8, score)
         score_window.refresh()
         game_window.refresh()

         # Game over
         if game_over:
            time.sleep(3)
            exit = True

         # Refresh rate
         time.sleep(0.2)

def write_score(window, y, x, score):
   window.addstr(0, 8, str(score))

def write_message(window, height, width, text): 
   window.addstr(height-5, int((width-len(text)) / 2), text)

def generate_food(max_height, max_width):
   return {
      'y': random.randint(1, max_height-2),
      'x': random.randint(1, max_width-2)
   }

def collision(y, x, blocks):
   first = True
   for block in blocks:
      if first:
         first = False
         continue
      if y == block['y'] and x == block['x']:
         return True
   return False

@contextmanager
def wrapper():
   # Setup curses
   stdscr = curses.initscr()
   curses.noecho() # No echo key input
   curses.cbreak() # Input without enter
   curses.curs_set(0) # Hide cursor
   stdscr.keypad(True) # Allow arrow keys
   stdscr.nodelay(True) # Non-blocking input reading
   # Yield screen
   try:
      yield stdscr
   # Teardown curses
   finally:
      curses.curs_set(1)
      curses.nocbreak()
      curses.echo()
      curses.endwin()

if __name__ == '__main__':
   main()