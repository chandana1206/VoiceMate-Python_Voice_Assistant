import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact

# url = 'C:\Users\user\.vscode\vsc\python\ds\data.csv'
data = pd.read_csv('data.csv')
# #read the dataset
# data=pd.read_csv('data.csv')

#shape of the dataset
shape=data.shape
print('Shape of the data set:', shape)

#head of the dataset
data.head()

#check for missing values
data.isnull().sum()

#crops present in the dataset
data['label'].value_counts()

#average values
print("Average Ratio of Nitrogen in the soil: {:.2f}".format(data['N'].mean()))
print("Average Ratio of Phosphorus in the soil: {:.2f}".format(data['P'].mean()))
print("Average Ratio of Potassium in the soil: {:.2f}".format(data['K'].mean()))
print("Average Temperature in Celsius: {:.2f}".format(data['temperature'].mean()))
print("Average Humidity in %: {:.2f}".format(data['humidity'].mean()))
print("Average pH value: {:.2f}".format(data['ph'].mean()))
print("Average Rainfall in mm: {:.2f}".format(data['rainfall'].mean()))

@interact
def summary(crops = list(data['label'].value_counts().index)):
    x = data[data['label']== crops]
    z = data.drop(['label'],axis=1)
    for i in z.columns:
        print(f'Minimum {i} required: {x[i].min():.2f}')
        print(f'Average {i} required: {x[i].mean():.2f}')
        print(f'Maximum {i} required: {x[i].max():.2f}')
        print('--------------------------------------------------')

@interact
def compare(condition=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']):
    # Calculate the average requirement for each crop for the selected condition
    avg_requirements = data.groupby('label')[condition].mean()
    
    # Display the crops and their average requirements for the selected condition
    print(f"Average {condition} requirement for each crop:")
    print('--------------------------------------------------')
    for crop, avg in avg_requirements.items():
        print(f"{crop}: {avg:.2f}")
    print('--------------------------------------------------')

#distribution of conditions

plt.rcParams['figure.figsize']=(15, 7)
    
# Plot distribution
plt.subplot(2,4,1)
sns.histplot(data['N'], color='lightgrey')
plt.xlabel('Ratio of Nitrogen')
plt.ylabel('Frequency')
plt.grid()

plt.subplot(2,4,2)
sns.histplot(data['P'], color='yellow')
plt.xlabel('Ratio of Phosphorous')
plt.ylabel('Frequency')
plt.grid()

plt.subplot(2,4,3)
sns.histplot(data['K'], color='darkblue')
plt.xlabel('Ratio of Potassium')
plt.ylabel('Frequency')
plt.grid()

plt.subplot(2,4,4)
sns.histplot(data['temperature'], color='green')
plt.xlabel('Ratio of temperature')
plt.ylabel('Frequency')
plt.grid()

plt.subplot(2,4,5)
sns.histplot(data['humidity'], color='black')
plt.xlabel('Ratio of humidity')
plt.ylabel('Frequency')
plt.grid()

plt.subplot(2,4,6)
sns.histplot(data['ph'], color='orange')
plt.xlabel('Ratio of ph')
plt.ylabel('Frequency')
plt.grid()

plt.subplot(2,4,7)
sns.histplot(data['rainfall'], color='red')
plt.xlabel('Ratio of rainfall')
plt.ylabel('Frequency')
plt.grid()

plt.tight_layout()
plt.show()

# Find crops with very high or low requirements
print('Crops which require a very high ratio of Nitrogen content in soil:', 
      data[data['N'] > 120]['label'].unique())
print('Crops which require a very high ratio of Phosphorous content in soil:', 
      data[data['P'] > 100]['label'].unique())
print('Crops which require a very high ratio of Potassium content in soil:', 
      data[data['K'] > 200]['label'].unique())
print('Crops which require very high rainfall:', 
      data[data['rainfall'] > 200]['label'].unique())
print('Crops which require a very low temperature:', 
      data[data['temperature'] < 10]['label'].unique())
print('Crops which require a very high temperature:', 
      data[data['temperature'] > 40]['label'].unique())
print('Crops which require very low humidity:', 
      data[data['humidity'] < 20]['label'].unique())
print('Crops which require a very low pH:', 
      data[data['ph'] < 4]['label'].unique())
print('Crops which require a very high pH:', 
      data[data['ph'] > 9]['label'].unique())

print('Summer Crops:', data[(data['temperature']>30) & (data['humidity']>50)]['label'].unique())
print('Winter Crops:', data[(data['temperature']<20) & (data['humidity']>30)]['label'].unique())
print('Rainy Crops:', data[(data['rainfall']>200) & (data['humidity']>30)]['label'].unique())

#clustering analysis
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

x = data.drop(['label'],axis=1)
x = data.loc[:,x.columns].values
x_data = pd.DataFrame(x)
x_data.head()

plt.rcParams['figure.figsize'] = (10,4)
wcss = []
for i in range (1,11):
    km = KMeans(n_clusters =i, init= 'k-means++', max_iter=300, n_init=10, random_state=0)
    km.fit(x)
    wcss.append(km.inertia_)
    
#plot the results
plt.plot(range(1,11), wcss)
plt.title('Elbow Method', fontsize= 15)
plt.xlabel('No. of cluster')
plt.ylabel('wcss')
plt.show()

km = KMeans(n_clusters =4, init= 'k-means++', max_iter=300, n_init=10, random_state=0)
y_means= km.fit_predict(x)

a = data['label']
y_means = pd.DataFrame(y_means)
w = pd.concat([y_means, a], axis=1)
w =w.rename(columns= {0:'cluster'})

for i in range(0,4): #for 4 clusters 0,1,2,3
    print('Crops is cluster', i+1, w[w['cluster']==i]['label'].unique())
    print('--------------------------------------------------------------------')
    
# split the dataset
y=data['label']
x=data.drop(['label'],axis=1)

print('Shape of x:',x.shape)
print('Shape of y:',y.shape)

#Train-Test Split
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

print('Shape of train x:',x_train.shape)
print('Shape of test x:',x_test.shape)
print('Shape of train y:',y_train.shape)
print('Shape of test y:',y_test.shape)

# create predictive model
from sklearn.linear_model import LogisticRegression

model= LogisticRegression()
model.fit(x_train, y_train)

# prediction variable
y_pred=model.predict(x_test)

# evaluate model performace
from sklearn.metrics import classification_report
cr= classification_report(y_test,y_pred)
print(cr)

data.head()

# Take user input
N = float(input("Enter the Nitrogen content in the soil: "))
P = float(input("Enter the Phosphorus content in the soil: "))
K = float(input("Enter the Potassium content in the soil: "))
temperature = float(input("Enter the temperature in Celsius: "))
humidity = float(input("Enter the humidity in percentage: "))
ph = float(input("Enter the pH value of the soil: "))
rainfall = float(input("Enter the rainfall in mm: "))

# Prepare input data for prediction as a NumPy array
user_input = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

# Predict the crop
prediction = model.predict(user_input)
print("The Suggested Crop for given climatic condition is :",prediction)
