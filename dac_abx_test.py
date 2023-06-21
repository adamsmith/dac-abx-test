import pyhid_usb_relay
import random


def main():
    print("See instructions at https://github.com/adamsmith/dac-abx-test/")
    print()

    print("Shuffling initial state...")
    shuffle_relay_state()

    # "A" is the source being played after the initial shuffle
    # "B" is the other source
    n_preferred_a = 0
    n_preferred_b = 0
    
    current_playing_a = True
    for _ in range(10):
        print()
        print("New round...")

        changed_playing = shuffle_relay_state()
        if changed_playing:
            current_playing_a = not current_playing_a
        x_is_a = current_playing_a
        currently_playing_x = True
        while True:
            command = input(f"""Currently playing {"X" if currently_playing_x else "Y"}, press enter to toggle, X or Y to select preference...""")
            if command == "":
                toggle_relay()
                current_playing_a = not current_playing_a
                currently_playing_x = not currently_playing_x
            elif command.lower() == "x":
                if x_is_a:
                    n_preferred_a += 1
                else:
                    n_preferred_b += 1
                break
            elif command.lower() == "y":
                if x_is_a:
                    n_preferred_b += 1
                else:
                    n_preferred_a += 1
                break
            elif command.lower() == "s":
                # "skip" command
                # useful if we want to end the test early but still see results so far
                break
            else:
                print("Unrecognized input")
    
    # set to A so we can reveal which was which
    if not current_playing_a:
        toggle_relay()

    print()
    print()
    print(
f"""Votes for...
  - A: {n_preferred_a}
  - B: {n_preferred_b}

The output has been set to 'A' so you know which is which!

(Statistical-significance test?)""")

def shuffle_relay_state():
    # returns whether we did changed the currently-playing state
    # shuffles at least 20 times so we can't track `change` by listening
    #   to relay sounds
    change = random.choice([True, False])
    for _ in range(20 + (1 if change else 0)):
        toggle_relay()
    return change

def toggle_relay():
    relay = pyhid_usb_relay.find()
    relay.toggle_state("all")  # both audio channels (stereo)
    return relay.state


if __name__ == "__main__":
    main()