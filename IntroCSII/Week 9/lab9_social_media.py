"""
Social Media's Impact on Democracy
==================================

In this tutorial, we'll explore how social media impacts democratic processes
through data analysis using Python. We'll work with simulated data that mimics
real-world patterns of social media engagement, filter bubbles, and information spread.
"""

# First, let's import the libraries we'll need
import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"]) 

import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(5)  # For reproducibility
np.random.seed(5)

#################################################
#
# Section 1: Creating a simulated social media network
#
#################################################

print("\nSECTION 1: SIMULATING A SOCIAL MEDIA NETWORK\n")

# Let's create some simulated users with political leanings
# We'll use a scale from -10 (very liberal) to 10 (very conservative)
def create_users(num_users):
    """Create a specified number of simulated social media users."""
    users = []
    for i in range(num_users):
        # Create a user with an ID and a political leaning
        user = {
            "id": i,
            "political_leaning": random.uniform(-10, 10),
            "friends": set(),
            "posts_seen": [],
            "beliefs": {}
        }
        users.append(user)
    return users

# Create 100 users
all_users = create_users(100)

print(f"Created {len(all_users)} simulated social media users.")
print(f"Example user: {all_users[0]}")

"""
QUESTION 1: Understanding the data structure
--------------------------------------------
Look at the user dictionary above. What information does it store about each user?
How would you classify a user with a political_leaning of -8? What about +5?
"""

# To visualize the political distribution of our users
political_leanings = [user["political_leaning"] for user in all_users]

