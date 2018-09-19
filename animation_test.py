import time
import sys
import curses

animation = "|/-\\"
def animation_loop():
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

def main(sc):
    sc.nodelay(1)

    for angry in range(20):
        sc.addstr(angry, 1, "hi")
        sc.refresh()

        if sc.getch() == ord('q'):
            break

        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
