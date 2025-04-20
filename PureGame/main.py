# main.py
import pygame
import sys
import torch
import Game
import settings
from AICore import DQNAgent
# train_dqn contains the main training loop now
import Train

def main():
    pygame.init()
    pygame.font.init()

    print("-------------------------")
    print("  Dino AI Game Options")
    print("-------------------------")
    print("  1. Play the game yourself")
    print("  2. See the AI play the game (Requires trained model)")
    print("  3. Train the AI agent")
    print("-------------------------")

    choice = input("Enter choice (1, 2, or 3): ")

    if choice == '1':
        print("\nStarting Human Play...")
        print("Controls: [SPACE]=Jump, [DOWN]=Duck/FastFall, [P]=Pause")
        game_instance = Game.Game(render_mode=True)
        game_instance.run() # run() is the human play loop

    elif choice == '2':
        print("\nStarting AI Watch Mode...")
        state_dim = 5
        action_dim = 3
        agent = DQNAgent(state_dim, action_dim, epsilon_start=0, epsilon_end=0)
        model_path = "dino_dqn_model_final.pth" # Default to final model

        try:
            # Load the saved weights into the policy network
            agent.policy_net.load_state_dict(torch.load(model_path, map_location=agent.device))
            agent.policy_net.eval()
            print(f"Loaded trained model from {model_path}")
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}.")
            print("Please train the AI first (Mode 3) or place a trained model file.")
            pygame.quit(); sys.exit()
        except Exception as e:
             print(f"Error loading model: {e}")
             pygame.quit(); sys.exit()

        game_instance = Game.Game(render_mode=True)
        state = game_instance.reset()
        running = True
        current_score = 0 # Track score for display maybe
        while running:
            action = agent.choose_action(state)
            next_state, reward, done = game_instance.step(action)
            current_score += reward # Update score based on reward received
            game_instance.score = current_score # Update game score for UI display
            game_instance.draw() # Draw the frame
            game_instance.game_clock.tick(60) # Control watch speed
            state = next_state

            if done:
                 print(f"AI finished episode. Final Score: {current_score:.2f}. Press R in window to watch again, or close window.")
                 current_score = 0 # Reset score for next watch
                 wait_for_reset = True
                 while wait_for_reset and running:
                     for event in pygame.event.get():
                         if event.type == pygame.QUIT:
                             wait_for_reset = False; running = False
                         if event.type == pygame.KEYDOWN:
                             if event.key == pygame.K_r:
                                 state = game_instance.reset()
                                 wait_for_reset = False
                     game_instance.game_clock.tick(15)

            # Check for QUIT event during AI run
            if not game_instance.handle_events_minimal():
                running = False

    elif choice == '3':
        print("\nExecuting AI Training...")
        # Call the training function from the separate file
        Train.train()
        print("Training process finished.")

    else:
        print("Invalid choice.")

    print("Exiting.")
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    try:
         # Check essential AI imports before running main menu
         from dqn_agent import DQNAgent
         from replay_buffer import ReplayBuffer
         import torch
         import numpy
         from collections import deque
    except ImportError as e:
         print(f"Error: Could not import necessary AI/PyTorch components: {e}")
         print("Please ensure PyTorch, NumPy are installed and")
         print("dqn_agent.py, dqn_model.py, replay_buffer.py exist.")
         sys.exit(1)

    main()