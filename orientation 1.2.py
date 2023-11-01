# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

#testing that the read function actually works 
df = pd.read_csv('actual_data1.csv',usecols=['accel-x', 'accel-y', 'accel-z','mag-x', 'mag-y', 'mag-z', 'gyro-x', 'gyro-y', 'gyro-z','lat','long','seconds'])
#print(df)

arr=np.array(df)
#print(arr)

diode = np.array([[0.51],[0],[0.86]])
#print(diode)


pitch = np.arcsin(-arr[:,3])
print(pitch)

roll = np.arcsin(arr[:,4]/np.cos(pitch))
#print(roll)

mgx = arr[:,9]*np.cos(pitch)-arr[:,11]*np.sin(pitch)
mgy = arr[:,9]*np.sin(roll)*np.sin(pitch)+arr[:,10]*np.cos(roll)-arr[:,11]*np.sin(roll)*np.cos(pitch) 
yaw = np.arctan2(mgy,mgx)
#print(yaw)

accrot_matrix = np.zeros(shape=[len(pitch),3,3])
this_matrix = np.zeros(shape=[3,3])  

acc_1 = np.cos(pitch)*np.cos(yaw) 
acc_2 = np.sin(roll)*np.sin(pitch)*np.cos(yaw)-np.cos(roll)*np.sin(yaw)
acc_3 = np.cos(roll)*np.sin(pitch)*np.cos(yaw)+np.sin(roll)*np.sin(yaw)
acc_4 = np.cos(pitch)*np.sin(yaw)
acc_5 = np.sin(roll)*np.sin(pitch)*np.sin(yaw)+np.cos(roll)*np.cos(yaw)
acc_6 = np.cos(roll)*np.sin(pitch)*np.sin(yaw)+np.sin(roll)*np.cos(yaw)
acc_7 = -np.sin(pitch)
acc_8 = np.sin(roll)*np.cos(pitch)
acc_9 = np.cos(roll)*np.cos(pitch)

for i in range(len(acc_1)):
    this_matrix[0,0] = acc_1[i]
    this_matrix[0,1] = acc_2[i]
    this_matrix[0,2] = acc_3[i]
    this_matrix[1,0] = acc_4[i]
    this_matrix[1,1] = acc_5[i]
    this_matrix[1,2] = acc_6[i]
    this_matrix[2,0] = acc_7[i]
    this_matrix[2,1] = acc_8[i]
    this_matrix[2,2] = acc_9[i]
    
    accrot_matrix[i] = this_matrix

#print(accrot_matrix)


accdiode = np.matmul(accrot_matrix,diode)
print("acc/mag diode")
print(accdiode)

####gyroscoe rotation 
gyro_1 = np.array(arr[:,6])
gyro_2 = np.array(arr[:,7])
gyro_3 = np.array(arr[:,8])

gyrorot_matrix = np.zeros(shape=[len(gyro_1),3,3])
gyro_matrix = np.zeros(shape=[3,3])

gyrorot_diode = np.zeros(shape=[len(gyro_1),3,1])
gyro_diode = np.zeros(shape=[3,1])
gyrorot_angle = np.zeros(shape=[len(gyro_2),1])
gyro_angle = np.zeros(shape=[1])

for i in range(len(gyro_1)):
    gyro_diode[0] = gyro_1[i]/(np.sqrt((gyro_1[i]**2)+(gyro_2[i]**2)+(gyro_3[i]**2)))
    gyro_diode[1] = gyro_2[i]/(np.sqrt((gyro_1[i]**2)+(gyro_2[i]**2)+(gyro_3[i]**2)))
    gyro_diode[2] = gyro_3[i]/(np.sqrt((gyro_1[i]**2)+(gyro_2[i]**2)+(gyro_3[i]**2)))
    
    gyrorot_diode[i] = gyro_diode
    
#print(gyrorot_diode)
#that is the rotation axis for all 

for i in range(len(gyro_1)):
    gyro_angle[0] = (np.sqrt((gyro_1[i]**2)+(gyro_2[i]**2)+(gyro_3[i]**2)))
    gyrorot_angle[i] = gyro_angle
    
#print(gyrorot_angle)
#that is the angle rotated around the roataion axis 