plt.figure(figsize=(10, 6))
plt.hist(political_leanings, bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Political Leanings in Our Simulated Social Network")
plt.xlabel("Political Leaning (-10: Very Liberal, +10: Very Conservative)")
plt.ylabel("Number of Users")
plt.grid(axis='y', alpha=0.75)
plt.show()

"""
QUESTION 2: Exploring the distribution
--------------------------------------
Based on the histogram above, how would you describe the political makeup of our
simulated social network? Is it balanced? Skewed? What might this distribution 
mean for information flow in the network?
"""

#################################################
#
# Section 2: Creating social connections (friend networks)
#
#################################################

print("\nSECTION 2: CREATING SOCIAL CONNECTIONS\n")

def create_friendships(users, homophily_factor=0.7):
    """
    Connect users into a social network.
    The homophily_factor (0-1) determines how likely users are to connect
    with others who have similar political views.
    """
    for user in users:
        # Each user will make between 5-15 friend connections
        num_friends = random.randint(5, 15)
        potential_friends = users.copy()
        potential_friends.remove(user)  # Can't be friends with yourself
        
        for _ in range(num_friends):
            if not potential_friends:  # If no more potential friends
                break
                
            if random.random() < homophily_factor:
                # Homophilic connection - connect with someone similar
                # Calculate "political distance" to all potential friends
                distances = []
                for pfriend in potential_friends:
                    distance = abs(user["political_leaning"] - pfriend["political_leaning"])
                    distances.append((pfriend, distance))
                
                # Sort by distance (closest first)
                distances.sort(key=lambda x: x[1])
                
                # Pick one of the 10 closest or all if fewer than 10
                closest = distances[:min(10, len(distances))]
                friend = random.choice(closest)[0]
            else:
                # Random connection
                friend = random.choice(potential_friends)
            
            # Add the friendship (both ways)
            user["friends"].add(friend["id"])
            friend["friends"].add(user["id"])
            
            # Remove from potential friends to avoid duplicate connections
            potential_friends.remove(friend)

# Create friendships with high homophily (people tend to connect with similar others)
create_friendships(all_users, homophily_factor=0.7)

# Calculate average number of friends
avg_friends = sum(len(user["friends"]) for user in all_users) / len(all_users)
print(f"Average number of friends per user: {avg_friends:.2f}")

# Show friendship count distribution
friend_counts = [len(user["friends"]) for user in all_users]
plt.figure(figsize=(10, 6))
plt.hist(friend_counts, bins=range(max(friend_counts)+2), color='lightgreen', edgecolor='black')
plt.title("Distribution of Friend Counts")
plt.xlabel("Number of Friends")
plt.ylabel("Number of Users")
plt.grid(axis='y', alpha=0.75)
plt.show()

"""
QUESTION 3: Homophily in social networks
----------------------------------------
We used a homophily_factor of 0.7, meaning users have a 70% chance of connecting
with similar-minded people. Why is this important for understanding social media's
impact on democracy? How might changing this factor affect information spread?

Try modifying the homophily_factor value to 0.3 and rerun the code. What changes?
"""

# Let's check if users with similar politics actually have more connections
def analyze_political_friendships(users):
    """Analyze how political leaning affects friendship patterns."""
    results = []
    for user in users:
        # Get friends' political leanings
        friend_politics = [
            users[friend_id]["political_leaning"] 
            for friend_id in user["friends"]
        ]
        
        # Calculate average political leaning of friends
        avg_friend_leaning = sum(friend_politics) / len(friend_politics) if friend_politics else 0
        
        # Calculate political distance (how different user is from their friends)
        avg_distance = abs(user["political_leaning"] - avg_friend_leaning)
        
        results.append({
            "user_id": user["id"],
            "user_leaning": user["political_leaning"],
            "avg_friend_leaning": avg_friend_leaning,
            "political_distance": avg_distance
        })
    
    return results

friendship_analysis = analyze_political_friendships(all_users)

# Plot user political leaning vs. friends' average leaning
user_leanings = [data["user_leaning"] for data in friendship_analysis]
friend_leanings = [data["avg_friend_leaning"] for data in friendship_analysis]

plt.figure(figsize=(10, 6))
plt.scatter(user_leanings, friend_leanings, alpha=0.6)
plt.plot([-10, 10], [-10, 10], 'r--')  # Diagonal line for reference
plt.title("User Political Leaning vs. Friends' Average Leaning")
plt.xlabel("User Political Leaning")
plt.ylabel("Average Political Leaning of Friends")
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.grid(True)
plt.show()

"""
QUESTION 4: Echo chambers
-------------------------
Look at the scatter plot above. The diagonal red line represents where users
and their friends have identical political leanings.

How would you describe the relationship between a user's political leaning
and that of their friends? Do you see evidence of echo chambers? What implications
might this have for political discourse in social media?
"""

#################################################
#
# Section 3: Simulating information spread
#
#################################################

print("\nSECTION 3: INFORMATION SPREAD & BELIEF FORMATION\n")

# Create some news stories with inherent political slant
def create_news_stories(num_stories=50):
    """Create simulated news stories with political leanings."""
    stories = []
    # Topics relevant to democracy
    topics = ["election", "voting", "candidate", "policy", "scandal", 
              "protest", "rights", "legislation", "campaign", "debate"]
    
    for i in range(num_stories):
        # Create a story with an ID, topic, and political slant
        story = {
            "id": i,
            "topic": random.choice(topics),
            "political_slant": random.uniform(-10, 10),
            "factual_accuracy": random.uniform(0.5, 1.0),  # Higher is more accurate
            "virality": random.uniform(0.1, 0.9)  # Likelihood of being shared
        }
        stories.append(story)
    return stories

# Create 50 news stories
news_stories = create_news_stories(50)

print(f"Created {len(news_stories)} simulated news stories.")
print(f"Example story: {news_stories[0]}")

# Visualize the stories by political slant and accuracy
political_slants = [story["political_slant"] for story in news_stories]
factual_accuracy = [story["factual_accuracy"] for story in news_stories]

plt.figure(figsize=(10, 6))
plt.scatter(political_slants, factual_accuracy, alpha=0.7)
plt.title("News Stories: Political Slant vs. Factual Accuracy")
plt.xlabel("Political Slant (-10: Very Liberal, +10: Very Conservative)")
plt.ylabel("Factual Accuracy (0-1)")
plt.grid(True)
plt.show()

"""
QUESTION 5: Analyzing news content
----------------------------------
Looking at the scatter plot, do you notice any patterns between political slant
and factual accuracy in our simulated news stories? What might this suggest
about news content in the real world? What other factors might influence the
factual accuracy of news on social media?
"""

# Simulate how news spreads through the network
def simulate_news_feed(users, stories, days=30):
    """Simulate a personalized news feed algorithm."""
    for day in range(days):
        print(f"Simulating day {day+1}...")
        
        # Each user sees some stories in their feed
        for user in users:
            # Personalized feed: more likely to see content aligned with their views
            # and shared by friends
            
            # Weight stories by how closely they align with user's politics
            weighted_stories = []
            for story in stories:
                # Political alignment (higher when views match)
                political_alignment = 1 - (abs(user["political_leaning"] - story["political_slant"]) / 20)
                
                # Stories shared by friends get a boost
                friend_boost = 1.0
                for friend_id in user["friends"]:
                    if any(s["id"] == story["id"] for s in users[friend_id]["posts_seen"]):
                        friend_boost = 2.0
                        break
                
                # Overall weight
                weight = political_alignment * friend_boost * story["virality"]
                weighted_stories.append((story, weight))
            
            # Sort by weight (descending)
            weighted_stories.sort(key=lambda x: x[1], reverse=True)
            
            # User sees top 5 stories
            feed = [s[0] for s in weighted_stories[:5]]
            user["posts_seen"].extend(feed)
            
            # User forms/updates beliefs based on what they see
            for story in feed:
                topic = story["topic"]
                # If this is a new topic, initialize belief
                if topic not in user["beliefs"]:
                    # Initial belief is influenced by the story's slant
                    # and moderated by user's existing political leaning
                    user["beliefs"][topic] = (
                        story["political_slant"] * 0.6 + 
                        user["political_leaning"] * 0.4
                    )
                else:
                    # Update existing belief
                    current_belief = user["beliefs"][topic]
                    # Belief update depends on story accuracy and how much it confirms
                    # existing beliefs
                    confirmation_bias = 1 - (abs(current_belief - story["political_slant"]) / 20)
                    update_strength = story["factual_accuracy"] * confirmation_bias * 0.2
                    
                    # Update belief
                    new_belief = current_belief * (1 - update_strength) + story["political_slant"] * update_strength
                    user["beliefs"][topic] = new_belief

# Run the simulation for 10 days
simulate_news_feed(all_users, news_stories, days=10)

# Analyze what happened to beliefs
def analyze_belief_polarization(users):
    """Analyze how users' beliefs evolved."""
    topics = set()
    for user in users:
        topics.update(user["beliefs"].keys())
    
    topic_data = {}
    for topic in topics:
        beliefs = [user["beliefs"].get(topic, None) for user in users if topic in user["beliefs"]]
        topic_data[topic] = beliefs
    
    return topic_data

belief_data = analyze_belief_polarization(all_users)

# Pick one topic to visualize
sample_topic = list(belief_data.keys())[0]
print(f"Analyzing belief distribution for topic: '{sample_topic}'")

plt.figure(figsize=(10, 6))
plt.hist(belief_data[sample_topic], bins=20, color='coral', edgecolor='black')
plt.title(f"Distribution of Beliefs on '{sample_topic}' After News Exposure")
plt.xlabel("Belief Position (-10: Very Liberal, +10: Very Conservative)")
plt.ylabel("Number of Users")
plt.grid(axis='y', alpha=0.75)
plt.show()

"""
QUESTION 6: Belief polarization
-------------------------------
Compare the histogram of beliefs on this topic with the original political
distribution from Exercise 2. How have users' beliefs evolved? Do you see any
evidence of polarization (opinions clustering at the extremes)? 

Why might social media algorithms contribute to political polarization in
democratic societies?
"""

# Let's measure and visualize polarization over time
def calculate_polarization(beliefs):
    """
    Calculate polarization as the standard deviation of beliefs.
    Higher values indicate more spread out (polarized) beliefs.
    """
    return np.std(beliefs)

# For every topic, compare polarization to initial political distribution
initial_polarization = np.std(political_leanings)
topic_polarization = {}

for topic, beliefs in belief_data.items():
    topic_polarization[topic] = calculate_polarization(beliefs)

# Sort topics by polarization level
sorted_topics = sorted(topic_polarization.items(), key=lambda x: x[1], reverse=True)

topics = [item[0] for item in sorted_topics]
polarization_values = [item[1] for item in sorted_topics]

plt.figure(figsize=(12, 6))
bars = plt.bar(topics, polarization_values, color='lightcoral')
plt.axhline(y=initial_polarization, color='blue', linestyle='--', label='Initial Political Polarization')
plt.title("Belief Polarization by Topic Compared to Initial Political Distribution")
plt.xlabel("Topic")
plt.ylabel("Polarization (Standard Deviation)")
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""
QUESTION 7: Topic-based polarization
------------------------------------
Which topics show the highest polarization? Why might some topics be more
polarizing than others on social media? How does this relate to democratic 
discourse and decision-making?
"""

#################################################
#
# Section 4: Network analysis and information bubbles
#
#################################################

print("\nSECTION 4: NETWORK ANALYSIS & INFORMATION BUBBLES\n")

# Analyze how similar users' feeds are within vs. across political groups
def analyze_feed_similarity(users):
    """Analyze similarity of content in users' feeds based on political leaning."""
    # Group users by political leaning
    liberal_users = [u for u in users if u["political_leaning"] < -3]
    moderate_users = [u for u in users if -3 <= u["political_leaning"] <= 3]
    conservative_users = [u for u in users if u["political_leaning"] > 3]
    
    # Get feed content for each group
    liberal_feeds = [set(post["id"] for post in user["posts_seen"]) for user in liberal_users]
    moderate_feeds = [set(post["id"] for post in user["posts_seen"]) for user in moderate_users]
    conservative_feeds = [set(post["id"] for post in user["posts_seen"]) for user in conservative_users]
    
    # Calculate within-group similarity (average Jaccard similarity)
    def calculate_avg_jaccard(feeds):
        if len(feeds) <= 1:
            return 0
        
        similarities = []
        for i in range(len(feeds)):
            for j in range(i+1, len(feeds)):
                intersection = len(feeds[i] & feeds[j])
                union = len(feeds[i] | feeds[j])
                if union > 0:  # Avoid division by zero
                    similarity = intersection / union
                    similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0
    
    # Calculate cross-group similarity
    def calculate_cross_group_jaccard(feeds1, feeds2):
        if not feeds1 or not feeds2:
            return 0
        
        similarities = []
        for feed1 in feeds1:
            for feed2 in feeds2:
                intersection = len(feed1 & feed2)
                union = len(feed1 | feed2)
                if union > 0:  # Avoid division by zero
                    similarity = intersection / union
                    similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0
    
    # Within-group similarities
    liberal_similarity = calculate_avg_jaccard(liberal_feeds)
    moderate_similarity = calculate_avg_jaccard(moderate_feeds)
    conservative_similarity = calculate_avg_jaccard(conservative_feeds)
    
    # Cross-group similarities
    lib_con_similarity = calculate_cross_group_jaccard(liberal_feeds, conservative_feeds)
    lib_mod_similarity = calculate_cross_group_jaccard(liberal_feeds, moderate_feeds)
    mod_con_similarity = calculate_cross_group_jaccard(moderate_feeds, conservative_feeds)
    
    return {
        "liberal_similarity": liberal_similarity,
        "moderate_similarity": moderate_similarity,
        "conservative_similarity": conservative_similarity,
        "liberal_conservative_similarity": lib_con_similarity,
        "liberal_moderate_similarity": lib_mod_similarity,
        "moderate_conservative_similarity": mod_con_similarity
    }

similarity_analysis = analyze_feed_similarity(all_users)

# Visualize the results
groups = ["Liberal", "Moderate", "Conservative"]
within_group = [
    similarity_analysis["liberal_similarity"],
    similarity_analysis["moderate_similarity"],
    similarity_analysis["conservative_similarity"]
]

# For cross-group, we'll average the relevant pairs
cross_group = [
    (similarity_analysis["liberal_moderate_similarity"] + 
     similarity_analysis["liberal_conservative_similarity"]) / 2,
    (similarity_analysis["liberal_moderate_similarity"] + 
     similarity_analysis["moderate_conservative_similarity"]) / 2,
    (similarity_analysis["liberal_conservative_similarity"] + 
     similarity_analysis["moderate_conservative_similarity"]) / 2
]

x = np.arange(len(groups))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x - width/2, within_group, width, label='Within Group Similarity')
plt.bar(x + width/2, cross_group, width, label='Cross Group Similarity')
plt.title('Content Similarity Within vs. Across Political Groups')
plt.xlabel('Political Group')
plt.ylabel('Average Content Similarity (Jaccard)')
plt.xticks(x, groups)
plt.legend()
plt.tight_layout()
plt.show()

