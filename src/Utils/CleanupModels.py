from src.Utils.ModelSelector import select_XGB_Model
import os
from tqdm import tqdm

for type in ["ML", "UO"]:
    dir = "../../"
    # fileToNotDelete = select_XGB_Model(type, dir)

    for file in tqdm(os.listdir("{1}Models/XGBoost_Models/{0}".format(type, dir))):
        # if not (type+'/'+file == fileToNotDelete):
        os.remove("{0}Models/XGBoost_Models/{1}/{2}".format(dir, type, file))