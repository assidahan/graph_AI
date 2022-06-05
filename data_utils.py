import pandas as pd


def norm_vec(x,new_max=None,new_min=None):
    normalized = (x - x.min()) / (x.max() - x.min())
    if new_max:
        normalized = normalized * (new_max-new_min) + new_min

    return normalized


def save_fea_importance(self,clf,title='saved_to_use',take_max=33):
    dict_feature_importance = {}
    fea = []
    for i in range(len(clf.feature_importances_)):
        fea.append(round(clf.feature_importances_[i],3))
        dict_feature_importance[self.features_columns[i]] = fea[-1]

    fea = np.array(fea)
    ind = np.argsort(-fea)
    fea = fea[ind]
    col = np.array(self.features_columns)
    col = col[ind]
    if Conf.local_mode:
        plt.figure()
        plt.subplot(4,1,(1,2))
        plt.plot(col[0:take_max],fea[0:take_max],'-*')
        plt.title('explained features')
        plt.grid()
        plt.xticks(rotation=60)
        # plt.show(block=False)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        plt.savefig(Conf.plots_folder + f'explained features-{title}.png')
    plt.close('all')

    return col






def hill_function(x,x_k_noraml,power=2,decay=False,amplitude = 1,th_max=None):
    if pd.isnull(x):
        val = None
    else:
        if decay:
            val = (x_k_noraml**power)/(x**power+x_k_noraml**power)
        else:
            val = (x**power)/(x**power+x_k_noraml**power)
        val = amplitude * val
        if th_max:
            val = min(th_max,val)
    return val

