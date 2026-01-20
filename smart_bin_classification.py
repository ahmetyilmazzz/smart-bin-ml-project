import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression



df = pd.read_csv("Smart_Bin.csv")
print("Veri seti boyutu:", df.shape)
print("Class dağılımı:\n", df["Class"].value_counts(), "\n")


# doluluk artışını hesaplıyorum
df["Doluluk_Artisi"] = df["FL_B"] - df["FL_A"]

# pivot tabloları oluşturuyorum
pivot_fl_b = df.pivot_table(values="FL_B", index="Container Type",
                            columns="Recyclable fraction", aggfunc="mean")
pivot_fl_a = df.pivot_table(values="FL_A", index="Container Type",
                            columns="Recyclable fraction", aggfunc="mean")
pivot_delta = df.pivot_table(values="Doluluk_Artisi", index="Container Type",
                             columns="Recyclable fraction", aggfunc="mean")

print("PIVOT 1 - mean(FL_B)\n", pivot_fl_b, "\n")
print("PIVOT 2 - mean(FL_A)\n", pivot_fl_a, "\n")
print("PIVOT 3 - mean(FL_B-FL_A) (dolma artışı)\n", pivot_delta, "\n")

max_val = pivot_delta.max().max()
best = pivot_delta.stack().idxmax()
print(f">>> EN HIZLI DOLAN: {best[0]} + {best[1]} | Ortalama artış: {max_val:.2f}\n")

# heatmap'i çizip kaydediyorum

os.makedirs("images", exist_ok=True)
plt.figure(figsize=(10, 7))
sns.heatmap(pivot_delta, annot=True, fmt=".2f", cmap="YlOrRd")
plt.title("Konteyner Tipi x Atık Türü - Ortalama Doluluk Artışı (FL_B - FL_A)")
plt.xlabel("Recyclable fraction")
plt.ylabel("Container Type")
plt.tight_layout()
plt.savefig("images/pivot_heatmap.png", dpi=150)
plt.close()
print("Heatmap kaydedildi: images/pivot_heatmap.png\n")

# eksik konteyner tiplerini mod ile doldurdum
df["Container Type"] = df["Container Type"].fillna(df["Container Type"].mode()[0])

# kategorik verileri sayıya çeviriyorum

le_cont = LabelEncoder()
le_rec = LabelEncoder()
le_y = LabelEncoder()

df["Container_Enc"] = le_cont.fit_transform(df["Container Type"])
df["Recyclable_Enc"] = le_rec.fit_transform(df["Recyclable fraction"])
y = le_y.fit_transform(df["Class"])


features = ["FL_A", "FL_B", "Doluluk_Artisi", "VS", "Container_Enc", "Recyclable_Enc"]
X = df[features].fillna(df[features].median())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3 farklı modeli deniyorum
models = {
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=42),
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred, average="weighted")
    results.append((name, acc, f1))
    print(f"{name}: Accuracy={acc:.4f} | F1={f1:.4f}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, pred), "\n")

best_model = max(results, key=lambda x: x[1])
print(f"En iyi model (Accuracy'ye göre): {best_model[0]} (Accuracy={best_model[1]:.4f})")

# confusion matrix çizdiriyorum
best_model_name = best_model[0]
best_model_obj = models[best_model_name]
best_pred = best_model_obj.predict(X_test)
cm = confusion_matrix(y_test, best_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=le_y.classes_, yticklabels=le_y.classes_)
plt.title(f"Confusion Matrix - {best_model_name}")
plt.xlabel("Tahmin Edilen")
plt.ylabel("Gerçek")
plt.tight_layout()
plt.savefig("images/confusion_matrix.png", dpi=150)
plt.close()
print("Confusion matrix kaydedildi: images/confusion_matrix.png")
