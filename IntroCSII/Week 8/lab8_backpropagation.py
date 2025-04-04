"""
Neural Network Backpropagation Tutorial
======================================

In this tutorial, you'll learn about neural network backpropagation by implementing
a simple neural network to predict whether it will rain based on temperature and humidity.
Follow along with the worksheet to gain a deeper understanding of how neural networks learn!
You should submit your completed worksheet and the answer to the following questions:

1. What do the parameters in our neural network represent?
2. Why do neural networks need activation functions?
3. Why is the sigmoid function appropriate for the output layer in this task?
4. What happens at each layer during a forward pass?
5. What does the loss represent?
6. Why do we calculate y - o instead of o - y when calculating the error?
7. What does the product of h1 * error represent in w2_1_adjustment?
8. How close did your final prediction get to the target value? What does this tell you
   about how neural networks learn?
9. Describe the pattern you see in the loss graph. Why does the loss decrease more quickly
   at first and then more slowly?
10. How would increasing or decreasing the learning rate affect training?

"""

import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])        # comment these lines out
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])   # after the first run if you want
import numpy as np
import matplotlib.pyplot as plt

#############################################################
# STEP 1: DEFINE NEURAL NETWORK PARAMETERS
#############################################################

# Given values from the worksheet
# QUESTION 1: What do these parameters represent in our neural network?

x1, x2 = 0.5, -0.5  # Inputs (temperature and humidity)
y = 0.6             # Target output (will it rain? 1=yes, 0=no)

# Initial weights
# From input to hidden layer:
w1_11, w1_21 = 0.15, -0.2  # Weights for hidden neuron 1
w1_12, w1_22 = 0.25, 0.2   # Weights for hidden neuron 2

# From hidden to output layer:
w2_1, w2_2 = 0.3, -0.1     # Weights for output neuron

# Learning rate
learning_rate = 0.1

# For visualizing progress
loss_history = []
prediction_history = []

#############################################################
# STEP 2: DEFINE ACTIVATION FUNCTIONS
#############################################################

def relu(x):
    """
    ReLU activation function: returns x if x > 0, otherwise returns 0
    
    QUESTION 2: Why do neural networks need activation functions? 
    What would happen if we didn't use them?

    
    """
    return max(0, x)

def sigmoid(x):
    """
    Sigmoid activation function: maps any input to a value between 0 and 1
    
    QUESTION 3: Why is sigmoid appropriate for the output layer in this task?

    
    """
    return 1 / (1 + np.exp(-x))

#############################################################
# STEP 3: IMPLEMENT THE FORWARD PASS
#############################################################

# This is where our neural network makes a prediction

def forward_pass(x1, x2, w1_11, w1_21, w1_12, w1_22, w2_1, w2_2):
    """
    Performs the forward pass through the neural network
    
    QUESTION 4: Trace the steps of a forward pass. What happens at each layer?

    
    """
    # Input to Hidden Layer
    # Calculate the input to each hidden neuron
    h1_in = x1 * w1_11 + x2 * w1_21
    h2_in = x1 * w1_12 + x2 * w1_22
    
    print(f"Hidden layer inputs: h1_in = {h1_in}, h2_in = {h2_in}")
    
    # Apply ReLU activation function
    h1 = relu(h1_in)
    h2 = relu(h2_in)
    
    print(f"Hidden layer outputs after ReLU: h1 = {h1}, h2 = {h2}")
    
    # Hidden to Output Layer
    # Calculate the input to the output neuron
    o_in = h1 * w2_1 + h2 * w2_2
    
    print(f"Output layer input: o_in = {o_in}")
    
    # Apply Sigmoid activation function
    o = sigmoid(o_in)
    
    print(f"Final output after sigmoid: o = {o}")
    
    # Return all values for use in the backward pass
    return h1_in, h2_in, h1, h2, o_in, o

# Run the forward pass with initial weights
print("\n--- INITIAL FORWARD PASS ---")
h1_in, h2_in, h1, h2, o_in, o = forward_pass(x1, x2, w1_11, w1_21, w1_12, w1_22, w2_1, w2_2)

#############################################################
# STEP 4: CALCULATE THE LOSS
#############################################################

# Calculate how far off our prediction is from the target
loss = 0.5 * (y - o) ** 2
print(f"\nTarget value: {y}")
print(f"Predicted value: {o}")
print(f"Initial loss: {loss}")

# QUESTION 5: What does the loss represent?


#############################################################
# STEP 5: IMPLEMENT THE BACKWARD PASS (BACKPROPAGATION)
#############################################################

# This is where our neural network learns from its mistakes

print("\n--- BEGINNING TRAINING ---")
num_iterations = 150

