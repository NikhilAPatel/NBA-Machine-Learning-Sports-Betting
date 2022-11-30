from src.Utils.ModelSelector import select_XGB_Model
import os
from tqdm import tqdm


def delete_all():
    for type1 in ["ML", "UO"]:

        for file in tqdm(os.listdir("{1}Models/XGBoost_Models/{0}".format(type1, dir1))):
            os.remove("{0}Models/XGBoost_Models/{1}/{2}".format(dir1, type1, file))


def delete_all_but_best():
    for type1 in ["ML", "UO"]:
        fileToNotDelete = select_XGB_Model(type1)

        for file1 in tqdm(os.listdir("Models/XGBoost_Models/{0}".format(type1))):
            if not (type1 + '/' + file1 == fileToNotDelete):
                os.remove("Models/XGBoost_Models/{0}/{1}".format(type1, file1))
