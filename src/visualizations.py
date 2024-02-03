from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import learning_curve
from matplotlib.ticker import FormatStrFormatter
from matplotlib import pyplot as plt
from pandas import DataFrame
import IPython.display as ipd
import numpy as np


def classification_data(classifier, x_train, y_train, x_test, y_test, splits = 5):

    train_accuracy, test_accuracy, train_precisions, test_precisions, train_recall, test_recall, train_f1, test_f1 = [], [], [], [], [], [], [], []

    # Διαίρεση των δεδομένων εκπαίδευσης σε n υποσύνολα
    split_size = int(len(x_train) / splits)
    x_splits = np.split(x_train, splits)
    y_splits = np.split(y_train, splits)

    # Εκπαίδευση του μοντέλου σε κάθε υποσύνολο και αξιολόγηση στο σύνολο δεδομένων ελέγχου
    for i in range(len(x_splits)):
        if i == 0:
            x_train = x_splits[0]
            y_train = y_splits[0]
        else:
            x_train = np.concatenate((x_train, x_splits[i]), axis=0) # το υποσυνολο αυξανεται, συνενωνοντας τα προηγουμενα δεδομενα με τα επομενα
            y_train = np.concatenate((y_train, y_splits[i]), axis=0)
        
        # Εκπαίδευση του μοντέλου και λήψη προβλέψεων εκπαίδευσης/ελέγχου
        classifier.fit(x_train, y_train)
        train_pred = classifier.predict(x_train)
        test_pred = classifier.predict(x_test)
        
        # Calculate and save the accuracy score
        train_accuracy.append(accuracy_score(y_train, train_pred))
        test_accuracy.append(accuracy_score(y_test, test_pred))
        
        # Calculate and save the precision score
        train_precisions.append(precision_score(y_train, train_pred))
        test_precisions.append(precision_score(y_test, test_pred))
        
        # Calculate and save the recall score
        train_recall.append(recall_score(y_train, train_pred))
        test_recall.append(recall_score(y_test, test_pred))
        
        # Calculate and save the f1 score
        train_f1.append(f1_score(y_train, train_pred))
        test_f1.append(f1_score(y_test, test_pred))

    # Calculate the final confusion matrix
    cm = confusion_matrix(y_test, test_pred) #τετραγωνικός πίνακας που δείχνει τον αριθμό των πραγματικών και προβλεπόμενων κλάσεων για ένα πρόβλημα δυαδικής ταξινόμησης.

    data = {'estimator': classifier.__class__.__name__, 
            'split_size': split_size, 
            'splits': splits,
            'test_predictions': test_pred,
            'train_accuracy': train_accuracy, 
            'test_accuracy': test_accuracy, 
            'train_precision': train_precisions, 
            'test_precision': test_precisions, 
            'train_recall': train_recall, 
            'test_recall': test_recall, 
            'train_f1': train_f1, 
            'test_f1': test_f1,
            'final_cm': cm}

    return data

  
def classification_table(classification_data, x_train):

    split_size = classification_data['split_size']
    df = DataFrame(data={'Train Accuracy': np.round(classification_data['train_accuracy'], 2), 
                          'Test Accuracy': np.round(classification_data['test_accuracy'], 2), 
                          'Precision Train' : np.round(classification_data['train_precision'], 2), 
                          'Precision Test' : np.round(classification_data['test_precision'], 2), 
                          'Recall Train' : np.round(classification_data['train_recall'], 2), 
                          'Recall Test' : np.round(classification_data['test_recall'], 2), 
                          'F1 Train' : np.round(classification_data['train_f1'], 2), 
                          'F1 Test' : np.round(classification_data['test_f1'], 2)}, 
                    index=list(range(split_size, len(x_train) + split_size, split_size)))
    return df

def plot_learning_curve(data, title="Learning Curve", full_scale=False):

    split_size = data['split_size']
    split = data['splits']
    splits = list(range(split_size, split*split_size + split_size, split_size))
    train_acc = data['train_accuracy']
    test_acc = data['test_accuracy']

    train_scores_std = np.std(train_acc)
    val_scores_std = np.std(test_acc)

    if full_scale:
        plt.ylim(0, 1)
    plt.title(title)
    plt.xlabel("Training Examples")
    plt.ylabel("Accuracy")
    plt.plot()

    plt.fill_between(splits, train_acc - train_scores_std,
                    train_acc + train_scores_std, alpha=0.1,
                    color="b")
    plt.fill_between(splits, test_acc - val_scores_std,
                    test_acc + val_scores_std, alpha=0.1,
                    color="green")
    plt.plot(splits, train_acc, 'o-', color="b",
            label="Training score")
    plt.plot(splits, test_acc, 'o-', color="green",
            label="Validation score")

    plt.legend(loc="best")
    plt.show()


def classification_plots(data, full_scale=False):

    split_size = data['split_size']
    splits = data['splits']
    
    x_splits = list(range(split_size, splits*split_size + split_size, split_size))
    
    figure, axis = plt.subplots(2, 2, figsize=(6, 6), dpi=100, gridspec_kw={'width_ratios': [1, 1], 'height_ratios': [1, 1]})
    figure.suptitle("Learning Curve for {estimator}".format(estimator = data['estimator']), fontsize=16)
    labels = ['Accuracy', 'Precision', 'Recall', 'F1']

    axis[0,0].plot(x_splits, data['train_accuracy'], 'o-', color="b",  label='Training Accuracy')
    axis[0,0].plot(x_splits, data['test_accuracy'], 'o-', color="red",label='Test Accuracy')
    axis[0,0].legend(loc="lower right")

    axis[0,1].plot(x_splits, data['train_precision'], 'o-', color="b",  label='Training Precision')
    axis[0,1].plot(x_splits, data['test_precision'], 'o-', color="red",label='Test Precision')
    axis[0,1].legend(loc="lower right")

    axis[1,0].plot(x_splits, data['train_recall'], 'o-', color="b",  label='Training Recall')
    axis[1,0].plotx_split(x_splits, data['test_recall'], 'o-', color="red",label='Test Recall')
    axis[1,0].legend(loc="lower right")

    axis[1,1].plot(x_splits, data['train_f1'], 'o-', color="b",  label='Training f1')
    axis[1,1].plot(x_splits, data['test_f1'], 'o-', color="red",label='Test f1')
    axis[1,1].legend(loc="lower right")
    
    if full_scale:
        for i , j in zip([0,1], [0,1]):
            axis[i,j].axis(ymin= 0.0, ymax= 1.0)

    # handles, labels = axis[1, 1].get_legend_handles_labels()
    # figure.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2, fancybox=True, shadow=True)
    figure.tight_layout()

    return figure