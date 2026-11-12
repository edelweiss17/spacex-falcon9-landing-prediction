import os
import nbformat as nbf

def build_ml_notebook(output_dir):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# SpaceX Falcon 9 Machine Learning Prediction\n"
            "This notebook builds, tunes, and evaluates four classification algorithms "
            "(Logistic Regression, Support Vector Machine, Decision Tree, K-Nearest Neighbors) "
            "using 10-fold cross-validation GridSearchCV to predict first stage landing outcomes."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from sklearn.model_selection import train_test_split, GridSearchCV\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.svm import SVC\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.metrics import confusion_matrix\n\n"
            "# Load datasets\n"
            "X = pd.read_csv('../data/dataset_part_3.csv')\n"
            "Y = pd.read_csv('../data/dataset_part_2.csv')['Class'].to_numpy()\n"
            "print('Features shape:', X.shape, '| Target shape:', Y.shape)"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Feature Standardization & Train/Test Split\n"
            "Standardize features with `StandardScaler` and split data 80% train / 20% test with `random_state=2`."
        ),
        nbf.v4.new_code_cell(
            "transform = StandardScaler()\n"
            "X_scaled = transform.fit_transform(X)\n\n"
            "X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)\n"
            "print(f'Train samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}')"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Model 1: Logistic Regression\n"
            "Tune regularization `C` using 10-fold cross-validation."
        ),
        nbf.v4.new_code_cell(
            "lr_parameters = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}\n"
            "lr = LogisticRegression()\n"
            "logreg_cv = GridSearchCV(lr, lr_parameters, cv=10)\n"
            "logreg_cv.fit(X_train, Y_train)\n"
            "print('Tuned hyperparameters (best parameters):', logreg_cv.best_params_)\n"
            "print('Train CV accuracy:', logreg_cv.best_score_)\n"
            "lr_acc = logreg_cv.score(X_test, Y_test)\n"
            "print('Test accuracy:', lr_acc)"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Model 2: Support Vector Machine (SVM)\n"
            "Tune kernels and hyperparameters `C` and `gamma`."
        ),
        nbf.v4.new_code_cell(
            "svm_parameters = {'kernel': ['linear', 'rbf', 'sigmoid'], 'C': np.logspace(-3, 3, 5), 'gamma': np.logspace(-3, 3, 5)}\n"
            "svm = SVC()\n"
            "svm_cv = GridSearchCV(svm, svm_parameters, cv=10)\n"
            "svm_cv.fit(X_train, Y_train)\n"
            "print('Tuned hyperparameters:', svm_cv.best_params_)\n"
            "print('Train CV accuracy:', svm_cv.best_score_)\n"
            "svm_acc = svm_cv.score(X_test, Y_test)\n"
            "print('Test accuracy:', svm_acc)"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Model 3: Decision Tree Classifier\n"
            "Tune tree depth, splitting criteria, and minimum sample leaves."
        ),
        nbf.v4.new_code_cell(
            "tree_parameters = {\n"
            "    'criterion': ['gini', 'entropy'],\n"
            "    'splitter': ['best', 'random'],\n"
            "    'max_depth': [2 * n for n in range(1, 10)],\n"
            "    'max_features': ['sqrt'],\n"
            "    'min_samples_leaf': [1, 2, 4],\n"
            "    'min_samples_split': [2, 5, 10]\n"
            "}\n"
            "tree = DecisionTreeClassifier(random_state=42)\n"
            "tree_cv = GridSearchCV(tree, tree_parameters, cv=10)\n"
            "tree_cv.fit(X_train, Y_train)\n"
            "print('Tuned hyperparameters:', tree_cv.best_params_)\n"
            "print('Train CV accuracy:', tree_cv.best_score_)\n"
            "tree_acc = tree_cv.score(X_test, Y_test)\n"
            "print('Test accuracy:', tree_acc)"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Model 4: K-Nearest Neighbors (KNN)\n"
            "Tune `n_neighbors` and distance metrics."
        ),
        nbf.v4.new_code_cell(
            "knn_parameters = {'n_neighbors': list(range(1, 11)), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1, 2]}\n"
            "knn = KNeighborsClassifier()\n"
            "knn_cv = GridSearchCV(knn, knn_parameters, cv=10)\n"
            "knn_cv.fit(X_train, Y_train)\n"
            "print('Tuned hyperparameters:', knn_cv.best_params_)\n"
            "print('Train CV accuracy:', knn_cv.best_score_)\n"
            "knn_acc = knn_cv.score(X_test, Y_test)\n"
            "print('Test accuracy:', knn_acc)"
        ),
        nbf.v4.new_markdown_cell(
            "## 6. Model Comparison & Confusion Matrices\n"
            "Compare the evaluation scores of all 4 models and plot confusion matrices."
        ),
        nbf.v4.new_code_cell(
            "models = ['Logistic Regression', 'SVM', 'Decision Tree', 'KNN']\n"
            "train_scores = [logreg_cv.best_score_, svm_cv.best_score_, tree_cv.best_score_, knn_cv.best_score_]\n"
            "test_scores = [lr_acc, svm_acc, tree_acc, knn_acc]\n\n"
            "df_perf = pd.DataFrame({'Model': models, 'Train_CV_Accuracy': train_scores, 'Test_Accuracy': test_scores})\n"
            "print(df_perf)\n\n"
            "# Bar chart comparison\n"
            "plt.figure(figsize=(9, 4.5))\n"
            "x = np.arange(len(models))\n"
            "w = 0.35\n"
            "plt.bar(x - w/2, [s*100 for s in train_scores], width=w, label='Train CV Accuracy', color='#337ab7')\n"
            "plt.bar(x + w/2, [s*100 for s in test_scores], width=w, label='Test Accuracy', color='#2ca02c')\n"
            "plt.xticks(x, models, fontsize=10)\n"
            "plt.ylabel('Accuracy (%)')\n"
            "plt.title('Machine Learning Models Performance Comparison', fontsize=12, fontweight='bold')\n"
            "plt.ylim(0, 105)\n"
            "plt.legend()\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_code_cell(
            "# Confusion Matrices\n"
            "fig, axes = plt.subplots(2, 2, figsize=(9, 6))\n"
            "model_preds = [\n"
            "    ('Logistic Regression', logreg_cv.predict(X_test), lr_acc),\n"
            "    ('SVM', svm_cv.predict(X_test), svm_acc),\n"
            "    ('Decision Tree', tree_cv.predict(X_test), tree_acc),\n"
            "    ('KNN', knn_cv.predict(X_test), knn_acc)\n"
            "]\n"
            "for idx, (name, y_pred, acc) in enumerate(model_preds):\n"
            "    ax = axes.flatten()[idx]\n"
            "    cm = confusion_matrix(Y_test, y_pred)\n"
            "    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,\n"
            "                xticklabels=['Failed (0)', 'Landed (1)'], yticklabels=['Failed (0)', 'Landed (1)'])\n"
            "    ax.set_title(f'{name} (Acc: {acc*100:.1f}%)', fontsize=10, fontweight='bold')\n"
            "    ax.set_xlabel('Predicted Label')\n"
            "    ax.set_ylabel('True Label')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        )
    ]
    path = os.path.join(output_dir, "05_spacex_machine_learning_prediction.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path