"""
QUESTION 8: Information bubbles
-------------------------------
Based on the chart above, what can you say about the "information bubbles" 
that form in our simulated social network? Do users across the political
spectrum see similar content? What are the democratic implications of these
filtering effects?
"""

#################################################
#
# Section 5: Misinformation spread
#
#################################################

print("\nSECTION 5: MISINFORMATION SPREAD\n")

# Let's introduce some "fake news" and see how it spreads
def simulate_misinformation(users, days=5):
    """Simulate the spread of a single piece of misinformation."""
    # Create a fake news story with very low factual accuracy
    fake_story = {
        "id": 999,
        "topic": "election",
        "political_slant": 8,  # Strongly conservative
        "factual_accuracy": 0.1,  # Very inaccurate
        "virality": 0.9  # Highly viral
    }
    
    # Initially seed the story to 5 random users
    seed_users = random.sample(users, 5)
    for user in seed_users:
        user["has_fake_news"] = True
        user["believes_fake_news"] = random.random() < 0.8  # 80% chance of believing
    
    # Track spread over time
    spread_data = []
    belief_data = []
    
    for day in range(days):
        # Count users with fake news
        users_with_fake = sum(1 for user in users if user.get("has_fake_news", False))
        users_believing_fake = sum(1 for user in users if user.get("believes_fake_news", False))
        
        spread_data.append(users_with_fake)
        belief_data.append(users_believing_fake)
        
        print(f"Day {day+1}: {users_with_fake} users have seen the fake news, {users_believing_fake} believe it")
        
        # Spread to friends
        new_exposures = []
        for user in users:
            if user.get("has_fake_news", False):
                # User shares the story with probability based on if they believe it
                sharing_prob = 0.7 if user.get("believes_fake_news", False) else 0.2
                if random.random() < sharing_prob:
                    # Share with all friends
                    for friend_id in user["friends"]:
                        if not users[friend_id].get("has_fake_news", False):
                            new_exposures.append(friend_id)
        
        # Mark the newly exposed users
        for user_id in new_exposures:
            users[user_id]["has_fake_news"] = True
            
            # Probability of believing depends on political alignment
            political_alignment = 1 - (abs(users[user_id]["political_leaning"] - fake_story["political_slant"]) / 20)
            belief_prob = 0.3 + (political_alignment * 0.6)  # Base 30% + up to 60% more if aligned
            users[user_id]["believes_fake_news"] = random.random() < belief_prob
    
    return spread_data, belief_data

