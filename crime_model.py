import pandas as pd
def predict_crime(df):

    predictions = []

    for state in df['state'].unique():
        state_df = df[df['state'] == state].sort_values('year')

        values = state_df['count'].values

        if len(values) < 3:
            continue

        growth_rates = []

        for i in range(1, len(values)):
            prev = values[i-1]
            curr = values[i]

            if prev == 0:
                continue

            growth = (curr - prev) / prev
            growth_rates.append(growth)

        if len(growth_rates) == 0:
            avg_growth = 0
        else:
            avg_growth = sum(growth_rates) / len(growth_rates)

        last_value = values[-1]

        pred_2024 = last_value * (1 + avg_growth)
        pred_2025 = pred_2024 * (1 + avg_growth)

        pred_2024 = max(0, pred_2024)
        pred_2025 = max(0, pred_2025)

        predictions.append({
            'state': state,
            'year': 2024,
            'predicted_crime': int(pred_2024),
            'growth_rate': avg_growth
        })

        predictions.append({
            'state': state,
            'year': 2025,
            'predicted_crime': int(pred_2025),
            'growth_rate': avg_growth
        })

    return pd.DataFrame(predictions)