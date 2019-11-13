import numpy as np

tsk_loop = [300,290,295,297,293]
tsk_name = ['R0','R1','R2','R3','R4']


for nTsk, Tsk in enumerate(tsk_loop):

    surface  = (((np.random.rand(501,251)-0.5)*1.5)+Tsk)

    print('Array mean: %s' %np.mean(surface,(0,1)))
    print(np.shape(surface))

    np.savetxt('input_tsk' + tsk_name[nTsk], surface)

