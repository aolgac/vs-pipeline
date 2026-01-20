import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import yaml

with open("flexx_roc.conf.example", "r") as f:
    config = yaml.safe_load(f)

actives_file_path = config["actives_csv"]
decoys_file_path = config["decoys_csv"]
save_path = config["output_png"]
n_actives = config.get("n_actives", None)
n_decoys = config.get("n_decoys", None)

actives = pd.read_csv(actives_file_path)
decoys = pd.read_csv(decoys_file_path)
decoys0 = pd.read_csv(decoys_file_path)

actives['is_active'] = 1
decoys['is_active'] = 0

if n_decoys is not None and len(decoys) < n_decoys:
    additional_decoys = n_decoys - len(decoys)
    decoys = pd.concat([decoys, pd.DataFrame({'File Name': ['placeholder_decoy']*additional_decoys,
                                              'Results': [0]*additional_decoys,
                                              'is_active': [0]*additional_decoys})], ignore_index=True)

if n_actives is not None and len(actives) < n_actives:
    additional_actives = n_actives - len(actives)
    actives = pd.concat([actives, pd.DataFrame({'File Name': ['placeholder_active']*additional_actives,
                                                'Results': [0]*additional_actives,
                                                'is_active': [1]*additional_actives})], ignore_index=True)

data = pd.concat([actives, decoys], ignore_index=True)

y_true = data['is_active']
y_scores = -data['Results']

fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.suptitle('Receiver Operating Characteristic Curve of FlexX')
plt.title(f'Actives: {len(actives)} of {n_actives}, Decoys: {len(decoys0)} of {n_decoys}', fontsize=8)
plt.legend(loc="lower right")
plt.savefig(save_path, dpi=300)

print(f'ROC curve and AUC figure saved at {save_path}')
