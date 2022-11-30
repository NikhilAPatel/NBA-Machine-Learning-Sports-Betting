import os

def select_XGB_Model(type):
    accs = [file[file.index('_')+1:file.index('%')] for file in os.listdir("Models/XGBoost_Models/{0}".format(type))]
    accs = sorted(accs)

    return '{1}/XGBoost_{0}%_{1}-{2}.json'.format(accs[~0], type, 2 if type=="ML" else 6)

# print(select_XGB_Model("ML"))
# print(select_XGB_Model("UO"))