from matplotlib import pyplot as plt
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW

class myf():
    def __init__(self) -> None:
        pass

    @staticmethod
    def void(*args):
        return args

    @staticmethod
    def median_function(x,w=None):
        if(len(x)==0):
            return np.nan
        if(len(x)==1):
            return x.iloc[0]
        wdf = DescrStatsW(x, weights=w, ddof=1)
        return wdf.quantile([0.5],return_pandas=False)[0]

    @staticmethod
    def std_function(x,w=None):
        if(len(x)==0):
            return np.nan
        wdf = DescrStatsW(x, weights=w, ddof=1)
        return wdf.std
    
    @staticmethod
    def mean_function(x,w=None):
        if(len(x)==0):
            return np.nan
        wdf = DescrStatsW(x, weights=w, ddof=1)
        return wdf.mean

    @staticmethod
    def window_bin_data_1D(x,z,weights,f,f_x=None,x_step=0.02,x_window_length=0.2,threshold=5):
        '''
        1D窗口平均函数
        '''
        if(f_x==None):
            f_x = myf.mean_function
        x_min = np.min(x)
        x_max = np.max(x)
        x_bin_boundary_min = np.arange(x_min,x_max,x_step)
        x_bin_boundary_max = np.arange(x_min+x_window_length,x_max+x_window_length,x_step)
        N = np.min((len(x_bin_boundary_max),len(x_bin_boundary_min)))
        X = []
        Z = []
        for i in range(N):
            index = (x>=x_bin_boundary_min[i]) & (x<x_bin_boundary_max[i])
            if(np.sum(index)<threshold):
                X.append(np.nan)
                Z.append(np.nan)
                continue
            X.append(f_x(x[index],weights[index]))
            Z.append(f(z[index],weights[index]))
        return X,Z



    @staticmethod
    def window_bin_data_2D(x,y,z,weights,f,f_x=None,f_y=None,x_step=0.02,y_step=0.02,x_window_length=0.2,y_window_length=0.2,threshold=1,xrange=None,yrange=None):
        '''
        2D窗口平均函数
        '''
        if(xrange==None):
            x_min = np.min(x)
            x_max = np.max(x)
        else:
            x_min = xrange[0]
            x_max = xrange[1]
        if(yrange==None):
            y_min = np.min(y)
            y_max = np.max(y)
        else:
            y_min = yrange[0]
            y_max = yrange[1]
        x_bin_boundary_min = np.arange(x_min,x_max,x_step)
        x_bin_boundary_max = np.arange(x_min+x_window_length,x_max+x_window_length,x_step)
        y_bin_boundary_min = np.arange(y_min,y_max,y_step)
        y_bin_boundary_max = np.arange(y_min+y_window_length,y_max+y_window_length,y_step)
        N_X = np.min((len(x_bin_boundary_max),len(x_bin_boundary_min)))
        N_Y = np.min((len(y_bin_boundary_max),len(y_bin_boundary_min)))
        X = []
        Y = []
        Z = []
        if(f_x==None and f_y ==None):
            for i in range(N_X):
                temp_index = (x>=x_bin_boundary_min[i]) & (x<x_bin_boundary_max[i])
                temp_x = (x_bin_boundary_min[i]+x_bin_boundary_max[i])/2
                for j in range(N_Y):
                    index = temp_index & (y>=y_bin_boundary_min[j]) & (y<y_bin_boundary_max[j])
                    X.append(temp_x)
                    Y.append((y_bin_boundary_min[j]+y_bin_boundary_max[j])/2)
                    if(np.sum(index)<threshold):
                        Z.append(np.nan)
                        continue
                    Z.append(f(z[index],weights[index]))
        else:
            for i in range(N_X):
                temp_index = (x>=x_bin_boundary_min[i]) & (x<x_bin_boundary_max[i])
                for j in range(N_Y):
                    index = temp_index & (y>=y_bin_boundary_min[j]) & (y<y_bin_boundary_max[j])
                    if(np.sum(index)<threshold):
                        X.append(f_x(x[index],weights[index]))
                        Y.append(f_y(y[index],weights[index]))
                        Z.append(np.nan)
                        continue
                    X.append(f_x(x[index],weights[index]))
                    Y.append(f_y(y[index],weights[index]))
                    Z.append(f(z[index],weights[index]))
        X = np.array(X)
        Y = np.array(Y)
        Z = np.array(Z)
        X = X.reshape(N_X,N_Y)
        Y = Y.reshape(N_X,N_Y)
        Z = Z.reshape(N_X,N_Y)
        return X,Y,Z

if __name__ == '__main__':
    x = np.arange(200)
    y = np.arange(200)
    z = np.arange(200)
    X,Y,Z = myf.window_bin_data_2D(x,y,z,weights=y,f=myf.mean_function,x_step=10,y_step=10,x_window_length=20,y_window_length=20)
    plt.scatter(X,Y,c=Z)
    plt.show()