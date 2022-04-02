# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:39:15 2021

@author: Xie
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.contrib.distributions import MultivariateNormalFullCovariance
from tensorflow.python.ops.parallel_for.gradients import jacobian
from collections import Iterable
import xlrd

from tensorflow.contrib.distributions import MultivariateNormalDiag

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x
def GetDataFromXls():
    #xl = xlrd.open_workbook('D:\Doc\SofrWare\matlab_python\data.xls')
    xl = xlrd.open_workbook('data.xls')
    table = xl.sheets()[0]
    row = table.row_values(0)
    X = row[0]
    Y = row[1]
    return X,Y


DNA_SIZE = 2         # parameter (solution) number
N_POP = 6          # population size
N_GENERATION = 6   # training step
LR = 0.02            # learning rate

# MuX=0.75
# MuY=0.75


# fitness function
def get_fitness(pred):
    fitness=-(5*(pred[:, 0])**2 +5*( pred[:, 1])**2)
    print (pred)
    print (fitness)
    # xl=xlrd.open_workbook('D:\Doc\SofrWare\matlab_python\data.xlsx')
    # table=xl.sheets()[0]
    # row=table.row_values(0)
    return fitness


# build multivariate distribution

#Read data from xls
(MuX,MuY)=GetDataFromXls()
#notes

mean = tf.Variable([MuX,MuY], dtype=tf.float32)
cov = tf.Variable(1. * tf.eye(DNA_SIZE), dtype=tf.float32)
mvn = MultivariateNormalFullCovariance(loc=mean, covariance_matrix=cov)
make_kid = mvn.sample(N_POP)                                    # sampling operation

# compute gradient and update mean and covariance matrix from sample and fitness
tfkids_fit = tf.placeholder(tf.float32, [N_POP, ])
tfkids = tf.placeholder(tf.float32, [N_POP, DNA_SIZE])

mean_new=tf.placeholder(tf.float32, [2,])
cov_new=tf.placeholder(tf.float32, [2,2])

#mean_=tf.Variable(tf.random_normal([2, ], 13., 1.), dtype=tf.float32)
#mean_=tf.assign(mean_,mean)
#cov_=cov
mean_update=tf.assign(mean,mean_new)
cov_update=tf.assign(cov,cov_new)

#loss = -tf.reduce_mean(mvn.log_prob(tfkids)*tfkids_fit)         # log prob * fitness
#train_op = tf.train.GradientDescentOptimizer(LR).minimize(loss) # compute and apply gradients for mean and cov
#para=tf.train.GradientDescentOptimizer(LR).compute_gradients(loss,[mean,cov])
#d_ux=[[para[0][0][0]],[para[0][0][0]]]

#grad=tf.train.GradientDescentOptimizer(1).compute_gradients(mvn.log_prob(tfkids),[mean,cov])
mvn_logPro=mvn.log_prob(tfkids)
fit_mvnLogPro=mvn.log_prob(tfkids)*tfkids_fit

J_fitMvnLogPro=jacobian(fit_mvnLogPro,[mean,cov])
J_mvnLogPro=jacobian(mvn_logPro,[mean,cov])



#train_op=tf.train.GradientDescentOptimizer(LR).apply_gradients(para)

sess = tf.Session()
sess.run(tf.global_variables_initializer())                     # initialize tf variables

'''
# something about plotting (can be ignored)
n = 300
x = np.linspace(-20, 20, n)
X, Y = np.meshgrid(x, x)
Z = np.zeros_like(X)
for i in range(n):
    for j in range(n):
        Z[i, j] = get_fitness(np.array([[x[i], x[j]]]))
plt.contourf(X, Y, -Z, 100, cmap=plt.cm.rainbow)
plt.ylim(-20, 20)
plt.xlim(-20, 20)
plt.ion()
'''

