# coding: utf-8
#
#
#            Copyright (C) 2020 Yasushi Ohsugi
#            Copyright (C) 2021 Yasushi Ohsugi
#            Copyright (C) 2022 Yasushi Ohsugi


# ******************************
# make_active_week_dic
# ******************************
#active_week_dic =i_PlanSpace.make_active_week_dic(active_week_list)

def make_active_week_dic(active_week_list):

# ******************************
# 一年間のactive_week(=船便の着荷受入週など)を設定する。
# ******************************

#Bi-Weekly 1&3 BACKWARD
#active_week_no_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]

#Bi-Weekly 1&3 BACKWARD
#active_week_no_list = [1,3,5,7,9,11,14,16,17,20,22,24,27,29,31,33,35,37,40,42,44,46,48,50]

#1 time a month 1st
#active_week_no_list = [1,5,9,14,17,22,27,31,35,40,44,48]


    active_week_dic = {} # active_week_dicの辞書型の宣言

    week_no_cal_pos = 0 # actuve_week[1,2,3,4,5]のposを作る[0,1,2,3,4]

    for i in range(1,13):
        active_week_dic[i] = [] # 12ヶ月分の空リストを初期化


    for W in active_week_list:

    # Wはweek_no_yearなので、month_no,week_noに変換
        month_no_cal, week_no_cal = year2month_week(W)

# *******************************
# week_no to week_pos 
# *******************************
        week_no_cal_pos = week_no_cal - 1  

        active_week_dic[month_no_cal].append( week_no_cal_pos )

    #print('active_week_dic',active_week_dic)

    return active_week_dic


                ##active_week_no_list = [1,3,5,7,9,11,14,16,17,20,22,24,27,29,31,33,35,37,40,42,44,46,48,50]

                #辞書型で、{month_no,[week_list,,,]}のデータを持たせる

                #active_week = []
                #active_week = active_week_dic(month_no)


def show_lot_space_M( lot_space ):
    #print( 'showing LotSpace M' )
    for W, W_list in enumerate(lot_space):
        print('week',W, W_list )


def show_lot_space_Y( lot_space ):
    #print( 'showing LotSpace Y' )
    for W, W_list in enumerate(lot_space):
        print('Week',W, W_list )


def act_inact_convert( active_week_list ) :

    inactive_week_list = []

    for i in [0,1,2,3,4]:

        if i in active_week_list:

            continue

        else:

            inactive_week_list.append(i)

    return inactive_week_list

# ******************************
# 年週=>月&月週の変換ライブラリ　year2month_week使用
# ******************************
def year2month_week( week_no_year ):

    MW2W_list = [[ 1 , 1 , 1 ],[ 1 , 2 , 2 ],[ 1 , 3 , 3 ],[ 1 , 4 , 4 ],[ 2 , 1 , 5 ],[ 2 , 2 , 6 ],[ 2 , 3 , 7 ],[ 2 , 4 , 8 ],[ 3 , 1 , 9 ],[ 3 , 2 , 10 ],[ 3 , 3 , 11 ],[ 3 , 4 , 12 ],[ 3 , 5 , 13 ],[ 4 , 1 , 14 ],[ 4 , 2 , 15 ],[ 4 , 3 , 16 ],[ 4 , 4 , 17 ],[ 5 , 1 , 18 ],[ 5 , 2 , 19 ],[ 5 , 3 , 20 ],[ 5 , 4 , 21 ],[ 6 , 1 , 22 ],[ 6 , 2 , 23 ],[ 6 , 3 , 24 ],[ 6 , 4 , 25 ],[ 6 , 5 , 26 ],[ 7 , 1 , 27 ],[ 7 , 2 , 28 ],[ 7 , 3 , 29 ],[ 7 , 4 , 30 ],[ 8 , 1 , 31 ],[ 8 , 2 , 32 ],[ 8 , 3 , 33 ],[ 8 , 4 , 34 ],[ 9 , 1 , 35 ],[ 9 , 2 , 36 ],[ 9 , 3 , 37 ],[ 9 , 4 , 38 ],[ 9 , 5 , 39 ],[ 10 , 1 , 40 ],[ 10 , 2 , 41 ],[ 10 , 3 , 42 ],[ 10 , 4 , 43 ],[ 11 , 1 , 44 ],[ 11 , 2 , 45 ],[ 11 , 3 , 46 ],[ 11 , 4 , 47 ],[ 12 , 1 , 48 ],[ 12 , 2 , 49 ],[ 12 , 3 , 50 ],[ 12 , 4 , 51 ],[ 12 , 5 , 52 ]]

    month           = 0
    week_no_month   = 0

    A_list = [0,0,0]

    #print('week_no_year', week_no_year )

    for i, A_list in enumerate(MW2W_list):
        #print('i & A_list', i , A_list )

        if A_list[2]  == week_no_year:


                month         = A_list[0]
                week_no_month = A_list[1]

                #print('M&W',month,week_no_month)
    return( month , week_no_month )