# Run the misinformation simulation
misinformation_spread, misinformation_belief = simulate_misinformation(all_users, days=7)

# Visualize misinformation spread
days = list(range(1, len(misinformation_spread) + 1))

plt.figure(figsize=(10, 6))
plt.plot(days, misinformation_spread, 'r-', marker='o', label='Exposed to Misinformation')
plt.plot(days, misinformation_belief, 'b--', marker='s', label='Believing Misinformation')
plt.title('Spread of Misinformation Through the Network')
plt.xlabel('Day')
plt.ylabel('Number of Users')
plt.legend()
plt.grid(True)
plt.show()

"""
QUESTION 9: Misinformation and democracy
----------------------------------------
Based on the simulation, how quickly does misinformation spread in our social
network? What factors influence whether users believe the misinformation?

What dangers does the rapid spread of misinformation pose to democratic processes
like elections? Can you think of real-world examples where this has happened?
"""

#################################################
#
# Section 6: Interventions and solutions
#
#################################################

print("\nSECTION 6: INTERVENTIONS & SOLUTIONS\n")

# Let's simulate some potential interventions
def simulate_interventions(users, intervention_type):
    """
    Simulate different types of interventions to counter misinformation
    and information bubbles.
    
    Types:
    - 'fact_check': Add fact-checking to posts
    - 'diversity': Expose users to more diverse content
    - 'education': Educate users about media literacy
    """
    # Create a copy of users for this simulation
    users_copy = []
    for user in users:
        user_copy = user.copy()
        user_copy["beliefs"] = user["beliefs"].copy()
        users_copy.append(user_copy)
    
    # Create news stories
    stories = create_news_stories(50)
    
    # Apply the selected intervention
    if intervention_type == 'fact_check':
        # Fact checking intervention: Low accuracy posts get labeled
        for story in stories:
            if story["factual_accuracy"] < 0.7:
                story["fact_checked"] = True
    
    elif intervention_type == 'diversity':
        # Content diversity intervention: We'll implement this during feed generation
        pass
    
    elif intervention_type == 'education':
        # Media literacy education: Users become more skeptical
        for user in users_copy:
            user["media_literate"] = True
    
    # Run simulation with the intervention
    days = 10
    for day in range(days):
        for user in users_copy:
            # Create a feed of stories
            if intervention_type == 'diversity':
                # Diversity intervention: Include some random stories regardless of politics
                weighted_stories = []
                for story in stories:
                    political_alignment = 1 - (abs(user["political_leaning"] - story["political_slant"]) / 20)
                    weight = political_alignment * story["virality"]
                    weighted_stories.append((story, weight))
                
                weighted_stories.sort(key=lambda x: x[1], reverse=True)
                
                # Take top 3 stories from algorithm + 2 random ones for diversity
                top_stories = [s[0] for s in weighted_stories[:3]]
                remaining_stories = [s[0] for s in weighted_stories[3:]]
                random_stories = random.sample(remaining_stories, min(2, len(remaining_stories)))
                feed = top_stories + random_stories
            else:
                # Normal personalized feed
                weighted_stories = []
                for story in stories:
                    political_alignment = 1 - (abs(user["political_leaning"] - story["political_slant"]) / 20)
                    weight = political_alignment * story["virality"]
                    weighted_stories.append((story, weight))
                
                weighted_stories.sort(key=lambda x: x[1], reverse=True)
                feed = [s[0] for s in weighted_stories[:5]]
            
            # Update beliefs based on feed, taking into account interventions
            for story in feed:
                topic = story["topic"]
                
                # Initialize belief if new topic
                if topic not in user["beliefs"]:
                    # Initial belief is influenced by the story, but less so
                    # with media literacy education
                    if intervention_type == 'education' and user.get("media_literate", False):
                        # More skeptical initial belief
                        user["beliefs"][topic] = (
                            story["political_slant"] * 0.4 + 
                            user["political_leaning"] * 0.6
                        )
                    else:
                        # Normal initial belief
                        user["beliefs"][topic] = (
                            story["political_slant"] * 0.6 + 
                            user["political_leaning"] * 0.4
                        )
                else:
                    # Update existing belief
                    current_belief = user["beliefs"][topic]
                    
                    # Adjust how much user is influenced based on interventions
                    if intervention_type == 'fact_check' and story.get("fact_checked", False):
                        # Fact checked stories have less influence if inaccurate
                        update_strength = story["factual_accuracy"] * 0.1
                    elif intervention_type == 'education' and user.get("media_literate", False):
                        # Media literate users are less influenced by confirmation bias
                        confirmation_bias = 1 - (abs(current_belief - story["political_slant"]) / 20) * 0.5
                        update_strength = story["factual_accuracy"] * confirmation_bias * 0.1
                    else:
                        # Normal belief update
                        confirmation_bias = 1 - (abs(current_belief - story["political_slant"]) / 20)
                        update_strength = story["factual_accuracy"] * confirmation_bias * 0.2
                    
                    # Update belief
                    new_belief = current_belief * (1 - update_strength) + story["political_slant"] * update_strength
                    user["beliefs"][topic] = new_belief
    
    # Return belief data for analysis
    topics = set()
    for user in users_copy:
        topics.update(user["beliefs"].keys())
    
    topic_data = {}
    for topic in topics:
        beliefs = [user["beliefs"].get(topic, None) for user in users_copy if topic in user["beliefs"]]
        topic_data[topic] = beliefs
    
    return topic_data

