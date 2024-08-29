import pandas as pd

"""Script to find overlapping vessel names for same period from PowerBI table."""

# Path to xlsx sheet that is a copy of PowerBI table
path = r"C:\Users\tokit\OneDrive\Desktop\Projects\Vessels with common name in Act profile\double_id.xlsx"
df = pd.read_excel(path)

df['vessel_name'] = df['vessel_name'].str.title()

# Initialize a list to collect vessel names with multiple IDs at overlapping periods
conflicting_vessels = []

# Group by vessel_name
for vessel_name, group in df.groupby('vessel_name'):
    # Track last end date and last vessel_id
    last_end = None
    last_id = None

    # Iterate over each row within the group
    for _, row in group.iterrows():
        current_id = row['vessel_id']
        current_start = row['start']
        current_end = row['end']

        # Check if there's an overlap or consecutive swap of vessel_id
        if last_end and current_start <= last_end and current_id != last_id:
            conflicting_vessels.append(vessel_name)
            break  # No need to check further once a conflict is found

        # Update last_end and last_id for the next iteration
        last_end = current_end
        last_id = current_id

# Remove duplicates if any
conflicting_vessels = list(set(conflicting_vessels))

# Output the results
print("Vessel names with multiple IDs at overlapping or consecutive periods:", conflicting_vessels)