for iteration in range(num_iterations):
    # Forward pass (prediction)
    h1_in, h2_in, h1, h2, o_in, o = forward_pass(x1, x2, w1_11, w1_21, w1_12, w1_22, w2_1, w2_2)
    
    # Calculate loss
    loss = 0.5 * (y - o) ** 2
    
    # Store history for visualization
    loss_history.append(loss)
    prediction_history.append(o)
    
    # Only print details every 25 iterations to avoid overwhelming output
    if iteration % 25 == 0 or iteration == num_iterations - 1:
        print(f"\nIteration {iteration + 1}:")
        print(f"Prediction: {o}, Loss: {loss}")
    
    #############################################################
    # STEP 5.1: Calculate the error
    #############################################################
    
    # QUESTION 6: Why do we calculate y - o instead of o - y?

    error = y - o
    
    #############################################################
    # STEP 5.2: Update weights in the output layer
    #############################################################
    
    # QUESTION 7: What does the product of h1 * error represent in w2_1_adjustment?

    w2_1_adjustment = learning_rate * h1 * error
    w2_2_adjustment = learning_rate * h2 * error
    
    # Update the weights for the output layer
    w2_1 = w2_1 + w2_1_adjustment
    w2_2 = w2_2 + w2_2_adjustment
    
    #############################################################
    # STEP 5.3: Update weights in the hidden layer
    #############################################################
    
    # In a full implementation, we would calculate the exact influence of each weight
    # using calculus (the chain rule). For this simplified tutorial, we're using a
    # fixed influence value of 0.1 with the sign of the error.
    
    error_sign = np.sign(error)  # Will be +1 if error is positive, -1 if negative
    influence = 0.1 * error_sign

    # Calculate adjustments for the first hidden neuron (h1)
    w1_11_adjustment = learning_rate * x1 * influence
    w1_21_adjustment = learning_rate * x2 * influence
    
    # Calculate adjustments for the second hidden neuron (h2)
    w1_12_adjustment = learning_rate * x1 * influence
    w1_22_adjustment = learning_rate * x2 * influence
    
    # Update the weights for the hidden layer
    w1_11 = w1_11 + w1_11_adjustment
    w1_21 = w1_21 + w1_21_adjustment
    w1_12 = w1_12 + w1_12_adjustment
    w1_22 = w1_22 + w1_22_adjustment

# Print the final weights after training
print("\n--- TRAINING COMPLETE ---")
print("\nFinal weights:")
print(f"w1_11 = {w1_11}, w1_21 = {w1_21}")
print(f"w1_12 = {w1_12}, w1_22 = {w1_22}")
print(f"w2_1 = {w2_1}, w2_2 = {w2_2}")

# Final forward pass with updated weights
print("\n--- FINAL FORWARD PASS ---")
_, _, _, _, _, final_output = forward_pass(x1, x2, w1_11, w1_21, w1_12, w1_22, w2_1, w2_2)
final_loss = 0.5 * (y - final_output) ** 2

print(f"\nInitial prediction: {prediction_history[0]}")
print(f"Final prediction: {final_output}")
print(f"Target: {y}")
print(f"Initial loss: {loss_history[0]}")
print(f"Final loss: {final_loss}")

#############################################################
# STEP 6: VISUALIZE THE LEARNING PROCESS
#############################################################

plt.figure(figsize=(12, 5))

# Plot the loss over time
plt.subplot(1, 2, 1)
plt.plot(loss_history)
plt.title('Loss over Training Iterations')
plt.xlabel('Iteration')
plt.ylabel('Loss')
plt.grid(True)

# Plot the prediction over time
plt.subplot(1, 2, 2)
plt.plot(prediction_history)
plt.axhline(y=y, color='r', linestyle='--', label=f'Target ({y})')
plt.title('Prediction over Training Iterations')
plt.xlabel('Iteration')
plt.ylabel('Prediction')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('learning_progress.png')  # Save the figure
plt.show()

#############################################################
# STEP 7: REFLECTION QUESTIONS
#############################################################

# QUESTION 8: How close did your final prediction get to the target value?
# What does this tell you about how neural networks learn?


# QUESTION 9: Look at the loss graph. Describe the pattern you see.
# Why does the loss decrease more quickly at first and then more slowly?


# QUESTION 10: If we increased the learning rate, how would that affect training?
# What if we decreased it?

"""
Congratulations! You've successfully implemented a simple neural network with
backpropagation. This demonstrates the fundamental process behind how neural
networks learn from data. The key steps are:

1. Forward pass: Make a prediction based on current weights
2. Calculate error: Compare prediction to the target
3. Backward pass: Update weights based on their contribution to the error
4. Repeat: Continue this process to improve predictions over time

This same basic approach underlies much more complex neural networks used
in modern machine learning applications!
"""