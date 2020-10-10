# -*- coding=UTF-8 -*-
import networkx as nx
import arcpy
from networkx.algorithms import bipartite

inputsource = r'I:\彝良国土空间规划\数据分析\New File Geodatabase.gdb\p2pDistances_1'
targetsource = r'I:\彝良国土空间规划\数据分析\New File Geodatabase.gdb\sheshi_CopyFeatures'

# 读取权重表
top_nodes, bottom_nodes, weight = [], [], []
cursor = arcpy.SearchCursor(inputsource)
for row in cursor:
    top_nodes.append(row.IN_FID)                            # IN_FID
    bottom_nodes.append(row.guanlian_field)                 # guanlian_field
    weight.append(row.quanzhong_weight)
del cursor, row
print('模1节点数:' + str(len(top_nodes)))
print('模2节点数:' + str(len(bottom_nodes)))
print('权重为：:' + str(weight))

# 构建二模网络
# edges = zip(top_nodes, bottom_nodes)
# B = nx.Graph(edges)
# print(B.edges())

B = nx.Graph()
edges = []
x = 0
for i in range(len(top_nodes)):
    edges.append((top_nodes[i], bottom_nodes[i], weight[i]))
B.add_weighted_edges_from(edges)
# print(B.edges())


# 二模转一模
# G=bipartite.projected_graph(B,bottom_nodes,multigraph=True)
# print(G.edges(keys=True))

# 计算二模网络的度
degX,degY=bipartite.degrees(B,bottom_nodes,weight='weight')
# 计算二模网络的点度中心性
D = bipartite.degree_centrality(B, bottom_nodes)
degX_dict, degY_dict, D_dict = dict(degX), dict(degY), dict(D)
print('模1的度为：', len(degX), degX_dict, '模2的度为：', len(degY), degY_dict, '模2的点度中心性', len(D), D_dict, sep='\n')


arcpy.env.overwriteOutput = True
targetsource1 = targetsource + 'output'
print(targetsource)
arcpy.Copy_management(in_data=targetsource, out_data=targetsource1)


mo2fieldname,mo1fieldname,mo2centraldegree = 'mo2degree', 'mo1degree', 'mo2centraldegree'
arcpy.AddField_management(targetsource1, mo2fieldname, "FLOAT",field_alias=mo2fieldname, field_is_nullable="NULLABLE")
arcpy.AddField_management(targetsource1, mo1fieldname, "FLOAT",field_alias=mo1fieldname, field_is_nullable="NULLABLE")
arcpy.AddField_management(targetsource1, mo2centraldegree, "FLOAT",field_alias=mo2centraldegree, field_is_nullable="NULLABLE")

analysisSourceField = 'link_fid'
cursor = arcpy.da.UpdateCursor(targetsource1, [analysisSourceField, mo2fieldname, mo2centraldegree])
for row in cursor:
    if row[0] in degY_dict.keys():
        # print(row[0])
        row[1] = degY_dict[row[0]]
        row[2] = D_dict[row[0]]
        cursor.updateRow(row)
arcpy.AddMessage(u'centrality successed')


