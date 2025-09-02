import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['inv_dist_road'] = 1.0 / (1.0 + df['dist_road_km'])
    df['inv_dist_settlement'] = 1.0 / (1.0 + df['dist_settlement_km'])
    denom = (df['forest_loss_5y'].max() - df['forest_loss_5y'].min()) or 1.0
    df['forest_loss_norm'] = (df['forest_loss_5y'] - df['forest_loss_5y'].min()) / denom
    return df
