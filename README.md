# Pong Game with Bullet and AI Opponent

This is a classic Pong game built with Python and Pygame, enhanced with a twist: the right paddle (controlled by the user) can shoot bullets at the computer-controlled left paddle. When hit by a bullet, the computer paddle becomes temporarily invisible (and non-collidable) for 3 seconds.

## Features

- **Classic Pong Gameplay:** Enjoy the timeless fun of Pong with a bouncing ball and two paddles.
- **AI-Controlled Paddle:** The left paddle is controlled by a simple AI that tracks the ball's vertical movement.
- **Bullet Mechanic:** Press the Space key to shoot a bullet from the right paddle. The bullet moves leftward.
- **Temporary Invisibility:** If the bullet collides with the computer paddle, it becomes invisible and non-collidable for 3 seconds.
- **Reset and Bounce Logic:** The ball resets to the center when it goes off-screen, and it bounces off the paddles and screen edges.

## Getting Started

### Prerequisites

- Python 3.x
- Pygame library

You can install Pygame via pip if you haven't already:

```bash
pip install pygame
