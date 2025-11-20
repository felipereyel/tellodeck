import pygame
import argparse
from joystick_map import get_button_name, BUTTON_MAPS, AXIS_MAPS, get_axis_name


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Test Pygame joystick inputs.")
    parser.add_argument(
        "--layout",
        type=str,
        default="default",
        help="Specify the layout map to use (e.g., '8BitDo', 'default').",
    )
    return parser.parse_args()


def run_joystick_test(layout: str):
    button_map = BUTTON_MAPS[layout]
    axis_map = AXIS_MAPS[layout]

    pygame.init()
    pygame.joystick.init()

    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No joysticks found.")
        return

    print(f"Found {joystick_count} joystick(s).")
    joysticks = []
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        print(f"Joystick {i}: {joystick.get_name()}")
        print(f"  Number of axes: {joystick.get_numaxes()}")
        print(f"  Number of buttons: {joystick.get_numbuttons()}")
        print(f"  Number of hats: {joystick.get_numhats()}")

    print("\nListening for joystick events... Press Ctrl+C to exit.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                axis_name = get_axis_name(event.axis, axis_map)
                print(
                    f"Joystick {event.joy} Axis {axis_name} moved to {event.value:.2f}"
                )
            elif event.type == pygame.JOYBUTTONDOWN:
                button_name = get_button_name(event.button, button_map)
                print(f"Joystick {event.joy} Button {button_name} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                button_name = get_button_name(event.button, button_map)
                print(f"Joystick {event.joy} Button {button_name} released")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Joystick {event.joy} Hat {event.hat} moved to {event.value}")

        pygame.time.wait(10)  # Small delay to prevent 100% CPU usage

    pygame.quit()


def main():
    """Main function to parse arguments and run the joystick test."""
    args = parse_args()
    run_joystick_test(args.layout)


if __name__ == "__main__":
    main()
