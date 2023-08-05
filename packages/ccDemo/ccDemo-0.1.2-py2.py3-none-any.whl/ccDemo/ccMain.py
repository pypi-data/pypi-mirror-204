if __package__ is None or __package__=='':
    import convexclustering as cc
else:
    from . import convexclustering as cc

import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
import random
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_moons
from sklearn.datasets import make_blobs
from sklearn.datasets import load_iris
from sklearn.datasets import load_wine
from sklearn.datasets import load_diabetes

def blobdata():
    # generage synthetic data
    n = 4
    np.random.seed(1)
    U1 = np.random.rand(n, 2)
    U2 = np.random.rand(n + 2, 2) + [2.5, 1]
    U3 = np.random.rand(n + 4, 2) + [1.7, 3]
    U12 = np.concatenate((U1, U2), axis=0)
    U = np.concatenate((U12, U3), axis=0)
    return U


def Gausdata():
    n = 5
    np.random.seed(1)
    dist = 4
    U1 = np.random.multivariate_normal([0, 0], [[1, 0], [0, 0.5]], 10 * n)
    U2 = np.random.multivariate_normal([dist, 0], [[0.04, 0], [0, 0.04]], 1 * n)
    # U3 = np.random.multivariate_normal([0,dist], [[1, 0], [0, 1]], 1*n)
    U12 = np.concatenate((U1, U2), axis=0)

    # U = np.concatenate((U12,U3), axis=0)
    return U12


randata = lambda: np.random.rand(20, 2)


def syndata():
    U = np.array([[0, 0], [0, -1], [0, 3], [0, 4], [1, 4], [5, 3], [5, 4], [4, 3], [4, 4]])
    return U


def suppDemo():
    print('Old supplementary demo')
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex='all', sharey='all')
    axs = (ax1, ax2, ax3)
    np.random.seed(0)
    # U = np.random.uniform(size=(50,2))
    # lambdas = [0.01291,0.012912,0.012912]
    U = np.random.uniform(size=(20, 2))
    lambdas = [0.031, 0.03, 0.0287]

    (n, d) = U.shape
    for i in range(3):
        lamda = lambdas[i]
        X = cc.ccADMM(U, lamda)
        # collect clusters
        indices = cc.collectCluster(U, X, n)
        axs[i].scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=5)
        # draw colors of points #######################################################################
        _, noC = indices.shape
        aa = [*range(1, noC + 1, 1)]
        pcolor = np.dot(indices, aa)
        axs[i].scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.1)
        axs[i].scatter(U[:, 0], U[:, 1], color='black', zorder=3, s=5)
        axs[i].set_aspect('equal')
        axs[i].set_title(r'$\lambda$=' + str(lambdas[i]))
        cc.ccVizclust(U, indices, lamda, axs[i])
    fig.savefig("suppDemo.pdf", bbox_inches='tight')


def moonDemo(lamda, ax1, ax2, ax3):  # lamda = 0.0172
    #    fig, (ax1, ax2, ax3) = plt.subplots(1,3, sharex='all', sharey = 'all')
    (U, y) = make_moons(n_samples=100, noise=0.15, random_state=1)
    (n, d) = U.shape

    X = cc.ccADMM(U, lamda)

    # collect clusters
    indices = cc.collectCluster(U, X, n)
    ax1.scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=0.1)
    # draw colors of points #######################################################################
    _, noC = indices.shape
    aa = [*range(1, noC + 1, 1)]
    pcolor = np.dot(indices, aa)
    ax1.scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.1)
    ax1.set_aspect('equal')
    ax1.set_title('Convex clustering')
    cc.ccVizclust(U, indices, lamda, ax1)

    # k-means clustering
    km = KMeans(n_clusters=2)
    km.fit(U)
    kmy = km.predict(U)
    ax2.set_aspect('equal')
    ax2.scatter(U[:, 0], U[:, 1], c=kmy, s=0.1)
    ax2.set_title('K-means')

    ac = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='single')
    acy = ac.fit_predict(U)
    ax3.set_aspect('equal')
    ax3.scatter(U[:, 0], U[:, 1], c=acy, s=0.1)
    ax3.set_title('Agglomerative')

    #    plt.show()
    #    fig.savefig("twomoons.pdf", bbox_inches='tight')

    print('Done.')


