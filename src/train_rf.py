import os, sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

sys.path.append(os.path.dirname(__file__))
from features import engineer_features

def load_sample(n=600, seed=42):
    import numpy as np
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        'dist_road_km': rng.uniform(0, 50, n),
        'dist_settlement_km': rng.uniform(0, 80, n),
        'forest_loss_5y': rng.gamma(2.0, 1.5, n),
        'protected_buffer': rng.integers(0, 2, n),
    })
    logits = -0.06*df['dist_road_km'] - 0.03*df['dist_settlement_km'] + 0.45*df['forest_loss_5y'] + 0.5*df['protected_buffer']
    p = 1/(1+np.exp(-logits/5))
    df['label'] = (rng.uniform(0,1,n) < p).astype(int)
    return df

def main():
    df = load_sample()
    df = engineer_features(df)
    X = df.drop(columns=['label'])
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()
