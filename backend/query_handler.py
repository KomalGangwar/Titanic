import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

df = pd.read_csv("testing.csv")
def handle_query(query: str):
    query = query.lower()
    if "percentage of passengers were male" in query:
        male_count = df[df['Sex'] == 'male'].shape[0]
        total_count = df.shape[0]
        return f"{(male_count / total_count) * 100:.2f}% of passengers were male.",False
    elif "histogram of passenger ages" in query:
        return generate_histogram(),True
    elif "average ticket fare" in query:
        return f"The average ticket fare was {df['Fare'].mean():.2f}.",False
    elif "passengers embarked from each port" in query:
        return df['Embarked'].value_counts().to_dict(),False
    elif "survival rate by class" in query:
        return survival_rate_by_class(),False
    elif "survival rate by gender" in query:
        return survival_rate_by_gender(),False
    elif "age distribution by class" in query:
        return age_distribution_by_class(),True
    else:
        return "I can't answer that yet."

def generate_histogram():
    # Create the plot
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Age'].dropna(), bins=20, kde=True)
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.title("Histogram of Passenger Ages")

    # Save the plot to a binary buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)  # Move cursor to start of the buffer
    plt.close()  # Close the figure to free memory

    return buffer  # Return the BytesIO object


def survival_rate_by_class():
    survival_rates = df.groupby("Pclass")["Survived"].mean().to_dict()
    return {f"Class {k}": f"{v * 100:.2f}%" for k, v in survival_rates.items()}

def survival_rate_by_gender():
    survival_rates = df.groupby("Sex")["Survived"].mean().to_dict()
    return {f"{k.capitalize()}": f"{v * 100:.2f}%" for k, v in survival_rates.items()}

def age_distribution_by_class():
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['Pclass'], y=df['Age'], data=df)
    plt.xlabel("Passenger Class")
    plt.ylabel("Age")
    plt.title("Age Distribution by Class")
    
   
    # Save the plot to a binary buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)  # Move cursor to start of the buffer
    plt.close()  # Close the figure to free memory

    return buffer  # Return the BytesIO object