def uniformDemo(lamda, ax1, ax2, ax3):  # lamda = 0.0172
    np.random.seed(1)
    U = np.random.uniform(size=(50, 2))
    (n, d) = U.shape

    X = cc.ccADMM(U, lamda)

    # collect clusters
    indices = cc.collectCluster(U, X, n)
    ax1.scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=0.1)
    # draw colors of points #######################################################################
    _, noC = indices.shape
    aa = [*range(1, noC + 1, 1)]
    pcolor = np.dot(indices, aa)
    ax1.scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.1)
    ax1.set_aspect('equal')
    cc.ccVizclust(U, indices, lamda, ax1)

    # k-means clustering
    km = KMeans(n_clusters=2)
    km.fit(U)
    kmy = km.predict(U)
    ax2.set_aspect('equal')
    ax2.scatter(U[:, 0], U[:, 1], c=kmy, s=0.1)

    ac = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='single')
    acy = ac.fit_predict(U)
    ax3.set_aspect('equal')
    ax3.scatter(U[:, 0], U[:, 1], c=acy, s=0.1)

    #    plt.show()
    #    fig.savefig("twomoons.pdf", bbox_inches='tight')

    print('Done.')


def noisyblobsDemo(lamda, ax1, ax2, ax3):
    #    fig, (ax1, ax2, ax3) = plt.subplots(1,3, sharex='all', sharey = 'all')

    # ax1.plot(x, y)
    # ax2.plot(x, -y)

    # U = blobdata() #n=4, lamda = 0.145
    # U = syndata()  #   lamda = 0.5
    # U = randata() #0.033
    # U = Gausdata()  # 0.0695

    # (U,y) = make_moons(n_samples=20,noise=0.1,random_state=1) #lamda = 0.085 2 clusters
    # next 3 lines: noisy 3 blobs lambda = 0.15
    # (U1,y) = make_blobs(n_samples=50,n_features=2,centers=3,random_state=1)
    # U2 = np.random.uniform(low=-10, high=10, size=(15,2))
    # U = np.concatenate((U1,U2))

    # 200 nodes demo
    (U1, y) = make_blobs(n_samples=180, n_features=2, centers=3, random_state=1)
    # adding noises
    U2 = np.random.uniform(low=-10, high=5, size=(20, 2))
    U = np.concatenate((U1, U2))
    # lamda = 0.042

    # 100 nodes demo
    # (U,y) = make_blobs(n_samples=100,n_features=2,centers=3,random_state=1)
    # lamda = 0.0425

    (n, d) = U.shape

    X = cc.ccADMM(U, lamda)

    # collect clusters
    indices = cc.collectCluster(U, X, n)
    ax1.scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=0.1)
    # draw colors of points #######################################################################
    _, noC = indices.shape
    aa = [*range(1, noC + 1, 1)]
    pcolor = np.dot(indices, aa)
    ax1.scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.1)
    ax1.set_aspect('equal')
    # ax1.set_title('Convex clustering')
    cc.ccVizclust(U, indices, lamda, ax1)

    # k-means clustering
    km = KMeans(n_clusters=3)
    km.fit(U)
    kmy = km.predict(U)
    ax2.set_aspect('equal')
    ax2.scatter(U[:, 0], U[:, 1], c=kmy, s=0.1)
    # ax2.set_title('K-means')

    ac = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='single')
    acy = ac.fit_predict(U)
    ax3.set_aspect('equal')
    ax3.scatter(U[:, 0], U[:, 1], c=acy, s=0.1)
    # ax3.set_title('Agglomerative')

    #    plt.show()
    #    fig.savefig("noisyblobs.pdf", bbox_inches='tight')

    print('Done.')


def threeblobsDemo(lamda, ax1, ax2, ax3):
    #    fig, (ax1, ax2, ax3) = plt.subplots(1,3, sharex='all', sharey = 'all')

    # ax1.plot(x, y)
    # ax2.plot(x, -y)

    # U = blobdata() #n=4, lamda = 0.145
    # U = syndata()  #   lamda = 0.5
    # U = randata() #0.033
    # U = Gausdata()  # 0.0695

    # (U,y) = make_moons(n_samples=20,noise=0.1,random_state=1) #lamda = 0.085 2 clusters
    # next 3 lines: noisy 3 blobs lambda = 0.15
    # (U1,y) = make_blobs(n_samples=50,n_features=2,centers=3,random_state=1)
    # U2 = np.random.uniform(low=-10, high=10, size=(15,2))
    # U = np.concatenate((U1,U2))

    # 200 nodes demo
    (U, y) = make_blobs(n_samples=200, n_features=2, centers=3, random_state=1)
    # adding noises
    # U2 = np.random.uniform(low=-10, high=5, size=(20,2))
    # U = np.concatenate((U1,U2))
    # lamda = 0.042

    # 100 nodes demo
    # (U,y) = make_blobs(n_samples=100,n_features=2,centers=3,random_state=1)
    # lamda = 0.0425

    (n, d) = U.shape

    X = cc.ccADMM(U, lamda)

    # collect clusters
    indices = cc.collectCluster(U, X, n)
    ax1.scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=0.1)
    # draw colors of points #######################################################################
    _, noC = indices.shape
    aa = [*range(1, noC + 1, 1)]
    pcolor = np.dot(indices, aa)
    ax1.scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.1)
    ax1.set_aspect('equal')
    # ax1.set_title('Convex clustering')
    cc.ccVizclust(U, indices, lamda, ax1)

    # k-means clustering
    km = KMeans(n_clusters=3)
    km.fit(U)
    kmy = km.predict(U)
    ax2.set_aspect('equal')
    ax2.scatter(U[:, 0], U[:, 1], c=kmy, s=0.1)
    # ax2.set_title('K-means')

    ac = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='single')
    acy = ac.fit_predict(U)
    ax3.set_aspect('equal')
    ax3.scatter(U[:, 0], U[:, 1], c=acy, s=0.1)
    # ax3.set_title('Agglomerative')

    #    plt.show()
    #    fig.savefig("threeblobs.pdf", bbox_inches='tight')

    print('Done.')


