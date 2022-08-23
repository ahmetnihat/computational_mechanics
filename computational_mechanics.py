from math import radians, cos, sin
import numpy as np
import pandas as pd

def create_element(angle, length):
    if angle == 90 or angle == 180:
        angle = angle * (3.14 / 180)
        element_cos = round(cos(angle))
        element_sin = round(sin(angle))
    else:
        angle = radians(angle)
        element_cos = cos(angle)
        element_sin = sin(angle)
    return length, element_cos, element_sin

A, E, alfa, deltaT = 1, 29.2 * 10**6, 12 * 10 ** -6, 10

def create_K(element):
    K = np.ones((4,4))
    element_length, element_cos, element_sin = element[0], element[1], element[2]
    K[0,0], K[0,1], K[0,2], K[0,3] = element_cos ** 2, element_cos * element_sin, - (element_cos ** 2), - (element_cos * element_sin)
    K[1,0], K[1,1], K[1,2], K[1,3] = element_cos * element_sin, element_sin ** 2, - (element_cos * element_sin), - (element_sin ** 2)
    K[2,0], K[2,1], K[2,2], K[2,3] = - (element_cos ** 2), - (element_cos * element_sin), element_cos ** 2, element_cos * element_sin
    K[3,0], K[3,1], K[3,2], K[3,3] =  - (element_cos * element_sin), - (element_sin ** 2), element_cos * element_sin, element_sin ** 2
    
    K = K * ((E * A / element_length) * alfa * deltaT)
    return K, element_length

element1 = create_element(0, 40)
element2 = create_element(90, 30)
element3 = create_element(180, 40)
element4 = create_element(36.87, 50)

K1, element1_length = create_K(element1)
K2, element2_length = create_K(element2)
K3, element3_length = create_K(element3)
K4, element4_length = create_K(element4)


K1_df, K2_df, K3_df, K4_df = pd.DataFrame(K1), pd.DataFrame(K2), pd.DataFrame(K3), pd.DataFrame(K4)

K1_df.columns = K1_df.index = ['u1', 'v1','u2', 'v2']
K2_df.columns = K2_df.index = ['u2', 'v2','u3', 'v3']
K3_df.columns = K3_df.index = ['u3', 'v3','u4', 'v4']
K4_df.columns = K4_df.index = ['u1', 'v1','u3', 'v3']

K = np.zeros((8,8))
K_df = pd.DataFrame(K)
K_df.columns = K_df.index = ['u1', 'v1','u2', 'v2', 'u3','v3', 'u4','v4']

K_matrices = [K1_df, K2_df, K3_df, K4_df]

for column in K_df.columns:
    for row in K_df.index:
        
        for K_matrix in K_matrices:
            
            for column1 in K_matrix.columns:
                for row1 in K_matrix.index:
                    if str(column) == str(column1) and str(row) == str(row1):
                        K_df[f"{column}"][f"{row}"] = K_df[f"{column}"][f"{row}"] + K_matrix[f"{column1}"][f"{row1}"]
                        
K_df = K_df * (((A * E) / (element1_length + element2_length + element3_length + element4_length)) * (alfa * deltaT))

will_be_dropped_list = ['u1', 'v1', 'u2', 'u4', 'v4']
reduced = K_df
for row_and_column in will_be_dropped_list:
    reduced = reduced.drop(index=row_and_column, columns=row_and_column)
    
f2x, f3x, f3y = 20000, 0, -25000
f_matrix = np.array([f2x, f3x, f3y])

reduced_inverse = np.linalg.inv(reduced)

u_new = np.dot(reduced_inverse, f_matrix)
u_new = u_new = pd.DataFrame(u_new)
u_new.index, u_new.columns = ['v2', 'u3','v3'], ['u_new']

print_list = [("K1", K1_df), ("K2", K2_df), ("K3", K3_df), ("K4", K4_df), ("K Global", K_df), ("K new (reduced)", reduced), ("U new", u_new)]

for matrix_name, show in print_list:
    print("\n"+"*"*50)
    print(f"{matrix_name}: \n", show)
    print("\n"+"*"*50)