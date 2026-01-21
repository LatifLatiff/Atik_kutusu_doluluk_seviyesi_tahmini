import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

# Veriyi yukle
df = pd.read_csv('Smart_Bin.csv')

df.head()
df.info()
df.describe()
  
# Bos degerleri doldur
sayisal_sutunlar = df.select_dtypes(include=['number']).columns
for sutun in sayisal_sutunlar:
    ortalama = df[sutun].mean()
    df[sutun].fillna(ortalama, inplace=True)

# Grafik ayarlari
sns.set_style("whitegrid")

# Konteyner tipine gore doluluk analizi
pivot = df.pivot_table(index='Container Type', 
                        columns='Recyclable fraction', 
                        values='FL_B', 
                        aggfunc='mean')

plt.figure(figsize=(12, 8))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd")
plt.title('Konteyner ve Atik Turune Gore Doluluk')
plt.show()

# Sinif dagilimi
plt.figure(figsize=(8, 5))
sns.countplot(x='Class', data=df)
plt.title('Sinif Dagilimi')
plt.show()

# Doluluk seviyesi histogrami
plt.figure(figsize=(10, 6))
plt.hist(df['FL_B'], bins=30, color='blue', alpha=0.7)
plt.title('Doluluk Seviyesi Dagilimi')
plt.xlabel('Doluluk (%)')
plt.ylabel('Frekans')
plt.show()

# Konteyner tipine gore doluluk
plt.figure(figsize=(14, 6))
sns.boxplot(x='Container Type', y='FL_B', data=df)
plt.xticks(rotation=45)
plt.title('Konteyner Tipine Gore Doluluk')
plt.show()

# Atik turune gore doluluk
plt.figure(figsize=(10, 6))
sns.boxplot(x='Recyclable fraction', y='FL_B', data=df)
plt.title('Atik Turune Gore Doluluk')
plt.show()

# Korelasyon matrisi
plt.figure(figsize=(10, 8))
korelasyon = df[sayisal_sutunlar].corr()
sns.heatmap(korelasyon, annot=True, cmap='coolwarm')
plt.title('Ozellikler Arasi Korelasyon')
plt.show()

# Verileri modele hazirla
le = LabelEncoder()
veri_model = df.copy()

kategorik_sutunlar = ['Container Type', 'Recyclable fraction', 'Class']
for sutun in kategorik_sutunlar:
    veri_model[sutun] = le.fit_transform(veri_model[sutun])


X = veri_model.drop('Class', axis=1)
y = veri_model['Class'] # Hedef degisken

# Train test olustur
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN icin normalizasyon
scaler = StandardScaler()
X_egitim_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Random Forest modelini egit
model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)
tahmin_rf = model_rf.predict(X_test)
dogruluk_rf = accuracy_score(y_test, tahmin_rf)

# Logistic Regression modelini egit
model_lr = LogisticRegression(max_iter=1000, random_state=42)
model_lr.fit(X_train, y_train)
tahmin_lr = model_lr.predict(X_test)
dogruluk_lr = accuracy_score(y_test, tahmin_lr)

# KNN modelini egit
model_knn = KNeighborsClassifier(n_neighbors=5)
model_knn.fit(X_egitim_scaled, y_train)
tahmin_knn = model_knn.predict(X_test_scaled)
dogruluk_knn = accuracy_score(y_test, tahmin_knn)

# Sonuclari yazdir
print("\n--- Model Sonuclari ---")
print("Random Forest Dogruluk: %.2f%%" % (dogruluk_rf * 100))
print("Logistic Regression Dogruluk: %.2f%%" % (dogruluk_lr * 100))
print("KNN Dogruluk: %.2f%%" % (dogruluk_knn * 100))

