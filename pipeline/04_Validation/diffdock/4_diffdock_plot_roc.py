import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import yaml

with open("diffdock_roc.conf.example", "r") as f:
    config = yaml.safe_load(f)

actives_file_path = config["actives_file"]
decoys_file_path = config["decoys_file"]
output_plot = config["output_plot"]
expected_actives = config.get("n_actives")
expected_decoys = config.get("n_decoys")

actives = pd.read_csv(actives_file_path)
decoys = pd.read_csv(decoys_file_path)
decoys0 = pd.read_csv(decoys_file_path)

actives['is_active'] = 1
decoys['is_active'] = 0

if expected_decoys and len(decoys) < expected_decoys:
    additional_decoys = expected_decoys - len(decoys)
    decoys = pd.concat([decoys, pd.DataFrame({'File': ['placeholder']*additional_decoys,
                                              'minimizedAffinity': [100]*additional_decoys,
                                              'is_active': [0]*additional_decoys})],
                        ignore_index=True)

if expected_actives and len(actives) < expected_actives:
    additional_actives = expected_actives - len(actives)
    actives = pd.concat([actives, pd.DataFrame({'File': ['placeholder']*additional_actives,
                                                'minimizedAffinity': [100]*additional_actives,
                                                'is_active': [1]*additional_actives})],
                        ignore_index=True)

data = pd.concat([actives, decoys], ignore_index=True)

y_true = data['is_active']
y_scores = -data['minimizedAffinity']

fpr, tpr, _ = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.suptitle("Receiver Operating Characteristic Curve of DiffDock + GNINA - rms_curr")
plt.title(f"Actives: {len(actives)} of {expected_actives}, Decoys: {len(decoys0)} of {expected_decoys}", fontsize=8)
plt.legend(loc="lower right")
plt.savefig(output_plot, dpi=300)
print(f'ROC curve and AUC saved at {output_plot}')
