from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

def readTexts():
    with open('T1/texts.txt', 'r') as file:
        text = file.read()
    return text

def writeTexts(text):
    with open('T1/texts.txt', 'w') as file:
        file.write(text)

# Clean the text file by removing commas and colons
def cleanTextFile():
    text = readTexts()
    cleaned_text = text.replace(',', '').replace(':', '')
    writeTexts(cleaned_text)

# Convert MM/DD/YY to MMDDYY in text
def convertDate(text):
    try:
        parts = text.split(' ')
        if len(parts) >= 2:
            date_str = parts[0]
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            return date_obj.strftime("%m%d%y")
        else:
            print("Date conversion failed for:", text)  # Debug print
            return ""
    except ValueError:
        print("Date conversion failed for:", text)  # Debug print
        return ""

# Count words in text
def countWords(text):
    words = text.split()
    return len(words)

# Store texts from file by date and time
def storeTexts():
    text = readTexts()
    texts = text.split('\n')
    textsByDate = {}
    for t in texts:
        if t.strip() != '':
            date = convertDate(t.strip())
            if date:
                if date in textsByDate:
                    textsByDate[date].append(t)
                else:
                    textsByDate[date] = [t]
            else:
                print("Invalid date format in text:", t)  # Debug print
    return textsByDate

# Graph texts by date and number of texts sent
def graphTextsDate():
    textsByDate = storeTexts()
    dates = list(textsByDate.keys())
    dates.sort()
    all_dates = [datetime.strptime(date, "%m%d%y") for date in dates]
    min_date = min(all_dates)
    max_date = max(all_dates)
    date_range = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]
    texts = [len(textsByDate[date.strftime("%m%d%y")]) if date.strftime("%m%d%y") in textsByDate else 0 for date in date_range]
    plt.plot(date_range, texts, color='black')  # Change the line color to black
    plt.ylabel('')  # Remove the y-axis label
    plt.xlabel('')  # Remove the x-axis label
    plt.title('')  # Remove the title
    plt.xticks(rotation=45)  # Rotate x-axis tick labels by 45 degrees
    plt.xticks([])  # Remove x-axis tick marks
    plt.yticks([])  # Remove y-axis tick marks
    plt.show()

# Graph texts by time of day and number of texts sent
def graphTextsTime():
    text = readTexts()
    texts = text.split('\n')
    times = []
    for t in texts:
        if t.strip() != '':
            try:
                parts = t.split(' ')
                if len(parts) >= 2:
                    time_str = parts[1].strip()
                    hour = datetime.strptime(time_str, "%I%M%p").hour
                    times.append(hour)
                else:
                    print("Time parsing failed for:", t)  # Debug print
            except (IndexError, ValueError) as e:
                print("Time parsing failed for:", t, "Error:", e)  # Debug print
    plt.hist(times, bins=24, range=(0, 24), edgecolor='black', color='black')
    plt.ylabel('')  # Remove the y-axis label
    plt.xlabel('')  # Remove the x-axis label
    plt.title('')  # Remove the title
    plt.xticks(range(0, 24))  # Set x-axis tick marks from 0 to 23
    plt.xticks([])  # Remove x-axis tick marks
    plt.yticks([])  # Remove y-axis tick marks
    plt.show()

# graph number of words by time of day
def graphWordsTime():
    text = readTexts()
    texts = text.split('\n')
    times = []
    words = []
    for t in texts:
        if t.strip() != '':
            try:
                parts = t.split(' ')
                if len(parts) >= 2:
                    time_str = parts[1].strip()
                    hour = datetime.strptime(time_str, "%I%M%p").hour
                    times.append(hour)
                    words.append(countWords(t))
                else:
                    print("Time parsing failed for:", t)  # Debug print
            except (IndexError, ValueError) as e:
                print("Time parsing failed for:", t, "Error:", e)  # Debug print
    plt.scatter(times, words, color='black')
    plt.ylabel('')  # Remove the y-axis label
    plt.xlabel('')  # Remove the x-axis label
    plt.title('')  # Remove the title
    plt.xticks(range(0, 24))  # Set x-axis tick marks from 0 to 23
    plt.xticks([])  # Remove x-axis tick marks
    plt.yticks([])  # Remove y-axis tick marks
    plt.show()

# Graph texts by number of words and date
def graphTextsWordsDate():
    textsByDate = storeTexts()
    dates = list(textsByDate.keys())
    dates.sort()
    all_dates = [datetime.strptime(date, "%m%d%y") for date in dates]
    min_date = min(all_dates)
    max_date = max(all_dates)
    date_range = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]
    words = [sum(countWords(t) for t in textsByDate[date.strftime("%m%d%y")]) if date.strftime("%m%d%y") in textsByDate else 0 for date in date_range]
    plt.plot(date_range, words, color='black')  # Change the line color to black
    plt.ylabel('')  # Remove the y-axis label
    plt.xlabel('')  # Remove the x-axis label
    plt.title('')  # Remove the title
    plt.xticks(rotation=45)  # Rotate x-axis tick labels by 45 degrees
    plt.xticks([])  # Remove x-axis tick marks
    plt.yticks([])  # Remove y-axis tick marks
    plt.show()

# Main
cleanTextFile()
graphTextsDate()
graphTextsTime()
graphWordsTime()
graphTextsWordsDate()
