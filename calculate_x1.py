import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


File_path1=r'C:\Users\Administrator\Desktop\code\barcode1.xlsx'
File_path2=r'C:\Users\Administrator\Desktop\code\barcode2.xlsx'
data_1=pd.read_excel(File_path1,header=0)
data_2=pd.read_excel(File_path2,header=0)
true_data_1=data_1.values[:,:2]
true_data_2=data_2.values[:,:2]



def calculate_x1(barcod_1,barcode2):
    #barcode_1和barcode_2分别表示10cycle和100 cycle 的V-Q数据；
    #barcode_1的数据格式为2 x n，第一行表示电压V，第二行表示容量Q
    V1=barcod_1[0,:]
    Q1=barcod_1[1,:]
    V2=barcode2[0,:]
    Q2=barcode2[1,:]
    ####################################################
    # Step_1：对数据进行线性插值，获得barcode_1 和 barcode_2 更加精确的表示 
    v_min=max(V1[0],V2[0])
    v_max=min(V1[-1],V2[-1])
    V3=V1*(V1>=v_min)*(V1<=v_max)
    V4=V2*(V2>=v_min)*(V2<=v_max)
    V=np.concatenate((V3,V4),axis=0)
    V=np.unique(V)[1:] # 第一个值为0 舍弃
    matrix_1=np.matmul(Q1,get_matrix(V1,V))#线性插值
    matrix_2=np.matmul(Q2,get_matrix(V2,V))#线性插值
    #plt.plot(Q1,V1,matrix_1,V)
    #plt.show()
    ###################################################
    # Step_2：计算特征值（方差、差的绝对积分、差的最大值、差的平方积分）
    delta=np.fabs(matrix_1-matrix_2) #差
    variance=np.var(delta) #方差
    mean=np.mean(delta)#平均值
    hat_v1=np.concatenate((V[1:],[V[-1]]),axis=0)
    hat_v2=np.concatenate(([V[0]],V[0:-1]),axis=0)
    hat_v=hat_v1-hat_v2
    integral=sum(delta*hat_v)/2#积分
    delta_2=delta*delta
    integral_2=sum(delta_2*hat_v)/2#平方积分
    print(integral,integral_2,variance,mean)
    return variance
    ################## numpy还内置了其他统计量的计算，可以参考：
    #https://www.runoob.com/numpy/numpy-statistical-functions.html








    
def get_matrix(V1,V):
    #获取插值矩阵
    matrix_1=np.zeros((V1.size,V.size))
    list=np.arange(0,V1.size,1)
    for i in list:
        if i==0:
            matrix_1[i,:]= get_row(V1[i],V1[i],V1[i+1],V)
        elif i==list[-1]:
            matrix_1[i,:]= get_row(V1[i-1],V1[i],V1[i],V)
        else:
            matrix_1[i,:]= get_row(V1[i-1],V1[i],V1[i+1],V)
    return matrix_1


def  get_row(x1,x2,x3,list):
    #获取插值函数
    result=np.zeros(list.size)
    k=0
    if x1==x2:
        #print(1)
        for i in list:    
            y=(i>=x2)*(i-x3)-(i>=x3)*(i-x3)
            result[k]=y/(x2-x3)
            k=k+1
    elif x2==x3:
        #print(2)
        for i in list:
            y=(i<=x3)*(i-x1)-(i<=x1)*(i-x1)
            result[k]=y/(x2-x1)
            k=k+1
    else :
        for i in list:
            y=(i>x1)*(i-x1)*(x2-x3)+(i>=x2)*((x3-x1)*i+(x1*x2-x3*x2))-(i>=x3)*(i-x3)*(x2-x1)
            result[k]=y/((x2-x1)*(x2-x3))
            k=k+1
    return result


calculate_x1(true_data_1.T,true_data_2.T)
#list=np.arange(0,1,0.01)
#re=get_row(0.3,0.4,0.4,list)
#plt.plot(list,re,'o')
#plt.show()
