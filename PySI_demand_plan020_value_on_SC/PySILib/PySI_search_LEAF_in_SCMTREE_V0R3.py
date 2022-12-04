# make_leaf.py
#
# 1) bf_tree幅優先treeの空リスト[]のpositionでleafの位置を判定する
# 2) seq_listを使って、leafのnode_nameをappendして生成する

# read_SCMTREE.py


import csv

filename = 'scmtree_profile.csv'

pc = []

with open(filename, encoding='utf8', newline='') as f:

    csvreader = csv.reader(f)

    header = next(csvreader) # タイトル行を飛ばす

    for row in csvreader:

        pc_pair = row[:2]


        if pc_pair[0] == "root":

            tree  = [ pc_pair[1] ,[]]
            #tree = [ 'JPN'      ,[]]


            seq_list  = [ pc_pair[1] ]
            #seq_list = [ 'JPN'      ]


        pc.append(pc_pair)

        #print(pc)

    #print('pc =', pc )

# *********************************************************
# tree_test.py
# https://qiita.com/toyohisa/items/cf38e4f815f4a7a03e09


#@220618 実行する瞬間にopen treeとして与える
# tree = ["家康",[]]

# tree2 = []

import copy

# 親子関係を配列で表したデータ

parent_childs = pc

# parent_childs = [['JPN', 'YTO'], ['JPN', 'NYC'], ['JPN', 'LAX'], ,,,]

print(parent_childs)


# 祖を指定して、ツリー構造を作成する。
def tree_generator(tree,rel_data,tier_list):

    w = [0]

    # ここから調査する対象のノード一覧
    open = [tree]
    #open2= [tree2] #@220618 open2とtree2を作る

    # openが空になるまで繰り返す。
    while(len(open)!=0):
        # open の先頭を取り出す。

        n = open.pop(0)

        #n2 = open2.pop(0)

        # 親子関係のデータをすべてループする。
        for pc in rel_data:
        #for pc in rdata:


            # 親データと調査対象データが一致する場合
            if pc[0]==n[0]:


                # ツリーデータを作成して、調査対象のツリーの子ノードとして追加する。

                #w = [pc[1]]  #@220618 ともかく子供のリストを作る


                m = [pc[1],[]]
                n[1].append(m)


                #print('n',n)

                tier_list = copy.deepcopy( n )


                tier_list[0] = [ 0, n[0] ]


                n1_list = n[1]

                #print('tier_list_0',tier_list)

                #print('n1_list',n1_list)

                work_list = [tier_list[0]] + n1_list


                ####work_list = tier_list + n1_list


                #print('work_list',work_list)

                
                for i, x in enumerate(n1_list):

                    j = i + 1

                    work_list[j] = [ j, x[0] ]


                #print('tier_list',tier_list)

                #print('work_list',work_list)
 
                        


                # さらに発見された子ノードを、これから調査をする対象としてopenに登録する。
                open.append(m)

                #print('open',open)

                pass


            pass

        ####print('work_list_end =',work_list)

        if w[-1] != work_list :

            w.append(work_list)

        pass

    z = w.pop(0)

    #print('w =',w)
    #print('z',z)

    return tree, w


# ツリー構造の表示関数
def tstr(node,indent=""):

    s = indent+str(node[0])+"\n"

    for c in node[1]:              # 子ノードでループ
        s += tstr(c,indent+"+-")
        pass
    return s

## 歴代将軍の配列
#
#shogun = [ 'JPN'  ]
#
## shogun = [ "家康","秀忠","家光","家綱","綱吉","家宣","家継", "吉宗","家重","家治","家斉","家慶","家定","家茂","慶喜" ]
#
## 名前から何代将軍かを求める。将軍ではない場合は、空文字が返る。
#
#sno = lambda name: "" if name not in shogun else " "+ str(shogun.index(name)+1)





#tree = ['JPN',[]]  #@220629 file読み込み時にセット

tier_list = []


tree, w = tree_generator(tree,parent_childs,tier_list)

## 220617 test
#print(tree)

print(tstr(tree))

# ********************************************************************


