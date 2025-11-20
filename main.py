from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
import argparse

from joystick_map import AXIS_MAPS, BUTTON_MAPS, get_axis_name, get_button_name

# Speed of the drone
HORIZONTAL_SPEED_MULTIPLIER = 60
VERTICAL_SPEED_MULTIPLIER = 10
YAW_SPEED_MULTIPLIER = 30
JOYSTICK_DEADZONE = 0.5

# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 120


class FrontEnd(object):
    """Maintains the Tello display and moves it through the joystick controls.
    Press escape key to quit.
    The controls are:
        - START: Takeoff
        - SELECT: Land
        - Right Axis: Horizontal movement
        - Left Axis: Vertical + rotation
    """

    def __init__(self, layout: str):
        # Init pygame
        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        if pygame.joystick.get_count() == 0:
            raise Exception("No joystick found.")

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.axis_map = AXIS_MAPS[layout]
        self.button_map = BUTTON_MAPS[layout]

        # Create pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def run(self):
        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                elif event.type == pygame.JOYAXISMOTION:
                    self.axis_motion(event)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_down(event)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # battery n. 电池
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(
                frame, text, (5, 720 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def axis_motion(self, event):
        axis_name = get_axis_name(event.axis, self.axis_map)
        axis_value = event.value

        if abs(axis_value) < JOYSTICK_DEADZONE:
            axis_value = 0

        axis_value = int(axis_value * 100)

        if axis_name == "LX":  # Left Stick X
            self.yaw_velocity = int(axis_value * YAW_SPEED_MULTIPLIER)
        elif axis_name == "LY":  # Left Stick Y
            self.up_down_velocity = int(-axis_value * VERTICAL_SPEED_MULTIPLIER)
        elif axis_name == "RX":  # Right Stick X
            self.left_right_velocity = int(axis_value * HORIZONTAL_SPEED_MULTIPLIER)
        elif axis_name == "RY":  # Right Stick Y
            self.for_back_velocity = int(-axis_value * HORIZONTAL_SPEED_MULTIPLIER)

    def button_down(self, event):
        button_name = get_button_name(event.button, self.button_map)

        if button_name == "START":
            self.tello.takeoff()
            self.send_rc_control = True
        elif button_name == "SELECT":
            self.tello.land()
            self.send_rc_control = False
        elif button_name == "UP":
            self.tello.flip_forward()
        elif button_name == "DOWN":
            self.tello.flip_back()
        elif button_name == "LEFT":
            self.tello.flip_left()
        elif button_name == "RIGHT":
            self.tello.flip_right()

    def update(self):
        """Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(
                self.left_right_velocity,
                self.for_back_velocity,
                self.up_down_velocity,
                self.yaw_velocity,
            )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Test Pygame joystick inputs.")
    parser.add_argument(
        "--layout",
        type=str,
        default="8bitdo",
        help="Specify the layout map to use (e.g., '8BitDo', 'default').",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    frontend = FrontEnd(args.layout)

    # run frontend
    frontend.run()


if __name__ == "__main__":
    main()