R_1 = (np.cos(gyrorot_angle)+(gyrorot_diode[:,0]**2)*(1-np.cos(gyrorot_angle)))
R_2 = (gyrorot_diode[:,0]*gyrorot_diode[:,1]*(1-np.cos(gyrorot_angle))-gyrorot_diode[:,2]*np.sin(gyrorot_angle))
R_3 = (gyrorot_diode[:,0]*gyrorot_diode[:,2]*(1-np.cos(gyrorot_angle))+gyrorot_diode[:,1]*np.sin(gyrorot_angle))
R_4 = (gyrorot_diode[:,0]*gyrorot_diode[:,1]*(1-np.cos(gyrorot_angle))+gyrorot_diode[:,2]*np.sin(gyrorot_angle))
R_5 = (np.cos(gyrorot_angle)+(gyrorot_diode[:,1]**2)*(1-np.cos(gyrorot_angle)))
R_6 = (gyrorot_diode[:,1]*gyrorot_diode[:,2]*(1-np.cos(gyrorot_angle))-gyrorot_diode[:,0]*np.sin(gyrorot_angle))
R_7 = (gyrorot_diode[:,0]*gyrorot_diode[:,2]*(1-np.cos(gyrorot_angle))-gyrorot_diode[:,1]*np.sin(gyrorot_angle))
R_8 = (gyrorot_diode[:,1]*gyrorot_diode[:,2]*(1-np.cos(gyrorot_angle))+gyrorot_diode[:,0]*np.sin(gyrorot_angle))
R_9 = (np.cos(gyrorot_angle)+(gyrorot_diode[:,2]**2)*(1-np.cos(gyrorot_angle)))

#print(R_2)

for i in range(len(R_1)):
    gyro_matrix[0,0] = R_1[i]
    gyro_matrix[0,1] = R_2[i]
    gyro_matrix[0,2] = R_3[i]
    gyro_matrix[1,0] = R_4[i]
    gyro_matrix[1,1] = R_5[i]
    gyro_matrix[1,2] = R_6[i]
    gyro_matrix[2,0] = R_7[i]
    gyro_matrix[2,1] = R_8[i]
    gyro_matrix[2,2] = R_9[i]
    
    gyrorot_matrix[i] = gyro_matrix
    
#print(gyrorot_matrix)

input_vector = np.zeros(shape=[len(R_1),3,1])
output_vector = np.zeros(shape=[len(R_1),3,1])

input_vector[0] = [[1],[1],[1]]

for i in range(len(R_1)):
    if i != 0:
        input_vector[i] = output_vector[i-1]
    output_vector[i] = np.matmul(gyrorot_matrix[i],input_vector[i])

print("gyro diode")    
print(output_vector)

#####sun angle
start = 11.167
time = np.array(arr[:,2])
LT = start + ((time/60)/60)
LSTM = 15*(-5)
day = 142
#day = 143
B = np.deg2rad((360/365)*(day-81))
EoT = 9.87*np.sin(2*B)-7.53*np.cos(B)-1.5*np.sin(B)
lat = np.array(arr[:,0])
long = np.array(arr[:,1])
TC = 4*(long-LSTM)+EoT
LST = LT+(TC/60)
HRA = 15*(LST-12)
ang = 23.45*np.sin(B)

rang = np.deg2rad(ang) 
rlat = np.deg2rad(lat)
rlong = np.deg2rad(long)
rHRA = np.deg2rad(HRA)

ele = np.arcsin(np.sin(rang)*np.sin(rlat)+np.cos(rang)*np.cos(rlat)*np.cos(rHRA))
azimuth = np.arccos((np.sin(rang)*np.cos(rlat)-np.cos(rang)*np.sin(rlat)*np.cos(rHRA))/np.cos(ele))

x = np.sin((np.pi/2)-ele)*np.cos(azimuth)
y = np.sin((np.pi/2)-ele)*np.sin(azimuth)
z = np.cos((np.pi/2)-ele)

sunrot_matrix = np.zeros(shape=[len(x),3,1])
sun_matrix = np.zeros(shape=[3,1])

for i in range(len(x)):
    sun_matrix[0,0] = x[i]
    sun_matrix[1,0] = y[i]
    sun_matrix[2,0] = z[i]
    
    sunrot_matrix[i] = sun_matrix

print("sun angle")
print(sunrot_matrix)

######dot product
accdotrot = np.zeros(shape=[len(acc_1)])
accdot = np.zeros(shape=[1])
accangle = np.zeros(shape = [1])
accangrot = np.zeros(shape=[len(acc_1)])

for i in range(len(accdiode)):
    accdot[0] = np.tensordot(accdiode[i],sunrot_matrix[i],2)
    accdotrot[i] = accdot

print("acc dot sun")
print(accdotrot)