# ******************************
# 月週から年週への変換 ※53週の例外外処理がないので要注意@211005
# ******************************
def month2year_week( month , week_no ):

    MW2Y_list = [[ 1 , 1 , 1 ],[ 1 , 2 , 2 ],[ 1 , 3 , 3 ],[ 1 , 4 , 4 ],[ 2 , 1 , 5 ],[ 2 , 2 , 6 ],[ 2 , 3 , 7 ],[ 2 , 4 , 8 ],[ 3 , 1 , 9 ],[ 3 , 2 , 10 ],[ 3 , 3 , 11 ],[ 3 , 4 , 12 ],[ 3 , 5 , 13 ],[ 4 , 1 , 14 ],[ 4 , 2 , 15 ],[ 4 , 3 , 16 ],[ 4 , 4 , 17 ],[ 5 , 1 , 18 ],[ 5 , 2 , 19 ],[ 5 , 3 , 20 ],[ 5 , 4 , 21 ],[ 6 , 1 , 22 ],[ 6 , 2 , 23 ],[ 6 , 3 , 24 ],[ 6 , 4 , 25 ],[ 6 , 5 , 26 ],[ 7 , 1 , 27 ],[ 7 , 2 , 28 ],[ 7 , 3 , 29 ],[ 7 , 4 , 30 ],[ 8 , 1 , 31 ],[ 8 , 2 , 32 ],[ 8 , 3 , 33 ],[ 8 , 4 , 34 ],[ 9 , 1 , 35 ],[ 9 , 2 , 36 ],[ 9 , 3 , 37 ],[ 9 , 4 , 38 ],[ 9 , 5 , 39 ],[ 10 , 1 , 40 ],[ 10 , 2 , 41 ],[ 10 , 3 , 42 ],[ 10 , 4 , 43 ],[ 11 , 1 , 44 ],[ 11 , 2 , 45 ],[ 11 , 3 , 46 ],[ 11 , 4 , 47 ],[ 12 , 1 , 48 ],[ 12 , 2 , 49 ],[ 12 , 3 , 50 ],[ 12 , 4 , 51 ],[ 12 , 5 , 52 ]]

    #@ 入口をweek_noに変更#@211108
    #@ week_no = week_pos + 1 #@211105 二か所目の同じ週ズレ補正#@211107

    A_list = [0,0,0]

    for i, A_list in enumerate(MW2Y_list):

        # print('A_list',A_list)

        if A_list[0]  == month: # 抽出したリストの第一要素(=月)が1,2,3,月ならば

            # print('A_list',A_list)

            if A_list[1] == week_no: # 月内の第N週は、年週にすると何か?
            
                #print( 'month2year_week A_list', A_list, A_list[2] )

                week_no_Y = A_list[2]

                return(week_no_Y)


# ******************************
# month2week code ある月が何週あるか?4-4-5の判定
# ******************************
def month2week( month_no ):

    w_m_y_list = [[1,4, 1],[2,4, 5],[3,5, 9],[ 4,4,14],[ 5,4,18],[ 6,5,22],                       [7,4,27],[8,4,31],[9,5,35],[10,4,40],[11,4,44],[12,5,48]]

    work_list = w_m_y_list[ month_no - 1 ]

    week_no_month = work_list[1]

    return(week_no_month)



