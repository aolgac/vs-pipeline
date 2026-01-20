import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import yaml

with open("glide_roc.conf.example", "r") as f:
    config = yaml.safe_load(f)

actives_file_path = config["actives_file"]
decoys_file_path = config["decoys_file"]
output_figure = config["output_figure"]
expected_actives = config.get("expected_actives", 50)
expected_decoys = config.get("expected_decoys", 500)

actives = pd.read_csv(actives_file_path)
decoys = pd.read_csv(decoys_file_path)
decoys0 = pd.read_csv(decoys_file_path)

required_columns = {"File Name", "GlideScore"}
if not required_columns.issubset(actives.columns) or not required_columns.issubset(decoys.columns):
    raise ValueError(f"Input files must contain columns: {required_columns}")

actives["is_active"] = 1
decoys["is_active"] = 0

if len(decoys) < expected_decoys:
    additional_decoys = expected_decoys - len(decoys)
    placeholder_decoys = pd.DataFrame({
        "File Name": ["placeholder_decoy"] * additional_decoys,
        "GlideScore": [0.0] * additional_decoys,
        "is_active": [0] * additional_decoys
    })
    decoys = pd.concat([decoys, placeholder_decoys], ignore_index=True)

if len(actives) < expected_actives:
    additional_actives = expected_actives - len(actives)
    placeholder_actives = pd.DataFrame({
        "File Name": ["placeholder_active"] * additional_actives,
        "GlideScore": [0.0] * additional_actives,
        "is_active": [1] * additional_actives
    })
    actives = pd.concat([actives, placeholder_actives], ignore_index=True)

data = pd.concat([actives, decoys], ignore_index=True)

y_true = data["is_active"]
y_scores = -data["GlideScore"]

if y_scores.isna().any():
    raise ValueError("GlideScore contains NaN values. Please check the input files.")

fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.suptitle("Receiver Operating Characteristic Curve of Glide SP - rms_cur")
plt.title(f"Actives: {len(actives)} of {expected_actives}, Decoys: {len(decoys0)} of {expected_decoys}", fontsize=8)
plt.legend(loc="lower right")
plt.savefig(output_figure, dpi=300)

print(f"ROC curve and AUC figure saved at {output_figure}")
print(f"AUC: {roc_auc:.2f}")
