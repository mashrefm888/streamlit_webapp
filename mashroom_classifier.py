from pyexpat import model
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score

def main():
    st.title("Binary Classification Webapp")  ##creating title for the project
    st.sidebar.title("Binary Classification Webapp") ##creating sidebar for the project
    st.markdown ("are your mashrooms edible or poisonous?🍄") ##main page markdown
    st.sidebar.markdown ("are your mashrooms edible or poisonous?🍄") ## sidebar markdown
if __name__=='__main__':
    main()


@st.cache(persist=True)
def load_data():
    data=pd.read_csv('C:/Users/mashr/OneDrive/Desktop/app_folder/mushrooms.csv')
    label=LabelEncoder()
    for col in data.columns:
        data[col]=label.fit_transform(data[col])
    return data

@st.cache(persist=True)

def split(df):
    y=df['class']
    x=df.drop(columns=['class'])
    x_train, x_test, y_train, y_test=train_test_split(x,y,test_size=0.3, random_state=0)
    return x_train, x_test, y_train, y_test

## plot user selected model evaluation matrices
st.set_option('deprecation.showPyplotGlobalUse', False) ##to remove the warnings????--IT WORKS!!!!

def plot_metrices(metrices_list):
    if 'Confusion matrix' in metrices_list:
        st.subheader("Confusion Matrix")
        plot_confusion_matrix(model, x_test, y_test, display_labels=class_names)
        st.pyplot()

    if "ROC Curve" in metrices_list:
        st.subheader("ROC Curve")
        plot_roc_curve(model, x_test, y_test)
        st.pyplot()

    if "Precision-Recall Curve" in metrices_list:
        st.subheader("Precision Recall Curve")
        plot_precision_recall_curve(model, x_test, y_test)
        st.pyplot()


df=load_data()
x_train, x_test, y_train, y_test=split(df)
class_names=['edible', 'poisonous']
st.sidebar.subheader("Choose Classifier")

classifier=st.sidebar.selectbox("Classifier", ("Support Vector Machine (SVM)", "Logistic Regression", "Ramdom Forest"))

if classifier=="Support Vector Machine (SVM)":
    st.sidebar.subheader("Model Hyperparameters")
    C=st.sidebar.number_input("C (Regularization Parameters)", 0.01,10.0, step=0.01, key='C')
    kernel=st.sidebar.radio("kernel", ("rbf", "linear"), key="kernel")
    gamma=st.sidebar.radio("Gamma (kernel coefficient", ("scale", "auto"), key="gamma")

    metrices=st.sidebar.multiselect("What metrices to plot?", ('Confusion matrix', 'ROC Curve','Precision-Recall Curve'))

    if st.sidebar.button("Classify", key='classify'):
        st.subheader("Support Vector Machine Results")
        model=SVC(C=C, kernel=kernel, gamma=gamma)
        model.fit(x_train, y_train)
        accuracy=model.score(x_test, y_test)
        y_pred=model.predict(x_test)
        st.write("Accuracy: ", accuracy.round(2))
        st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
        st.write("Precision: ", recall_score(y_test, y_pred, labels=class_names).round(2))
        plot_metrices(metrices)


##creating checkbox in the sidebar
    if st.sidebar.checkbox("Show raw data", False):
        st.subheader("Mashroom dataset (classification) show")
        st.write(df)


##Creating Logistic Regression Classifier:

if classifier=="Logistic Regression":
    st.sidebar.subheader("Model Hyperparameters")
    C=st.sidebar.number_input("C (Regularization Parameters)", 0.01,10.0, step=0.01, key='C_LR')
    max_iter=st.sidebar.slider("Maximum number of iterations", 100, 500, key='max_iter')


    metrices=st.sidebar.multiselect("What metrices to plot?", ('Confusion matrix', 'ROC Curve','Precision-Recall Curve'))

    if st.sidebar.button("Classify", key='classify'):
        st.subheader("Logistic Regression Results")
        model=LogisticRegression(C=C, max_iter=max_iter)
        model.fit(x_train, y_train)
        accuracy=model.score(x_test, y_test)
        y_pred=model.predict(x_test)
        st.write("Accuracy: ", accuracy.round(2))
        st.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
        st.write("Precision: ", recall_score(y_test, y_pred, labels=class_names).round(2))
        plot_metrices(metrices)