# training
for g in range(N_GENERATION):
    kids = sess.run(make_kid)
    #print(kids)
    kids_fit = get_fitness(kids)
    #print(sess.run(d_ux,{tfkids_fit: kids_fit, tfkids: kids}))

    #sess.run(train_op, {tfkids_fit: kids_fit, tfkids: kids})    # update distribution parameters

    #print(sess.run(para[1][1][0][0], {tfkids_fit: kids_fit, tfkids: kids}))
    #print(sess.run(para[1][1][0], {tfkids_fit: kids_fit, tfkids: kids}))
    #print(sess.run(J[0], {tfkids_fit: kids_fit, tfkids: kids}))
    #print(sess.run(mvn_pro, {tfkids_fit: kids_fit, tfkids: kids}))
    #xo=np.array(sess.run(d_ux, {tfkids_fit: kids_fit, tfkids: kids}))
    #print(type(xo))
    #print(sess.run(grad, {tfkids_fit: kids_fit, tfkids: kids}))

    J_M=sess.run(J_fitMvnLogPro, {tfkids_fit: kids_fit, tfkids: kids})


    F_M=sess.run(J_mvnLogPro, {tfkids_fit: kids_fit, tfkids: kids})

    #print(J)
    #print(F)


    J_flat=list(flatten(J_M))
    F_flat=list(flatten(F_M))

    #print(J_flat)
    J=np.array([0,0,0,0,0])
    for i in range(N_POP):
        J_mat=np.array([J_flat[i*2+0],J_flat[i*2+1],J_flat[i*4+2*N_POP],J_flat[i*4+2*N_POP+1],J_flat[i*4+2*N_POP+3]])
        J=J[0]+J_mat[0],J[1]+J_mat[1],J[2]+J_mat[2],J[3]+J_mat[3],J[4]+J_mat[4]
        #print(J_mat)
        #print("a")
    J_gra=np.reshape(np.array(J)/N_POP,(5,1))

    F=np.zeros([5,5])
    for i in range(N_POP):
        F_mat=np.array([F_flat[i*2+0],F_flat[i*2+1],F_flat[i*4+2*N_POP],F_flat[i*4+2*N_POP+1],F_flat[i*4+2*N_POP+3]])
        F_xita=np.matmul(np.array([F_mat]).T,np.array([F_mat]))
        #print(F_xita)
        #print("b")
        for j in range(5):
            for k in range(5):
                F[j][k]=F[j][k]+F_xita[j][k]
        #print(F)
        #print('c')
    if np.linalg.matrix_rank(F)<5:
        F_gra=np.eye(5)
    else:
        F_gra=np.linalg.inv(np.array(F)/20)
        #F_gra=np.eye(5)
    #print(F_gra)
    #print('A')
    xita_=np.matmul(F_gra,J_gra)
    xita=np.zeros(6)

    for l in range(6):
        if l <4:
            xita[l]=xita_[l]
        else:
            if l<5:
                xita[l]=xita_[3]
            else:
                xita[l]=xita_[4]


    mean_o=np.array(sess.run(mean))
    cov_o=np.array(sess.run(cov))
    #print(sess.run(mean))
    mean_value=(np.array(sess.run(mean))+(0.008*xita[0:2]).flatten())
    cov_value=(np.array(sess.run(cov))+(0.001*xita[2:6]).reshape(2,2))
    #print(sess.run(mean))
    #print(sess.run(cov))
    #print("B")
    #mean_value=np.array(sess.run(mean_,{tfkids_fit: kids_fit, tfkids: kids}))+J_gra[0:2]*0.2
    #cov_value=np.array(sess.run(cov_,{tfkids_fit: kids_fit, tfkids: kids}))+J_gra[2:6]*0.2
    #print(mean_value)
    sess.run(mean_update,{mean_new:mean_value})
    sess.run(cov_update,{cov_new:cov_value})
    print(sess.run(mean))
    #print(sess.run(cov))
    #print(" C ")
    print("Parameters are successfully updated!")

    try:
        sess.run(make_kid)
    except:
        print("Parameters are wrongly updated!")
        sess.run(mean_update,{mean_new:mean_o})
        sess.run(cov_update,{cov_new:cov_o})
    #print(matrix_arr)

    #print(sess.run(para, {tfkids_fit: kids_fit, tfkids: kids}))

    #print(sess.run(d, {tfkids_fit: kids_fit, tfkids: kids}))
    #print(sess.run(F,{tfkids:kids}))
    #print(len(para))
'''
    # plotting update

    if 'sca' in globals(): sca.remove()
    sca = plt.scatter(kids[:, 0], kids[:, 1], s=30, c='k');plt.pause(0.01)
    if 'sca' in globals(): sca.remove()
    sca = plt.scatter(kids[:, 0], kids[:, 1], s=30, c='k');plt.pause(0.01)

print('Finished'); plt.ioff(); plt.show()
'''
