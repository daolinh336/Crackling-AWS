import joblib
import numpy as np

model_file = '../layers/sgrnascorer2model/model-py38-svc0232.txt'
npz_filename = '../layers/sgrnascorer2model/sgrnascorer2_svm_numpy_data.npz'
svm = joblib.load(model_file)

# Extract support vectors and coefficients
support_vectors = svm.support_vectors_
dual_coef = svm.dual_coef_[0]
intercept = svm.intercept_[0]
classes = svm.classes_

np.savez(npz_filename,
         support_vectors=support_vectors,
         dual_coef=dual_coef,
         intercept=intercept,
         classes=classes)

def decision_function(x, support_vectors, dual_coef, intercept):
    return np.sum(dual_coef * np.dot(support_vectors, x)) + intercept

def predict(x, support_vectors, dual_coef, intercept, classes):
    score = decision_function(x, support_vectors, dual_coef, intercept)
    return classes[1] if score > 0 else classes[0], score

def seq_to_sgrnascorer_vector(seq):
    encoding = {
        'A' : '0001',        'C' : '0010',        'T' : '0100',        
        'G' : '1000',        'K' : '1100',        'M' : '0011',
        'R' : '1001',        'Y' : '0110',        'S' : '1010',        
        'W' : '0101',        'B' : '1110',        'V' : '1011',        
        'H' : '0111',        'D' : '1101',        'N' : '1111'
    }

    entryList = []

    x = 0
    while x < 20:
        y = 0
        while y < 4:
            entryList.append(int(encoding[seq[x]][y]))
            y += 1
        x += 1

    return entryList


sample_sequences = [
    seq_to_sgrnascorer_vector("ATCG"*5),
    seq_to_sgrnascorer_vector("CAGTCGATCGATTGTCACGT"),
    seq_to_sgrnascorer_vector("CTACGATCGACTACGCTAGC"),
    seq_to_sgrnascorer_vector("GGCTATCGCGCTAGCTCATA")
]

# Load offline arrays
data = np.load(npz_filename)
sv = data['support_vectors']
dc = data['dual_coef']
ic = data['intercept'].item()   # scalar
cl = data['classes']

print("\nComparing original SVC vs NumPy-only predictions:")

for i, x in enumerate(sample_sequences):
    # Original SVC prediction
    orig_pred = svm.predict([x])[0]
    orig_score = svm.decision_function([x])[0]

    # NumPy-only prediction
    np_pred, np_score = predict(x, sv, dc, ic, cl)

    print(f"Sample {i+1}:")
    print(f"  Original SVC -> pred: {orig_pred}, score: {orig_score:.4f}")
    print(f"  NumPy-only   -> pred: {np_pred}, score: {np_score:.4f}")
    print(f"  Match? {'Yes' if (orig_pred==np_pred and np.isclose(orig_score, np_score)) else 'No'}\n")
