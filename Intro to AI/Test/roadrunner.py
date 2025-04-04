# Import necessary libraries
import gym  # OpenAI Gym for the environment
import numpy as np  
import torch  # For PyTorch-based neural network training
import torch.nn as nn  # Neural network modules
import torch.optim as optim  # Optimizers for training
from collections import deque  # For implementing the replay buffer
import random  
import cv2  # For preprocessing frames (grayscale, resize)
import os  
import json  
import pickle  # saving/loading the replay buffer
# import matplotlib.pyplot as plt  # For plotting 

# Hyperparameters for training the agent
GAMMA = 0.99  # Discount factor for future rewards
LR = 0.00025  # Learning rate for the optimizer
BATCH_SIZE = 32  # Batch size for training from the replay buffer
REPLAY_BUFFER_SIZE = 50000  # Maximum capacity of the replay buffer
EPSILON_DECAY = 0.998  # Decay rate of epsilon (exploration vs. exploitation)
MIN_EPSILON = 0  # Minimum value of epsilon (least exploration)
TARGET_UPDATE_FREQ = 1000  # Frequency of target network updates

# File paths for saving/loading model and progress
SAVE_MODEL_PATH = "IntroAI/RoadRunner/saved_models/model_checkpoint1.pt"  # Path for saving the model
SAVE_PROGRESS_PATH = "IntroAI/RoadRunner/saved_models/training_progress1.json"  # Path for saving training progress
REPLAY_BUFFER_PATH = "IntroAI/RoadRunner/saved_models/replay_buffer1.pkl"  # Path for saving replay buffer

# Set the device for training (use GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Preprocess game frames (Deep Reinforcement Learning - DRL preprocessing step)
def preprocess_frame(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # Resize the frame to 84x84 pixels (standard for DRL)
    resized = cv2.resize(gray, (84, 84), interpolation=cv2.INTER_AREA)
    # Normalize pixel values to range [0, 1]
    return resized / 255.0

# Stack multiple frames for temporal awareness (DRL requirement for CNN input)
def stack_frames(stacked_frames, new_frame, is_new_episode):
    frame = preprocess_frame(new_frame)  # Preprocess the new frame
    if is_new_episode or stacked_frames is None:
        # Initialize with four identical frames for a new episode
        stacked_frames = np.stack([frame] * 4, axis=0)
    else:
        # Append the new frame and discard the oldest frame
        stacked_frames = np.concatenate((stacked_frames[1:, :, :], np.expand_dims(frame, 0)), axis=0)
    return stacked_frames

# Wrapper for reward shaping to improve learning efficiency
class RewardShapingWrapper(gym.Wrapper):
    def __init__(self, env):
        super(RewardShapingWrapper, self).__init__(env)
        self.previous_score = 0  # Track the previous score
        self.previous_lives = 0  # Track the number of lives

    def reset(self, **kwargs):
        # Reset score and lives at the start of an episode
        self.previous_score = 0
        self.previous_lives = 0
        observation, info = self.env.reset(**kwargs)  # Reset the environment
        self.previous_lives = info.get('lives', 0)  # Update the initial number of lives
        return observation, info

    def step(self, action):
        # Step the environment and collect relevant information
        observation, reward, terminated, truncated, info = self.env.step(action)
        current_score = info.get('score', 0)
        # Reward shaping: add a reward proportional to score improvement
        reward += (current_score - self.previous_score) * 0.1
        self.previous_score = current_score
        # Add a small reward for surviving each time step
        reward += 0.01
        current_lives = info.get('lives', self.previous_lives)
        # Penalize the agent for losing a life
        if current_lives < self.previous_lives:
            reward -= 1
            self.previous_lives = current_lives
        return observation, reward, terminated, truncated, info

# Define a Deep Q-Network (DQN) using a Convolutional Neural Network (CNN)
class DQN(nn.Module):
    def __init__(self, action_space):
        super(DQN, self).__init__()
        # Convolutional layers for feature extraction
        self.conv1 = nn.Conv2d(4, 16, kernel_size=8, stride=4)  # Input: 4 stacked frames
        self.conv2 = nn.Conv2d(16, 32, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=3, stride=1)
        # Fully connected layers for action-value prediction
        self.fc1 = nn.Linear(32 * 7 * 7, 256)
        self.fc2 = nn.Linear(256, action_space)

    def forward(self, x):
        # Forward pass through the network
        x = torch.relu(self.conv1(x))  # Apply ReLU activation after each layer
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten the tensor for the fully connected layers
        x = torch.relu(self.fc1(x))
        return self.fc2(x)  # Output action values

# Replay Buffer to store experience tuples for experience replay
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)  # Use deque for fixed-capacity buffer

    def push(self, state, action, reward, next_state, done):
        # Store an experience tuple in the buffer
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        # Sample a batch of experiences randomly from the buffer
        state, action, reward, next_state, done = zip(*random.sample(self.buffer, batch_size))
        return (
            np.array(state),
            torch.LongTensor(action).to(device),
            torch.FloatTensor(reward).to(device),
            np.array(next_state),
            torch.FloatTensor(done).to(device)
        )

    def __len__(self):
        return len(self.buffer)  # Return the number of items in the buffer

