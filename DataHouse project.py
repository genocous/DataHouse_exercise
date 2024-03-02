import json
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_distance(a, b):
    # Euclidean distance between two points
    # subtracting the similar attributes of b from the attributes of a and squaring each one
    # then adding them all together and taking the square root of the sum
    return math.sqrt(sum((a[attr] - b[attr]) ** 2 for attr in a))

def calculate_score(applicant, team):
    # Calculate compatibility score between an applicant and the team
    distances = [calculate_distance(applicant['attributes'], member['attributes']) for member in team]
    # The score is the maximum distance divided by the minimum distance
    min_distance = min(distances)
    max_distance = max(distances)
    # If all attributes are identical, return maximum score
    # Ensures that 1 is the ideal value
    if max_distance == 0:
        return 1.0  
    # Invert the scale so that 1 is the best value and 0 is the worst value
    return 1.0 - (min_distance / max_distance)

def calculate_score_df(applicant, member):
    # Calculate compatibility score between an applicant and a team member
    distance = calculate_distance(applicant['attributes'], member['attributes'])
    # If all attributes are identical, return maximum score
    if distance == 0:
        return 1.0  
    # Invert the scale so that 1 is the best value and 0 is the worst value
    return 1.0 - (distance / 10)  # The maximum possible distance is 10

def score_applicants(team, applicants):
    scored_applicants = []
    # Calculate compatibility score for each applicant and add it to the scored_applicants list
    for applicant in applicants:
        score = round(calculate_score(applicant, team), 2) # round each score to 2 decimal places
        scored_applicants.append({"name": applicant["name"], "score": score})
    return scored_applicants

def create_scores_df(team, applicants):
    # Initialize an empty DataFrame
    scores_df = pd.DataFrame(index=[applicant["name"] for applicant in applicants], 
                             columns=[member["name"] for member in team])

    # Calculate compatibility score for each applicant with each team member
    for applicant in applicants:
        for member in team:
            score = round(calculate_score_df(applicant, member), 2) # round each score to 2 decimal places
            # Add the score to the DataFrame in a row with the applicant and the member names
            scores_df.loc[applicant["name"], member["name"]] = score

    return scores_df

def create_heatmap(scores_df):
    # Create a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(scores_df.astype(float), annot=True, cmap='YlGnBu', fmt=".2f")

    # Add labels
    plt.xlabel('Team Members')
    plt.ylabel('Applicants')
    plt.title('Compatibility Scores')

    # Show the plot
    plt.show()

def main():
    # Input data
    data = {
        "team": [
            {"name": "Eddie", "attributes": {"intelligence": 1, "strength": 5, "endurance": 3, "spicyFoodTolerance": 1}},
            {"name": "Will", "attributes": {"intelligence": 9, "strength": 4, "endurance": 1, "spicyFoodTolerance": 6}},
            {"name": "Mike", "attributes": {"intelligence": 3, "strength": 2, "endurance": 9, "spicyFoodTolerance": 5}}
        ],
        "applicants": [
            {"name": "John", "attributes": {"intelligence": 4, "strength": 5, "endurance": 2, "spicyFoodTolerance": 1}},
            {"name": "Jane", "attributes": {"intelligence": 7, "strength": 4, "endurance": 3, "spicyFoodTolerance": 2}},
            {"name": "Joe", "attributes": {"intelligence": 1, "strength": 1, "endurance": 1, "spicyFoodTolerance": 10}}
        ]
    }

    # Calculate compatibility scores
    scored_applicants = score_applicants(data["team"], data["applicants"])

    # Create a DataFrame for the visualization
    scores_df = create_scores_df(data["team"], data["applicants"])

    # Create heat map chart of compatibility scores for the applicants with all the team members
    # 3x3 grid showing how compatible individual applicants are with individual team members
    create_heatmap(scores_df)

    # Output data
    output = {"scoredApplicants": scored_applicants}

    # Print output in JSON format
    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
