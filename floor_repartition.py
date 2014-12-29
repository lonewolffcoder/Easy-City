# Principe : Parcours classique de la matrice.
# Quand m[i][j]=0, creation d'un bloc de building (m[][]=1), de largeur 2 (ou 1 quand ce n'est pas possible autrement) et de taille random (entre 2 et tailleMaxBloc) positionner
# horizontalement ou verticalement.
# Le bloc est ensuite entoure de rue (m[][]=1). Repete jusqu'au remplissage de la matrice.

import bpy
from bpy.props import *
import numpy as np
import bmesh
import random
from math import *

# def add_floor(context, width, height):
#     verts = []
#     faces = []
#     w = width + 1
#     h = height + 1
#     for i in range(w):
#         for j in range(h):
#             verts.append((i, j, 0))
#             if i > 0 and j > 0:
#                 faces.append(((i*h)+(j-1), (i*h)+j, ((i-1)*h)+j, ((i-1)*h)+(j-1)))
    
#     me = bpy.data.meshes.new("Floor")
#     me.from_pydata(verts, [], faces)
#     ob = bpy.data.objects.new("Floor", me)
#     context.scene.objects.link(ob)
#     context.scene.objects.active = ob
#     return ob

# bpy.ops.object.mode_set(mode='EDIT')
# floor = bpy.data.meshes['Floor']
# bm = bmesh.from_edit_mesh(floor)

# floor_faces = np.array(bm.faces)
# floor_faces = floor_faces.reshape(5,5)
# for i in range(len(floor_faces)):
#     floor_faces[i][i].select = True

# bmesh.update_edit_mesh(floor)
# bpy.ops.mesh.split()
# bpy.ops.mesh.separate(type='SELECTED')
# bm.free()  # free and prevent further access

def floor_repartition(matrice, size, tailleMaxBloc):
    for i in range (0, size):
        j = 0
        while j < size:
            if matrice[i][j] == 0:
                longueur = random.randint(2, tailleMaxBloc)
                
                # Si 3 cases vides, pas de bloc vertical, sinon route de largeur 2. Donc, d'office horizontal et d'office de longueur 3
                cntLong = 0
                for k in range(j, size):
                    if matrice[i][k] == 0:
                        cntLong += 1
                    else:
                        break
                if cntLong == 3:
                    longueur = 3
                    horizontal = 1
                else:
                    horizontal = random.randint(0, 1)
                   
                # Creation building m[][]=1 entoure de route m[][]=2
                
                # Longueur horizontal
                if horizontal:
                    if cntLong >= longueur:
                        if j+longueur+1 < size:
                            if matrice[i][j+longueur+1] == 2 and matrice[i][j+longueur] == 0:
                                longueur += 1
                    else:
                        longueur = cntLong
                           
                    iPlus1 = i+1 < size 
                    iPlus2 = i+2 < size
                    iMoins1 = i-1 > 0
                    tempLongueur = longueur
                    tempJ = j
                    while j < size and longueur > 0:
                        matrice[i][j] = 1
                        if iPlus1:
                            matrice[i+1][j] = 1
                        if iPlus2:
                            matrice[i+2][j] = 2
                        if iMoins1:
                            matrice[i-1][j] = 2
                        longueur -= 1
                        j += 1
                    if tempJ-1 > 0:
                        matrice[i][tempJ-1] = 2
                        if iPlus1:
                            matrice[i+1][tempJ-1] = 2
                        if iPlus2:
                            matrice[i+2][tempJ-1] = 2
                        if iMoins1:
                            matrice[i-1][tempJ-1] = 2
                    if j < size:
                        matrice[i][j] = 2
                        if iPlus1:
                            matrice[i+1][j] = 2
                        if iPlus2:
                            matrice[i+2][j] = 2
                        if iMoins1:
                            matrice[i-1][j] = 2
                else: #longueur vertical
                    jPlus1 = j+1 < size
                    jPlus2 = j+2 < size
                    jMoins1 = j-1 > 0
                    tempLongueur = longueur
                    tempI = i
                    while i < size and longueur > 0:
                        matrice[i][j] = 1
                        if jPlus1:
                            if matrice[tempI][j+1] == 2:
                                matrice[i][j+1] = 2
                            else:
                                matrice[i][j+1] = 1
                                if jPlus2:
                                    matrice[i][j+2] = 2
                        if jMoins1:
                            matrice[i][j-1] = 2
                        longueur -= 1
                        i += 1
                    i = tempI
                    if i+tempLongueur < size:
                        matrice[i+tempLongueur][j] = 2
                        if jPlus1:
                            if matrice[i+tempLongueur-1][j+1] == 2:
                                matrice[i+tempLongueur][j+1] = 2
                            else:
                                matrice[i+tempLongueur][j+1] = 2
                                if jPlus2:
                                    matrice[i+tempLongueur][j+2] = 2
                        if jMoins1:
                            matrice[i+tempLongueur][j-1]=2
                    if i-1 > 0:
                        matrice[i-1][j] = 2
                        if jPlus1:
                            if matrice[i][j+1] == 2:
                                matrice[i-1][j+1] = 2
                            else:
                                matrice[i-1][j+1] = 2
                                if jPlus2:
                                    matrice[i-1][j+2] = 2
                        if jMoins1:
                            matrice[i-1][j-1] = 2
                    j += 2
            else:
                 j += 1