# Define a DQN Agent implementing Double Deep Q-Learning
class DQNAgent:
    def __init__(self, action_space):
        self.action_space = action_space  # Number of actions in the environment
        self.policy_net = DQN(action_space).to(device)  # Policy network for action selection
        self.target_net = DQN(action_space).to(device)  # Target network for stable updates
        self.target_net.load_state_dict(self.policy_net.state_dict())  # Initialize with the policy network's weights
        self.target_net.eval()  # Target network is not updated directly
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=LR)  # Adam optimizer for training
        self.replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)  # Replay buffer for experience replay
        self.epsilon = 1  # Start with full exploration (epsilon-greedy)

    def select_action(self, state):
        # Select an action using epsilon-greedy policy
        if random.random() < self.epsilon:
            return env.action_space.sample()  # Random action (exploration)
        else:
            state = torch.FloatTensor(state).unsqueeze(0).to(device)  # Convert state to tensor
            with torch.no_grad():
                return self.policy_net(state).argmax(dim=1).item()  # Choose action with highest Q-value (exploitation)

    def optimize_model(self):
        # Perform one step of optimization using a batch from the replay buffer
        if len(self.replay_buffer) < BATCH_SIZE:
            return  # Skip if there aren't enough samples
        state, action, reward, next_state, done = self.replay_buffer.sample(BATCH_SIZE)
        state = torch.FloatTensor(state).to(device)
        next_state = torch.FloatTensor(next_state).to(device)
        # Calculate Q-values for the current state and selected actions
        q_values = self.policy_net(state).gather(1, action.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            # Use the target network for the next Q-values (Double DQN)
            next_action = self.policy_net(next_state).argmax(dim=1).unsqueeze(1)
            next_q_values = self.target_net(next_state).gather(1, next_action).squeeze(1)
        expected_q_values = reward + GAMMA * next_q_values * (1 - done)  # Compute the target Q-values
        # Calculate the loss using Mean Squared Error
        loss = nn.MSELoss()(q_values, expected_q_values.detach())
        self.optimizer.zero_grad()  # Zero gradients
        loss.backward()  # Backpropagate the loss
        self.optimizer.step()  # Update network weights

    def update_target_network(self):
        # Update the target network with the policy network's weights
        self.target_net.load_state_dict(self.policy_net.state_dict())

# Save model and training progress (including replay buffer)
def save_progress(agent, reward_history):
    os.makedirs(os.path.dirname(SAVE_MODEL_PATH), exist_ok=True)  # Ensure the directory exists
    torch.save(agent.policy_net.state_dict(), SAVE_MODEL_PATH)  # Save policy network weights
    with open(SAVE_PROGRESS_PATH, "w") as f:
        json.dump({"reward_history": reward_history}, f)  # Save reward history
    with open(REPLAY_BUFFER_PATH, "wb") as f:
        pickle.dump(agent.replay_buffer, f)  # Save replay buffer

# Load model and training progress (including replay buffer)
def load_progress(agent):
    reward_history = []
    if os.path.exists(SAVE_MODEL_PATH):
        agent.policy_net.load_state_dict(torch.load(SAVE_MODEL_PATH))  # Load model weights
        agent.target_net.load_state_dict(agent.policy_net.state_dict())  # Sync target network
    if os.path.exists(SAVE_PROGRESS_PATH):
        with open(SAVE_PROGRESS_PATH, "r") as f:
            data = json.load(f)
            reward_history = data.get("reward_history", [])  # Load reward history
    if os.path.exists(REPLAY_BUFFER_PATH):
        with open(REPLAY_BUFFER_PATH, "rb") as f:
            agent.replay_buffer = pickle.load(f)  # Load replay buffer
    return reward_history

# Initialize the Road Runner environment with reward shaping
env = gym.make("ALE/RoadRunner-v5", frameskip=8)  # Initialize the environment
env = RewardShapingWrapper(env)  # Wrap with reward shaping

# Initialize the agent and load progress
agent = DQNAgent(env.action_space.n)  # Create the DQN agent
reward_history = load_progress(agent)  # Load previous training progress

average_rewards = [
    np.mean(reward_history[i:i+10]) for i in range(0, len(reward_history), 10)
]  # Calculate 10-episode average rewards for plotting

# Training loop for reinforcement learning
num_episodes = 1500  # Number of episodes to train
target_update_counter = 0  # Counter for updating the target network

for episode in range(len(reward_history), len(reward_history) + num_episodes):
    state, info = env.reset()  # Reset the environment at the start of an episode
    stacked_frames = stack_frames(None, state, is_new_episode=True)  # Initialize stacked frames
    total_reward = 0  # Track total reward for the episode
    done = False  # Initialize the done flag

    while not done:
        action = agent.select_action(stacked_frames)  # Select an action using epsilon-greedy
        next_state, reward, terminated, truncated, info = env.step(action)  # Take the action
        done = terminated or truncated  # Check if the episode is done
        stacked_frames_next = stack_frames(stacked_frames, next_state, is_new_episode=False)  # Update stacked frames
        agent.replay_buffer.push(stacked_frames, action, reward, stacked_frames_next, done)  # Store experience
        stacked_frames = stacked_frames_next  # Update current stacked frames
        agent.optimize_model()  # Optimize the policy network
        total_reward += reward  # Accumulate reward
        target_update_counter += 1  # Increment the target update counter
        if target_update_counter % TARGET_UPDATE_FREQ == 0:
            agent.update_target_network()  # Update the target network periodically

    reward_history.append(total_reward)  # Store the total reward for the episode
    agent.epsilon = max(MIN_EPSILON, agent.epsilon * EPSILON_DECAY)  # Decay epsilon

    if (episode + 1) % 10 == 0:
        avg_reward = np.mean(reward_history[-10:])  # Calculate average reward for last 10 episodes
        average_rewards.append(avg_reward)  # Append to average rewards
        print(f"Episode {episode + 1}: Average Reward (last 10 episodes): {avg_reward:.2f}, Epsilon: {agent.epsilon:.2f}")
        save_progress(agent, reward_history)  # Save progress periodically

env.close()  # Close the environment