def runTestDemo():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    (U, y) = make_moons(n_samples=100, noise=0.15, random_state=1)  # lamda = 0.085 2 clusters
    (n, d) = U.shape
    lamda = 0.0173

    X = cc.ccADMM(U, lamda)

    # collect clusters
    indices = cc.collectCluster(U, X, n)
    ax1.scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=0.1)
    # draw colors of points #######################################################################
    _, noC = indices.shape
    aa = [*range(1, noC + 1, 1)]
    pcolor = np.dot(indices, aa)
    ax1.scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.1)
    ax1.set_aspect('equal')
    ax1.set_title('Convex clustering')
    cc.ccVizclust(U, indices, lamda, ax1)

    ax2.scatter(X[:, 0], X[:, 1], c=pcolor, marker="+", s=0.1)
    ax2.set_aspect('equal')
    ax2.set_title('solution')

    plt.show()
    fig.savefig("test.pdf", bbox_inches='tight')


def mainDemo():
    # How difference the solutions of convex clustering are compared to that of k-means and agglomerative clusterings
    # Figure 2 in the paper

    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    # moon demo
    lamda = 0.0172
    moonDemo(lamda, axs[0], axs[1], axs[2])
    plt.show()
    fig.savefig("main1.pdf", bbox_inches='tight')

    # uniform
    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.01307
    uniformDemo(lamda, axs[0], axs[1], axs[2])
    plt.show()
    fig.savefig("main2.pdf", bbox_inches='tight')

    # threeblobdemo
    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.042
    threeblobsDemo(lamda, axs[0], axs[1], axs[2])
    plt.show()
    fig.savefig("main3.pdf", bbox_inches='tight')

    # noisyblobdemo
    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.042
    noisyblobsDemo(lamda, axs[0], axs[1], axs[2])
    plt.show()
    fig.savefig("main4.pdf", bbox_inches='tight')


def unidm():
    fig, axs = plt.subplots(1, 3, sharey='all')
    lamda = 0.01307
    uniformDemo(lamda, axs[0], axs[1], axs[2])
    plt.show()
    fig.savefig("uniform.pdf", bbox_inches='tight')


def cconly(U, lamda, ax1):
    # cluster data given lambda, vizualize in ax1
    (n, d) = U.shape
    X = cc.ccADMM(U, lamda)
    # collect clusters
    indices = cc.collectCluster(U, X, n)
    ax1.scatter(X[:, 0], X[:, 1], color='blue', marker="+", zorder=2, s=0.0001)
    # draw colors of points #######################################################################
    _, noC = indices.shape
    aa = [*range(1, noC + 1, 1)]
    pcolor = np.dot(indices, aa)
    ax1.scatter(U[:, 0], U[:, 1], c=pcolor, zorder=3, s=0.05)
    ax1.set_aspect('equal')
    cc.ccVizclust(U, indices, lamda, ax1)