for i in range(len(accdiode)):
    acclen = np.sqrt((accdiode[i,0]**2)+(accdiode[i,1]**2)+(accdiode[i,2]**2))
    sunlen = np.sqrt((sunrot_matrix[i,0]**2)+(sunrot_matrix[i,1]**2)+(sunrot_matrix[i,2]**2))
    accangle[0] = np.arccos(accdotrot[i]/(acclen*sunlen))
    #print(accangle)
    accangrot[i] = accangle

print("acc angle from sun dot")
print(accangrot)

gyrodotrot = np.zeros(shape=[len(acc_1)])
gyrodot = np.zeros(shape=[1])
gyroangle = np.zeros(shape = [1])
gyroangrot = np.zeros(shape=[len(acc_1)])

for i in range(len(R_1)):
    gyrodot[0] = np.tensordot(output_vector[i],sunrot_matrix[i],2)
    #print(gyrodot)
    gyrodotrot[i] = gyrodot

print("gyro dot sun")
print(gyrodotrot)

for i in range(len(accdiode)):
    gyrolen = np.sqrt((output_vector[i,0]**2)+(output_vector[i,1]**2)+(output_vector[i,2]**2))
    sunlen = np.sqrt((sunrot_matrix[i,0]**2)+(sunrot_matrix[i,1]**2)+(sunrot_matrix[i,2]**2))
    gyroangle[0] = np.arccos(gyrodotrot[i]/(gyrolen*sunlen))
    #print(accangle)
    gyroangrot[i] = gyroangle

print("gyro angle from sun dot")
print(gyroangrot)

######cross product

acccrossrot = np.zeros(shape=[len(acc_1),3])
accanglec = np.zeros(shape = [1])
accangrotc = np.zeros(shape=[len(acc_1)])

for i in range(len(accdiode)):
    #print(accdiode[i])
    acctemp = (accdiode[i]).flatten()
    suntemp = (sunrot_matrix[i]).flatten()
    acccross = np.cross(acctemp,suntemp)
    acccrossrot[i] = acccross

print("acc cross sun")
print(acccrossrot)

for i in range(len(accdiode)):
    crossleng = np.sqrt((acccrossrot[i,0]**2)+(acccrossrot[i,1]**2)+(acccrossrot[i,2]**2))
    accleng = np.sqrt((accdiode[i,0]**2)+(accdiode[i,1]**2)+(accdiode[i,2]**2))
    sunleng = np.sqrt((sunrot_matrix[i,0]**2)+(sunrot_matrix[i,1]**2)+(sunrot_matrix[i,2]**2))
    accanglec[0] = np.arcsin(crossleng/(accleng*sunleng))
    accangrotc[i] = accanglec

print("acc angle from sun cross")
print(accangrotc)

gyrocrossrot = np.zeros(shape=[len(acc_1),3])
gyroanglec = np.zeros(shape = [1])
gyroangrotc = np.zeros(shape=[len(acc_1)])

for i in range(len(accdiode)):
    #print(accdiode[i])
    gyrotemp = (output_vector[i]).flatten()
    suntemp = (sunrot_matrix[i]).flatten()
    gyrocross = np.cross(gyrotemp,suntemp)
    gyrocrossrot[i] = gyrocross

print("gyro cross sun")
print(gyrocrossrot)

for i in range(len(accdiode)):
    crossleng = np.sqrt((gyrocrossrot[i,0]**2)+(gyrocrossrot[i,1]**2)+(gyrocrossrot[i,2]**2))
    gyroleng = np.sqrt((output_vector[i,0]**2)+(output_vector[i,1]**2)+(output_vector[i,2]**2))
    sunleng = np.sqrt((sunrot_matrix[i,0]**2)+(sunrot_matrix[i,1]**2)+(sunrot_matrix[i,2]**2))
    gyroanglec[0] = np.arcsin(crossleng/(gyroleng*sunleng))
    gyroangrotc[i] = gyroanglec

print("gyro angle from sun cross")
print(gyroangrotc)

#######printing to a csv file 
#print(df.to_string())
#prints a new csv file
#df.to_csv("Acclex.csv")

dv = pd.DataFrame({"yaw":yaw, "acc angle dot":accangrot, "gyro angle dot":gyroangrot, "acc angle cross":accangrotc, "gyro angle cross":gyroangrotc})
dv.to_csv("angles1-2.csv")

db = pd.DataFrame({"acc vect":accdiode.flatten(), "gyro vect":output_vector.flatten(), "sun vect":sunrot_matrix.flatten()})
db.to_csv("vectors1-2.csv")