# w = [[[0, 'JPN'], [1, 'YTO'], [2, 'NYC'], [3, 'LAX'], [4, 'MEX'], [5, 'SAO'], [6, 'BUE'], [7, 'KUL'], [8, 'BKK'], [9, 'SIN'], [10, 'SGN'], [11, 'IST'], [12, 'JKT'], [13, 'SEL'], [14, 'SYD'], [15, 'DEL'], [16, 'RUH'], [17, 'GOT'], [18, 'LON'], [19, 'PAR'], [20, 'HAM'], [21, 'MXP'], [22, 'JNB'], [23, 'SHA'], [24, 'CAN'], [25, 'LED']],,,,]


L = 0
H0 = 0
H1 = 0

ax = []
bx = []

for i,a in enumerate(w):

    H0 = H1

    #print('H0',H0)

    for j, b in enumerate(a):

        L = len(b)


        if j == 0 :

            bx.append(b)

            continue

        else:

            H1 = H0 + j

            #print('b',b)
            #print('H1',H1)

            b[0] = H1

            #print('b',b)


            bx.append(b)

    #print('bx',bx)

    ax.append(bx)

    bx = []

print('ax =',ax)


# *********************************************************************

# make_breadth_first_search.py

# ax = [[[0, 'JPN'], [1, 'YTO'], [2, 'NYC'], [3, 'LAX'], [4, 'MEX'], [5, 'SAO'], [6, 'BUE'], [7, 'KUL'], [8, 'BKK'], [9, 'SIN'], [10, 'SGN'], [11, 'IST'], [12, 'JKT'], [13, 'SEL'], [14, 'SYD'], [15, 'DEL'], [16, 'RUH'], [17, 'GOT'], [18, 'LON'], [19, 'PAR'], [20, 'HAM'], [21, 'MXP'], [22, 'JNB'], [23, 'SHA'], [24, 'CAN'], [25, 'LED']], [[0, 'YTO'], [26, 'YTOLEAF']], [[0, 'NYC'], [27, 'NYC_N'], [28, 'NYC_D'], [29, 'NYC_I']], ,,,]


tree = []

#seq_list = ['JPN'] #@220629 file読み込み時にセット

bfs_list = []

child = []


def make_seq_list(ax):

    for x in ax:

        for y in x:

            if y[0] == 0 :

                continue

            else:

                seq_list.append(y[1])

    #print('seq_list =',seq_list)

    return seq_list





def search_child(ax,node):

    child = []

    for x in ax:

        for y in x:

            if y[0] == 0 and y[1] == node:

                x_child = x[1:]

                for c in x_child:

                    child.append(c[0])

                #print('child',child)

                break

            pass

        pass

    return child


def search_node_set_child(ax,seq_list,bf_list):

    for s in seq_list:

        #print('s',s)

        child = search_child(ax,s)



        bfs_list.append(child)

    return bfs_list


            


bf_list = []


seq_list = make_seq_list(ax)

#tree_dic = make_dic(ax)

print('seq_list =',seq_list)


bf_tree_list = search_node_set_child(ax,seq_list,bf_list)

print('bf_tree =',bf_tree_list)

# *****************************************************************:

#深さ優先探索２：帰りがけ順
#"""

#tree = [[1,2,3], [4], [5,6,7], [8,9], [10], [11,12], [13,14], [], [], [], [], [], [], [], []]


#seq_list = ['JPN', 'YTO', 'NYC', 'LAX', 'MEX', 'SAO', 'BUE', 'KUL', 'BKK', ,,]


tree = bf_tree_list

postorder = []

postorder_name = []

#print('tree = ',tree)

def search(pos):

    for i in tree[pos]:        #配下のノードを調べる

        search(i)              #再帰的に探索

    #print(pos, end = ' ')      #配下のノードを調べた後に出力

    postorder.append(pos)

    return postorder

p_order = search(0)

print('p_order',p_order)




def get_node_name(node_no_list,name_seq_list):

    node_name = []

    for pos in node_no_list:
    #for pos in p_order:

        node_name.append(name_seq_list[pos])
        #postorder_name.append(name_seq_list[pos])

    #print('node_name',node_name)
    #print('postorder_name',postorder_name)

    return node_name



node_name = get_node_name(p_order,seq_list)

print('post order node_name',node_name)


