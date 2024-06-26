import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv('./plate_predict_dataset.csv')

def predict_crop(crop_name):
    data.fillna(method='ffill', inplace=True)
    crop_data = data[data['name'] == crop_name]
    avg_seed_size = crop_data['seed_size'].mean()

    label_encoder = LabelEncoder()
    data['name_encoded'] = label_encoder.fit_transform(data['name'])

    X = data[['name_encoded']]
    y_seed = data['seed_plate_id']
    y_fertilizer = data['fertilizer_plate_id']
    X_train, X_test, y_seed_train, y_seed_test = train_test_split(X, y_seed, test_size=0.2, random_state=42)
    X_train, X_test, y_fertilizer_train, y_fertilizer_test = train_test_split(X, y_fertilizer, test_size=0.2, random_state=42)

    models = {
        'Decision Tree': DecisionTreeClassifier(),
        'Random Forest': RandomForestClassifier(),
        'SVM': SVC(),
        'KNN': KNeighborsClassifier()
    }

    seed_best_model = None
    seed_best_accuracy = 0

    fertilizer_best_model = None
    fertilizer_best_accuracy = 0

    for name, model in models.items():
        model.fit(X_train, y_seed_train)
        seed_predictions = model.predict(X_test)
        seed_accuracy = accuracy_score(y_seed_test, seed_predictions)
        if seed_accuracy > seed_best_accuracy:
            seed_best_accuracy = seed_accuracy
            seed_best_model = model

        model.fit(X_train, y_fertilizer_train)
        fertilizer_predictions = model.predict(X_test)
        fertilizer_accuracy = accuracy_score(y_fertilizer_test, fertilizer_predictions)
        if fertilizer_accuracy > fertilizer_best_accuracy:
            fertilizer_best_accuracy = fertilizer_accuracy
            fertilizer_best_model = model
        
        print(f"Model: {name}")
        print(f"Seed Plate Accuracy: {seed_accuracy}")
        print(f"Fertilizer Plate Accuracy: {fertilizer_accuracy}")

    crop_name_encoded = label_encoder.transform([crop_name])[0]

    seed_plate_prediction = seed_best_model.predict([[crop_name_encoded]])[0]
    fertilizer_plate_prediction = fertilizer_best_model.predict([[crop_name_encoded]])[0]

    print(f"Predicted seed_plate_id: {seed_plate_prediction}")
    print(f"Predicted fertilizer_plate_id: {fertilizer_plate_prediction}")
    print(f"Average seed size for {crop_name}: {avg_seed_size} mm")

    return seed_plate_prediction, fertilizer_plate_prediction, avg_seed_size