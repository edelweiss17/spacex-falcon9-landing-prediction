import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    # 1. Load data
    df_features = pd.read_csv(os.path.join(DATA_DIR, "dataset_part_3.csv"))
    df_target = pd.read_csv(os.path.join(DATA_DIR, "dataset_part_2.csv"))
    
    X = df_features
    Y = df_target["Class"].to_numpy()
    
    # 2. Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # 3. Train-test split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
    
    results = {}
    
    # Model 1: Logistic Regression
    lr_params = {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]}
    lr = LogisticRegression()
    lr_cv = GridSearchCV(lr, lr_params, cv=10)
    lr_cv.fit(X_train, Y_train)
    lr_test_acc = lr_cv.score(X_test, Y_test)
    results["Logistic Regression"] = {
        "best_params": lr_cv.best_params_,
        "train_acc": lr_cv.best_score_,
        "test_acc": lr_test_acc,
        "y_pred": lr_cv.predict(X_test)
    }
    
    # Model 2: Support Vector Machine (SVM)
    svm_params = {
        "kernel": ["linear", "rbf", "sigmoid"],
        "C": np.logspace(-3, 3, 5),
        "gamma": np.logspace(-3, 3, 5)
    }
    svm = SVC()
    svm_cv = GridSearchCV(svm, svm_params, cv=10)
    svm_cv.fit(X_train, Y_train)
    svm_test_acc = svm_cv.score(X_test, Y_test)
    results["Support Vector Machine"] = {
        "best_params": svm_cv.best_params_,
        "train_acc": svm_cv.best_score_,
        "test_acc": svm_test_acc,
        "y_pred": svm_cv.predict(X_test)
    }
    
    # Model 3: Decision Tree Classifier
    tree_params = {
        "criterion": ["gini", "entropy"],
        "splitter": ["best", "random"],
        "max_depth": [2 * n for n in range(1, 10)],
        "max_features": ["sqrt"],
        "min_samples_leaf": [1, 2, 4],
        "min_samples_split": [2, 5, 10]
    }
    tree = DecisionTreeClassifier(random_state=42)
    tree_cv = GridSearchCV(tree, tree_params, cv=10)
    tree_cv.fit(X_train, Y_train)
    tree_test_acc = tree_cv.score(X_test, Y_test)
    results["Decision Tree"] = {
        "best_params": tree_cv.best_params_,
        "train_acc": tree_cv.best_score_,
        "test_acc": tree_test_acc,
        "y_pred": tree_cv.predict(X_test)
    }
    
    # Model 4: K-Nearest Neighbors (KNN)
    knn_params = {
        "n_neighbors": list(range(1, 11)),
        "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
        "p": [1, 2]
    }
    knn = KNeighborsClassifier()
    knn_cv = GridSearchCV(knn, knn_params, cv=10)
    knn_cv.fit(X_train, Y_train)
    knn_test_acc = knn_cv.score(X_test, Y_test)
    results["K-Nearest Neighbors"] = {
        "best_params": knn_cv.best_params_,
        "train_acc": knn_cv.best_score_,
        "test_acc": knn_test_acc,
        "y_pred": knn_cv.predict(X_test)
    }
    
    # Print comparison
    summary_data = []
    for model_name, data in results.items():
        summary_data.append({
            "Model": model_name,
            "CV_Train_Accuracy": data["train_acc"],
            "Test_Accuracy": data["test_acc"]
        })
    summary_df = pd.DataFrame(summary_data)
    print("=== Model Performance Summary ===")
    print(summary_df.to_string(index=False))
    
    # Plot 1: Model Accuracy Comparison Bar Chart
    plt.figure(figsize=(9, 5))
    x_indices = np.arange(len(summary_df))
    bar_width = 0.35
    plt.bar(x_indices - bar_width/2, summary_df["CV_Train_Accuracy"] * 100, width=bar_width, label="Train CV Accuracy", color="#337ab7")
    plt.bar(x_indices + bar_width/2, summary_df["Test_Accuracy"] * 100, width=bar_width, label="Test Accuracy", color="#2ca02c")
    plt.xticks(x_indices, summary_df["Model"], rotation=12, ha="right", fontsize=10)
    plt.ylabel("Accuracy (%)")
    plt.title("Comparison of Machine Learning Models Performance")
    plt.ylim(0, 105)
    plt.legend(loc="lower right")
    for i, row in summary_df.iterrows():
        plt.text(i - bar_width/2, row["CV_Train_Accuracy"]*100 + 1.5, f"{row['CV_Train_Accuracy']*100:.1f}%", ha="center", fontsize=8.5)
        plt.text(i + bar_width/2, row["Test_Accuracy"]*100 + 1.5, f"{row['Test_Accuracy']*100:.1f}%", ha="center", fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "ml_model_accuracy_comparison.png"), dpi=300)
    plt.close()
    
    # Plot 2: Confusion Matrices for All 4 Models
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
    axes = axes.flatten()
    for idx, (m_name, m_data) in enumerate(results.items()):
        ax = axes[idx]
        cm = confusion_matrix(Y_test, m_data["y_pred"])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                    annot_kws={"size": 13, "weight": "bold"},
                    xticklabels=["Failed (0)", "Landed (1)"],
                    yticklabels=["Failed (0)", "Landed (1)"])
        ax.set_title(f"{m_name} (Acc: {m_data['test_acc']*100:.1f}%)", fontsize=11, fontweight="bold", pad=6)
        ax.set_xlabel("Predicted Label", fontsize=9)
        ax.set_ylabel("True Label", fontsize=9)
        ax.tick_params(labelsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "ml_confusion_matrices.png"), dpi=300)
    plt.close()
    
    print("Machine learning models trained and figures generated successfully.")

if __name__ == "__main__":
    main()

