import json
import pandas as pd

# JSON data
json_data = '''
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          [
            [
              -6.8106122479331646,
              61.83143713904167
            ],
            [
              -6.813609780864908,
              61.82692488528252
            ],
            [
              -6.806597115872762,
              61.82588337407043
            ],
            [
              -6.8042220244512635,
              61.83092996886867
            ],
            [
              -6.8106122479331646,
              61.83143713904167
            ]
          ]
        ],
        "type": "Polygon"
      }
    }
  ]
}
'''

# Parse JSON
data = json.loads(json_data)

# Extract coordinates
coordinates = data['features'][0]['geometry']['coordinates'][0]

# Create a DataFrame
df = pd.DataFrame(coordinates, columns=['longitude', 'latitude'])

# Save DataFrame to CSV
df.to_csv('../zones/harbors/fo_sandur.csv', index=False)
