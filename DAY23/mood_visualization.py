import pandas as pd
import matplotlib.pyplot as plt

def visualize_mood():
    
    data = pd.read_csv("mood_data.csv", header=None, names=["Date", "Mood", "Notes"])
    
    
    mood_counts = data['Mood'].value_counts()
    
    
    mood_counts.plot(kind='bar', color='skyblue')
    plt.title('Mood Distribution')
    plt.xlabel('Mood')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_mood()