def boundingDemo():
    # How the clustering solutions change as more points are added to a cluster.
    # Figure 1 in the paper
    centers = [[0.5, 0.5], [-4, -4], [-8, 4]]
    (U, y) = make_blobs(n_samples=60, n_features=2, centers=centers, random_state=1)
    lamda = 0.11
    fig, axs = plt.subplots(1, 4, sharex='all', sharey='all')

    cconly(U, lamda, axs[0])

    np.random.seed(1)
    U11 = np.random.uniform(size=(8, 2))
    U1 = np.concatenate((U, U11))
    cconly(U1, lamda, axs[1])

    np.random.seed(1)
    U22 = np.random.uniform(size=(16, 2))
    U2 = np.concatenate((U, U22))
    cconly(U2, lamda, axs[2])

    np.random.seed(1)

    U33 = np.random.uniform(size=(24, 2))
    U3 = np.concatenate((U, U33))
    cconly(U3, lamda, axs[3])
    plt.show()
    fig.savefig("bounding.pdf", bbox_inches='tight')

    #   shrinking lambda, too
    fig1, axs1 = plt.subplots(1, 4, sharex='all', sharey='all')
    cconly(U, lamda, axs1[0])
    cconly(U1, 0.104, axs1[1])
    cconly(U2, lamda * 0.8, axs1[2])
    cconly(U3, lamda * 0.7, axs1[3])
    plt.show()
    fig1.savefig("bounding1.pdf", bbox_inches='tight')


def newDemo():
    # How fast the solutions change with small change in lambda
    # Figure 1 in the supplementary material
    # moon demo
    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.017
    (U, y) = make_moons(n_samples=100, noise=0.15, random_state=1)
    cconly(U, lamda, axs[0])
    lamda = 0.0172
    cconly(U, lamda, axs[1])
    lamda = 0.0175
    cconly(U, lamda, axs[2])
    plt.show()
    fig.savefig("supp1.pdf", bbox_inches='tight')

    # uniform

    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.013
    np.random.seed(1)
    U = np.random.uniform(size=(50, 2))
    cconly(U, lamda, axs[0])
    lamda = 0.01307
    cconly(U, lamda, axs[1])
    lamda = 0.0131
    cconly(U, lamda, axs[2])
    plt.show()
    fig.savefig("supp2.pdf", bbox_inches='tight')

    # threeblobdemo
    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.035
    (U, y) = make_blobs(n_samples=200, n_features=2, centers=3, random_state=1)
    cconly(U, lamda, axs[0])
    lamda = 0.04
    cconly(U, lamda, axs[1])
    lamda = 0.045
    cconly(U, lamda, axs[2])
    fig.savefig("supp3.pdf", bbox_inches='tight')

    # noisyblobdemo
    fig, axs = plt.subplots(1, 3, sharex='all', sharey='all')
    lamda = 0.035
    (U1, y) = make_blobs(n_samples=180, n_features=2, centers=3, random_state=1)
    # adding noises
    U2 = np.random.uniform(low=-10, high=5, size=(20, 2))
    U = np.concatenate((U1, U2))
    cconly(U, lamda, axs[0])
    lamda = 0.04
    cconly(U, lamda, axs[1])
    lamda = 0.045
    cconly(U, lamda, axs[2])
    fig.savefig("supp4.pdf", bbox_inches='tight')


def irisdemo():
    idata = load_iris()  # 150 samples x 4 dim, 3 classes (50 each)
    U = idata.data
    n, d = U.shape
    smallU = U[0:n, :]
    lamdas = [0.01, 0.015, 0.02, 0.025, 0.03]
    rows = len(lamdas)
    toptens = [[0 for i in range(10)] for j in range(rows)]

    for i in range(rows):
        X = cc.ccADMM(U, lamdas[i])
        indices = cc.collectCluster(U, X, n)
        csizes = np.sum(indices, axis=0).tolist()
        csizes.sort(reverse=True)
        for j in range(min(10, len(csizes))):
            toptens[i][j] = csizes[j]

    # plotting cluster sizes real data
    idx = range(1, 11)
    for i in range(rows):
        plt.plot(idx, toptens[i], label=lamdas[i])
    plt.yscale('log')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('iris plants data cluster sizes')
    plt.show()
    plt.savefig("iris.pdf", bbox_inches='tight')



def winedemo():
    wdata = load_wine()  # 173x13, 3 classes [59,71,48]
    U = wdata.data
    n, d = U.shape
    print(U.shape)
    smallU = U[0:n, :]
    lamdas = [1, 1.5, 2, 2.5, 3, 3.5, 4]
    rows = len(lamdas)
    toptens = [[0 for i in range(10)] for j in range(rows)]

    for i in range(rows):
        X = cc.ccADMM(U, lamdas[i])
        indices = cc.collectCluster(U, X, n)
        csizes = np.sum(indices, axis=0).tolist()
        csizes.sort(reverse=True)
        for j in range(min(10,len(csizes))):
            toptens[i][j]= csizes[j]

    # plotting cluster sizes real data
    idx = range(1, 11)
    for i in range(rows):
        plt.plot(idx, toptens[i], label=lamdas[i])
    plt.yscale('log')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('wine recognition data cluster sizes')
    plt.show()
    plt.savefig("wine.pdf", bbox_inches='tight')