# Run simulations with different interventions
fact_check_data = simulate_interventions(all_users, 'fact_check')
diversity_data = simulate_interventions(all_users, 'diversity')
education_data = simulate_interventions(all_users, 'education')

# Compare polarization under different interventions
# Pick one topic that all interventions produced data for
common_topics = set(fact_check_data.keys()) & set(diversity_data.keys()) & set(education_data.keys())
if common_topics:
    sample_topic = list(common_topics)[0]
    
    polarization_no_intervention = calculate_polarization(belief_data[sample_topic])
    polarization_fact_check = calculate_polarization(fact_check_data[sample_topic])
    polarization_diversity = calculate_polarization(diversity_data[sample_topic])
    polarization_education = calculate_polarization(education_data[sample_topic])
    
    interventions = ['No Intervention', 'Fact Checking', 'Content Diversity', 'Media Literacy']
    polarization_values = [
        polarization_no_intervention,
        polarization_fact_check,
        polarization_diversity,
        polarization_education
    ]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(interventions, polarization_values, color=['gray', 'skyblue', 'lightgreen', 'coral'])
    plt.title(f"Effect of Interventions on Belief Polarization for '{sample_topic}'")
    plt.xlabel("Intervention Type")
    plt.ylabel("Polarization (Standard Deviation)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    """
    QUESTION 10: Evaluating interventions
    -------------------------------------
    Based on the chart above, which intervention appears most effective at reducing
    polarization? Why might this be the case? As a policy maker or platform designer, 
    what combination of interventions would you implement to protect democratic 
    discourse while respecting free speech?
    """
    
# If common_topics was empty, provide feedback
else:
    print("Could not find a common topic across all interventions for comparison.")