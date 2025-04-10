import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])

import matplotlib.pyplot as plt

x = [1,2,3,4,5,6]
y = [2,4,8,16,32,64]

### EXAMPLE 1 (line graph)
plt.plot(x,y, c = "red") # plot x and y coords
plt.ylabel("2 raised to the x") # label on y axis
plt.xlabel("x") # label on the x axis
plt.title("Example 1")
plt.show() # command to show the created graph


### EXAMPLE 2 (scatter plot)
x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,100,86,103,87,94,78,77,85,86]

plt.scatter(x,y, c = "blue")
plt.title("Example 2")
plt.show()

### EXAMPLE 3 (change appearance, save output)
# first dataset
x1 = [86,43,36,36,95,10,66,34,38,20]
y1 = [21,46,3,35,67,95,53,72,58,10]

# second dataset
x2 = [26,29,48,64,6,5,36,66,72,40]
y2 = [26,34,90,33,38,20,56,2,47,15]

# markers: s = square, o = circle, ^ = triangle
plt.scatter(x1,y1,c="green", linewidths=2, marker="o",edgecolor="red",s=100)
plt.scatter(x2,y2,c="yellow",linewidths=2,marker="^",edgecolor="red",s=200)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Example 3")

# if saving figures - save before .show(), which resets the plot
plt.savefig("out.jpg")
plt.savefig("out.png")
plt.show()

### EXAMPLE 4 (bar charts)
x = ["a","b","c","d"]
y = [3.2,3.25,3.3,3.4]
plt.bar(x,y)
plt.title("Example 4")
plt.show()