# make_leaf.py
#
# 1) bf_tree幅優先treeの空リスト[]のpositionでleafの位置を判定する
# 2) seq_listを使って、leafのnode_nameをappendして生成する


def find_leaf_pos(bf_tree):

    leaf_pos = []

    print('bf_tree =',bf_tree)

    for i, node in enumerate(bf_tree):

        if node == []:

            leaf_pos.append(i)

    print('end leaf check')

    return leaf_pos


leaf_pos_list = []

leaf_pos_list = find_leaf_pos(bf_tree_list)

print('leaf_pos_list',leaf_pos_list)




leaf_node_name = get_node_name(leaf_pos_list,seq_list)

print('leaf_node_name',leaf_node_name)


# node_name
#### post order node_name ['TKO_L', 'TKO', 'OSA_L', 'OSA', 'BRU_L', 'BRU', 'HEL_L', 'HEL', 'AMS_L', 'AMS', 'AKL_L', 'AKL', 'WAW_L', 'WAW', 'LIS_L', 'LIS', 'MAD_L', 'MAD', 'ZRH_L', 'ZRH', 'YTOLEAF', 'YTO', 'NYC_N', 'NYC_D', 'NYC_I', 'NYC', 'LAX_N', 'LAX_D', 'LAX_I', 'SFOLEAF', 'LAX', 'MEXLEAF', 'MEX', 'SAOLEAF', 'SAO', 'BUELEAF', 'BUE', 'KULLEAF', 'KUL', 'BKKLEAF', 'BKK', 'SINLEAF', 'SIN', 'SGNLEAF', 'SGN', 'ISTLEAF', 'IST', 'JKTLEAF', 'JKT', 'SELLEAF', 'SEL', 'SYDLEAF', 'SYD', 'DELLEAF', 'DEL', 'RUHLEAF', 'RUH', 'SWELEAF', 'DENLEAF', 'NORLEAF', 'GOT', 'LONLEAF', 'LON', 'PARLEAF', 'PAR', 'HAM_L', 'FRALEAF', 'FRA', 'MUCLEAF', 'MUC', 'HAM', 'MXPLEAF', 'MXP', 'JNBLEAF', 'JNB', 'SHA_N', 'SHA_D', 'SHA_I', 'BJS_N', 'BJS_D', 'BJS_I', 'SHA', 'CAN_N', 'CAN_D', 'CAN_I', 'CAN', 'LEDLEAF', 'LED', 'JPN']

# leaf_node_name
#### leaf_node_name ['TKO_L', 'OSA_L', 'BRU_L', 'HEL_L', 'AMS_L', 'AKL_L', 'WAW_L', 'LIS_L', 'MAD_L', 'ZRH_L', 'YTOLEAF', 'NYC_N', 'NYC_D', 'NYC_I', 'LAX_N', 'LAX_D', 'LAX_I', 'SFOLEAF', 'MEXLEAF', 'SAOLEAF', 'BUELEAF', 'KULLEAF', 'BKKLEAF', 'SINLEAF', 'SGNLEAF', 'ISTLEAF', 'JKTLEAF', 'SELLEAF', 'SYDLEAF', 'DELLEAF', 'RUHLEAF', 'SWELEAF', 'DENLEAF', 'NORLEAF', 'LONLEAF', 'PARLEAF', 'HAM_L', 'MXPLEAF', 'JNBLEAF', 'SHA_N', 'SHA_D', 'SHA_I', 'BJS_N', 'BJS_D', 'BJS_I', 'CAN_N', 'CAN_D', 'CAN_I', 'LEDLEAF', 'FRALEAF', 'MUCLEAF']

# ***********************************
# is_leaf node
# ***********************************
def is_leaf(node):

    if node in leaf_node_name:

        return True

    else:

        return False


## ***********************************
## is_leaf node
## ***********************************
#
#for node in node_name:  #### SCM tree nodes are postordering 
#
#    if is_leaf(node):
#
#        print('leaf node',node)
#
#        PySI(node, 'LEAF')
#
#    else:              #### root node処理が必要な場合はelif is_root分岐
#
#        print('mid or root node',node)
#
#        PySI(node, 'NOLEAF')

