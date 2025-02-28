import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
    roc_curve
)


def load_and_preprocess_data(csv_path: str) -> (np.ndarray, pd.Series):
    """
    Load the dataset, select features, handle missing values, encode categorical variables,
    and scale the features.
    """
    # Read CSV and select relevant features
    features = [
        'age', 'hypertension', 'heart_disease',
        'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'
    ]
    df = pd.read_csv(csv_path)[features]

    # Drop rows where BMI is missing
    df = df.dropna(subset=['bmi'])

    # Encode 'smoking_status' to numeric values
    df['smoking_status'] = LabelEncoder().fit_transform(df['smoking_status'])

    # Separate features and target variable
    X = df.drop('stroke', axis=1)
    y = df['stroke']

    # Normalize features with Min-Max scaling
    X_scaled = MinMaxScaler().fit_transform(X)
    return X_scaled, y


def tune_hyperparameters(X: np.ndarray, y: pd.Series) -> (dict, KNeighborsClassifier):
    """
    Tune hyperparameters for the KNN classifier using GridSearchCV and return the best parameters
    along with the best estimator.
    """
    param_grid = {
        'n_neighbors': np.arange(1, 31),
        'weights': ['uniform', 'distance'],
        'p': [1, 2]
    }
    
    knn = KNeighborsClassifier()
    grid = GridSearchCV(
        estimator=knn,
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    grid.fit(X, y)
    print(f"Best Hyperparameters: {grid.best_params_}")
    return grid.best_params_, grid.best_estimator_


def plot_roc_curve(fpr, tpr, roc_auc, fold: int):
    """Plot and display the ROC curve for the given fold."""
    plt.figure()
    plt.plot(fpr, tpr, label=f'Fold {fold} (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - Fold {fold}')
    plt.legend()
    plt.show()


def evaluate_model(model: KNeighborsClassifier, X: np.ndarray, y: pd.Series, n_splits: int = 5):
    """
    Evaluate the given model using K-Fold cross-validation.
    Print per-fold metrics and overall performance, and plot ROC curves.
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    accuracies, roc_aucs = [], []

    for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        y_probs = model.predict_proba(X_val)[:, 1]

        accuracy = accuracy_score(y_val, y_pred)
        roc_auc = roc_auc_score(y_val, y_probs)
        accuracies.append(accuracy)
        roc_aucs.append(roc_auc)

        print("\n" + "-" * 43)
        print(f"FOLD {fold} RESULTS")
        print("-" * 43)
        print(f"Accuracy: {accuracy:.4f}")
        print(f"ROC AUC Score: {roc_auc:.4f}")

        report = classification_report(y_val, y_pred, output_dict=True)
        print("\nDetailed Performance Metrics:")
        print("-" * 43)
        print("{:<10} {:<12} {:<10} {:<10} {:<10}".format("Class", "Precision", "Recall", "F1-Score", "Support"))
        print("-" * 43)
        # Correctly map report keys to class labels assuming '0' is No Stroke and '1' is Stroke.
        for label, cls_name in zip(['0', '1'], ["No Stroke", "Stroke"]):
            print("{:<10} {:<12.3f} {:<10.3f} {:<10.3f} {:<10d}".format(
                cls_name,
                report[label]['precision'],
                report[label]['recall'],
                report[label]['f1-score'],
                int(report[label]['support'])
            ))
        print("-" * 43)

        # Plot ROC Curve for this fold
        fpr, tpr, _ = roc_curve(y_val, y_probs)
        plot_roc_curve(fpr, tpr, roc_auc, fold)

    print("\n" + "-" * 43)
    print("Average Performance")
    print("-" * 43)
    print(f"Average Accuracy: {np.mean(accuracies):.4f}")
    print(f"Accuracy Std Dev: {np.std(accuracies):.4f}")
    print(f"Average ROC AUC Score: {np.mean(roc_aucs):.4f}")
    print(f"ROC AUC Std Dev: {np.std(roc_aucs):.4f}")


def main():
    # Load and preprocess data
    X_scaled, y = load_and_preprocess_data('healthcare-dataset-stroke-data.csv')
    
    # Tune hyperparameters using GridSearchCV
    best_params, best_knn = tune_hyperparameters(X_scaled, y)
    
    # Evaluate the tuned KNN model using cross-validation
    evaluate_model(best_knn, X_scaled, y)


if __name__ == '__main__':
    main()
