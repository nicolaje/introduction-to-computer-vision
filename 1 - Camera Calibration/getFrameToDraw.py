def getFrameToDraw(M):
    #ex=np.array([1,0,0,0])
    #ey=np.array([0,1,0,0])
    #ez=np.array([0,0,1,0])
    print(M)
    ex1=np.dot(M,ex)
    ex2=np.dot(M,ey)
    ex3=np.dot(M,ez)
    a1=Arrow3D([M[0,3],ex1[0]],[M[1,3],ex1[1]],[M[2,3],ex1[2]],mutation_scale=20,lw=3,arrowstyle="-|>",color="r")
    a2=Arrow3D([M[0,3],ex2[0]],[M[1,3],ex2[1]],[M[2,3],ex2[2]],mutation_scale=20,lw=3,arrowstyle="-|>",color="r")
    a3=Arrow3D([M[0,3],ex3[0]],[M[1,3],ex3[1]],[M[2,3],ex3[2]],mutation_scale=20,lw=3,arrowstyle="-|>",color="r")
    return a1,a2,a3