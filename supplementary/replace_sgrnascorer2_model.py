import joblib
import json

# --- Train/extract model ---
model_file = '../layers/sgrnascorer2model/model-py38-svc0232.txt'
json_filename = '../layers/sgrnascorer2model/sgrnascorer2_svm_data.json'
svm = joblib.load(model_file)

# Extract support vectors and coefficients, convert to pure Python lists
model_data = {
    "support_vectors": svm.support_vectors_.tolist(),
    "dual_coef": svm.dual_coef_[0].tolist(),
    "intercept": float(svm.intercept_[0]),
    "classes": svm.classes_.tolist()
}

# Save arrays as JSON for offline use (NumPy-free)
with open(json_filename, "w") as f:
    json.dump(model_data, f)


# --- NumPy-free inference code ---

def dot(u, v):
    """Dot product of two vectors."""
    return sum(ue * ve for ue, ve in zip(u, v))

def decision_function(x, support_vectors, dual_coef, intercept):
    """Manual SVM decision function without NumPy."""
    total = 0.0
    for coef, sv in zip(dual_coef, support_vectors):
        total += coef * dot(sv, x)
    return total + intercept

def predict(x, support_vectors, dual_coef, intercept, classes):
    score = decision_function(x, support_vectors, dual_coef, intercept)
    return (classes[1] if score > 0 else classes[0], score)

def seq_to_sgrnascorer_vector(seq):
    """Encode a DNA sequence into the sgRNAScorer 2.0 binary feature vector."""
    encoding = {
        'A' : '0001', 'C' : '0010', 'T' : '0100', 'G' : '1000',
        'K' : '1100', 'M' : '0011', 'R' : '1001', 'Y' : '0110',
        'S' : '1010', 'W' : '0101', 'B' : '1110', 'V' : '1011',
        'H' : '0111', 'D' : '1101', 'N' : '1111'
    }

    entryList = []
    for base in seq[:20]:  # only first 20 bases
        entryList.extend(int(bit) for bit in encoding[base])
    return entryList


# --- Test against original SVC ---

sample_sequences = [
    seq_to_sgrnascorer_vector("ATCG"*5),
    seq_to_sgrnascorer_vector("CAGTCGATCGATTGTCACGT"),
    seq_to_sgrnascorer_vector("CTACGATCGACTACGCTAGC"),
    seq_to_sgrnascorer_vector("GGCTATCGCGCTAGCTCATA")
]

# Load offline arrays (from JSON)
with open(json_filename, "r") as f:
    data = json.load(f)

sv = data['support_vectors']
dc = data['dual_coef']
ic = data['intercept']
cl = data['classes']

print("\nComparing original SVC vs pure-Python predictions:")

for i, x in enumerate(sample_sequences):
    # Original SVC prediction
    orig_pred = svm.predict([x])[0]
    orig_score = svm.decision_function([x])[0]

    # Pure Python prediction
    py_pred, py_score = predict(x, sv, dc, ic, cl)

    print(f"Sample {i+1}:")
    print(f"  Original SVC -> pred: {orig_pred}, score: {orig_score:.4f}")
    print(f"  Pure Python  -> pred: {py_pred}, score: {py_score:.4f}")
    print(f"  Match? {'Yes' if (orig_pred==py_pred and abs(orig_score - py_score) < 1e-6) else 'No'}\n")