def diabetesdemo():
    ddata = load_diabetes()  # 442x10, regression
    U = ddata.data
    n, d = U.shape
    smallU = U[0:n, :]
    lamdas = [0.0007, 0.0006, 0.0005, 0.0004, 0.0003, 0.0002]
    rows = len(lamdas)
    toptens = [[0 for i in range(10)] for j in range(rows)]

    for i in range(rows):
        X = cc.ccADMM(smallU, lamdas[i])
        indices = cc.collectCluster(smallU, X, n)
        csizes = np.sum(indices, axis=0).tolist()
        csizes.sort(reverse=True)
        for j in range(min(10,len(csizes))):
            toptens[i][j]= csizes[j]

    # plotting cluster sizes real data
    idx = range(1, 11)
    for i in range(rows):
        plt.plot(idx, toptens[i], label=lamdas[i])
    plt.yscale('log')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('diabetes data cluster sizes')
    plt.show()
    plt.savefig("diabetes.pdf", bbox_inches='tight')


def monks():
    mdata = pd.read_csv(r'https://raw.githubusercontent.com/canhhao/convexclustering/main/monks-1.csv', header=None)
    print(mdata.head())
    U = mdata.to_numpy()
    print(U.shape)
    n, d = U.shape
    lamdas = [0.02317, 0.02316, 0.02315]
    rows = len(lamdas)
    toptens = [[0 for i in range(10)] for j in range(rows)]

    for i in range(rows):
        X = cc.ccADMM(U, lamdas[i])
        indices = cc.collectCluster(U, X, n)
        csizes = np.sum(indices, axis=0).tolist()
        csizes.sort(reverse=True)
        for j in range(min(10, len(csizes))):
            toptens[i][j] = csizes[j]

   # plotting cluster sizes real data
    idx = range(1, 11)
    for i in range(rows):
        plt.plot(idx, toptens[i], label=lamdas[i])
    plt.yscale('log')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('monks-1 data cluster sizes')
    plt.show()
    plt.savefig("monks.pdf", bbox_inches='tight')

def hayes_roth():
    hdata = pd.read_csv(r'https://raw.githubusercontent.com/canhhao/convexclustering/main/hayes-roth.csv', header=None)

    print(hdata.head())
    U = hdata.to_numpy()
    print(U.shape)
    n, d = U.shape

    lamdas = [0.0275, 0.025, 0.0225, 0.02]

    rows = len(lamdas)
    toptens = [[0 for i in range(10)] for j in range(rows)]

    for i in range(rows):
        X = cc.ccADMM(U, lamdas[i])
        indices = cc.collectCluster(U, X, n)
        csizes = np.sum(indices, axis=0).tolist()
        csizes.sort(reverse=True)
        for j in range(min(10, len(csizes))):
            toptens[i][j] = csizes[j]

    # plotting cluster sizes real data
    idx = range(1, 11)
    for i in range(rows):
        plt.plot(idx, toptens[i], label=lamdas[i])
    plt.yscale('log')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('hayes roth data cluster sizes')
    plt.show()
    plt.savefig("hayes_roth.pdf", bbox_inches='tight')

def runDemo(option = 0):
    print("Please select the experiments:")
    print("0 : bounding balls for different lambdas and cluster densities")
    print("1 : comparing convex clustering vs k-means and aggromerative clustering")
    print("2 : convex clustering with different lambdas on synthetic datasets")
    print("3 : top 10 cluster sizes on iris plants data (different lambdas)")
    print("4 : top 10 cluster sizes on wine recognition data (different lambdas)")
    print("5 : top 10 cluster sizes on monks-1 data (different lambdas)")
    print("6 : top 10 cluster sizes on hayes roth data (different lambdas)")
    value = input("Please select 0-6:\n")
    option = int(value)

    if option == 2:
        newDemo()
    elif option == 0:
        boundingDemo()
    elif option == 1:
        mainDemo()
    elif option == 3:
        irisdemo()
    elif option == 4:
        winedemo()
    elif option == 5:
        monks()
    elif option == 6:
        hayes_roth()
    else:
        print("Must select options from 0-6")

if __name__ == '__main__':
    #boundingDemo() # demo: the first experiments
    # mainDemo()  # demo: the second experiment
    # newDemo()  # demo: the experiment on the supplementary material
    irisdemo()
    #winedemo()

    pass

    #diabetesdemo()
    #monks()
    #hayes_roth()