def road_direction(matrice):
    # Direction aux routes : Vertical=3; Horizontal=4; Croisement=5
    size = len(matrice)
    for i in range (0, size):
        for j in range (0, size):
            vertical = 0
            horizontal = 0
            if matrice[i][j] == 2:
                print(i, j)
                if j-1 > 0:
                    if matrice[i][j-1] > 1:
                        horizontal = 1
                if j+1 < size:
                    if matrice[i][j+1] > 1:
                        horizontal = 1
                if i-1 > 0:
                    if matrice[i-1][j] > 1:
                        vertical = 1
                if i+1 < size:
                    if matrice[i+1][j] > 1:
                        vertical = 1
                if vertical and horizontal:
                    matrice[i][j] = 5
                else:
                    if vertical:
                        matrice[i][j] = 3
                    if horizontal:
                        matrice[i][j] = 4

#Parks in the city
def park_creation(matrice, park_mean):
    size = len(matrice)
    pcPark = park_mean
    nbrOfBuildings = sum(sum(matrice == 1))
    nbrOfParks = floor(nbrOfBuildings*pcPark)

    for i in range (0, nbrOfParks):
        keepSearching = True
        x = random.randint(0,size-1)
        y = random.randint(0,size-1)
        while keepSearching:
            if matrice[x][y] == 1:
                matrice[x][y] = -1
                keepSearching = False
            else:
                y += 1
                if y == size:
                    y = 0
                    x += 1
                    if x == size:
                        x = 0

def draw_roads_and_buildings(size, roads, buildings, max_block_size, parks, park_mean):
    scene = bpy.context.scene

    """bpy.ops.mesh.primitive_plane_add(location=(size, size, 0))    # add plane
    floor = bpy.context.object                              # just added object
    floor.name = 'Terrain'                                  # change name
    floor.scale = (size, size, 1)                           # resize
    """

    route1Obj = roads["horizontal"]
    route2Obj = roads["vertical"]
    route3Obj = roads["crossing"]

    city = bpy.data.objects['City']

    bpy.ops.object.add(type='EMPTY')
    road = bpy.context.object
    road.name = 'Road'
    road.parent = city

    bpy.ops.object.add(type='EMPTY')
    b_rep = bpy.context.object
    b_rep.name = 'Buildings'
    b_rep.parent = city

    bpy.ops.object.add(type='EMPTY')
    p_rep = bpy.context.object
    p_rep.name = 'parks'
    p_rep.parent = city

    matrice = np.zeros((size, size), int)
    floor_repartition(matrice, size, max_block_size)
    road_direction(matrice)
    park_creation(matrice, park_mean)

    for i in range (0, len(matrice)):
        for j in range (0, len(matrice[0])):
            if matrice[i][j] == 3:
                newRoute1 = route1Obj.copy()
                newRoute1.location = (2*i, 2*j, 0)
                scene.objects.link(newRoute1)
                newRoute1.parent = road
            elif matrice[i][j] == 4:
                newRoute2 = route2Obj.copy()
                newRoute2.location = (2*i, 2*j, 0)
                scene.objects.link(newRoute2)
                newRoute2.parent = road
            elif matrice[i][j] == 5:
                newRoute3 = route3Obj.copy()
                newRoute3.location = (2*i, 2*j, 0)
                scene.objects.link(newRoute3)
                newRoute3.parent = road
            elif matrice[i][j] == 1:
                newbuild = buildings[random.randint(0, len(buildings)-1)].copy()
                newbuild.location = (2*i, 2*j, 0)
                scene.objects.link(newbuild)
                newbuild.parent = b_rep
            elif matrice[i][j] == -1:
                newPark=parks[random.randint(0, len(parks)-1)].copy()
                newPark.location = (2*i, 2*j, 0)
                scene.objects.link(newPark)
                newPark.parent = p_rep
