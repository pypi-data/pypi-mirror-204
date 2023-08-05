import numpy as np
import matplotlib.pyplot as plt


thres1 = 1e-6  # threshold to consider propotypes as "the same" or not the same due to numerical instability

tolerance = 1e-10  # tolerance of ADMM when to stop


def ccColumnNodeEdgeIncidentMatrix(n):
    # 1 -1 0
    # 1 0 -1
    # 0 1 -1
    A = np.zeros((0, n))
    for i in range(n - 1):
        # from the first block
        zp = np.zeros((n - i - 1, i))  # zero padding block
        oc = np.ones((n - i - 1, 1))  # column of 1
        t = np.concatenate((zp, oc), axis=1)
        t2 = np.concatenate((t, -1 * np.identity(n - i - 1)), axis=1)  # concat -I(n-i-1)
        A = np.concatenate((A, t2))
    return A


def ccADMMOld(U, lamda):
    # performing convex clustering using ADMM algorithm
    n, d = U.shape
    # initializating X, v, nu, Y, L
    X = np.copy(U)
    nu = 1
    Y = np.zeros((n, d))
    A = ccColumnNodeEdgeIncidentMatrix(n)
    aA = np.absolute(A)
    m, _ = A.shape
    v = np.zeros((m, d))  # new variables of fusion penalty
    L = np.zeros((m, d))  # lagrange multiplier
    lastX = np.copy(X)  # last solution to check for convergence

    for k in range(10000):
        # Update X
        for i in range(n):
            Y[i] = U[i] + np.dot(A[:, i], L + nu * v)
        X = (Y + n * nu * np.mean(U)) / (1 + n * nu)

        for i in range(m):
            delta = lamda / nu
            v[i] = proxADMM(A[i].dot(X) - (1 / nu) * L[i], delta)
            L[i] += nu * (v[i] - A[i].dot(X))

        # check stopping condition
        if np.linalg.norm(lastX - X) < tolerance:
            print('ADMM with ' + str(k) + ' iterations')
            break
        else:
            lastX = np.copy(X)

    return X


def ccADMM(U, lamda):
    # performing convex clustering using ADMM algorithm
    n, d = U.shape
    # initializating X, v, nu, Y, L
    X = np.copy(U)
    nu = 1
    Y = np.zeros((n, d))
    A = ccColumnNodeEdgeIncidentMatrix(n)
    aA = np.absolute(A)
    m, _ = A.shape
    v = np.zeros((m, d))  # new variables of fusion penalty
    L = np.zeros((m, d))  # lagrange multiplier
    lastX = np.copy(X)  # last solution to check for convergence

    for k in range(10000):
        # Update X

        Y = U + np.dot(A.transpose((1, 0)), L + nu * v)
        X = (Y + n * nu * np.mean(U)) / (1 + n * nu)

        delta = lamda / nu

        # For proxADMM
        #    A[i].dot(X) - (1 / nu) * L[i]
        AX = np.dot(A, X)
        LD = L / nu
        AXSLD = AX - LD

        # Norm
        LnormAXSLD = np.linalg.norm(AXSLD, axis=1, keepdims=True)
        LnormAXSLD[LnormAXSLD==0]=1
        iLnormAXSLD = delta / LnormAXSLD #if (LnormAXSLD > 0) else delta

        # max(0, 1 - delta / l) * v
        vv = (1 - iLnormAXSLD)
        vv[vv <= 0] = 0
        vv = vv * AXSLD
        v = vv
        # L += np.expand_dims(nu, axis=-1) * (vv - AX)
        L += nu * (vv - AX)
        # check stopping condition
        if np.linalg.norm(lastX - X) < tolerance:
            print('ADMM with ' + str(k) + ' iterations')
            break
        else:
            lastX = np.copy(X)

    return X


def proxADMM(v, delta):
    # print("ADMM", v.shape)
    l = np.linalg.norm(v)
    return max(0, 1 - delta / l) * v


def collectCluster(U, X, k):
    # given cluster propotypes, group samples into clusters
    n, d = U.shape
    cind = np.zeros((n, k))
    propo = np.zeros((k, d))
    # cluster 1
    cind[0, 0] = 1
    propo[0] = X[0]
    noC = 1

    for i in range(1, n):
        nfound = 1
        for j in range(noC):
            if np.linalg.norm(X[i] - propo[j]) < thres1:
                # found old cluster
                cind[i, j] = 1
                nfound = 0
                break  # break j loop
        if nfound:
            # new cluster
            cind[i, noC] = 1
            propo[noC] = X[i]
            noC = noC + 1
    indices = cind[:, 0:noC]
    return indices


def ccVizclust(U, indices, lamda, ax1):
    # visualize clustering solotions
    _, noC = indices.shape
    csize = sum(indices)
    print("There are ", noC, " clusters found.")
    # print(indices)
    # print(U)
    ccenter = np.dot(np.dot(np.diag(1 / csize), indices.transpose()), U)
    # print(ccenter)

    ax1.set_aspect('equal')
    for i in range(noC):
        circ = plt.Circle(ccenter[i], (csize[i] - 1) * lamda, zorder=1)
        # circ.set_edgecolor('red')
        circ.set_facecolor('lightcyan')
        ax1.add_patch(circ)
        # plt.gcf().gca().add_patch(circ)