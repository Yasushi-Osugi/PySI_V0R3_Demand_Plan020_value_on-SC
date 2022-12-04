# coding: utf-8
#
#
#            Copyright (C) 2020 Yasushi Ohsugi
#            Copyright (C) 2021 Yasushi Ohsugi
#            Copyright (C) 2022 Yasushi Ohsugi
#
#
from PySILib.PySI_library_V0R1_070 import *



# ******************************
# class PlanEnv
# ******************************
class PlanEnv:

    def __init__(self):

        # place_lotするスタート位置(week_no_year=1,step=0)の初期化
        self.plan_pos = 0


# ******************************
# ML main process 
# 1:doing action  2:updating plan status  3:evaluating plan & return reward
# ******************************
    def act_state_eval(self, next_action, month_no, i_PlanSpace, i_LotSpace, episode):


# ******************************
# ACTION place_lotして計画の状態を更新　lot_counts経由でPを更新し、PSIを再計算
# ******************************
        next_state = self.place_lot2next_pos(next_action, month_no, i_PlanSpace, i_LotSpace)


# ******************************
# 計画の状態を更新する。Pをlot_spaceから更新してから、PSIを再計算。
# ******************************
        i_PlanSpace.CalcPlanSIP() #@211019 copied_から => i_PlanSpace


# ******************************
# 計画の状態を評価する。ココでget_valueの結果rewardとvalueを返している
# ******************************

        reward , value           = i_PlanSpace.EvalPlanSIP() #@211019@221123
        #reward                  = i_PlanSpace.EvalPlanSIP() #@211019 


# ******************************
# rewardとvalueをi_PlanSpaceにセット
# ******************************
        i_PlanSpace.reward            = reward    #@221123 他でも使われる???
        i_PlanSpace.value             = value


#
#@221123 i_PlanSpace.lot_valueは、"reward"の差分ではなく、"profit"の差分とする
#        "reward"には、profit/revenue/profit_ratioの3パターンがあるが、
#        i_PlanSpace.lot_valueはprofitから生成される
#
# ******************************
# 計画の状態を評価する。ココでget_valueの結果valueを返している
# ******************************
#
#@220927 'value'計算の試行　ここはtry&errorの途中で、
#        C-P-Uへの書出すタイミング lot_noの付番と同時に? その時のvalueを書出す?
#
        #@220927 'value' (= value_delta)は、place_lotされたLOT一つ分の価値計算

        i_PlanSpace.value_delta = i_PlanSpace.value - i_PlanSpace.value_prev

        i_PlanSpace.lot_value    = i_PlanSpace.value_delta

        i_PlanSpace.value_prev  = i_PlanSpace.value    # _prev前に退避する


#
#@221009@221123 'lot_value'計算の確認　PlanLotでC-P-Uに書き出し
#        C-P-Uへの書出すタイミングでlot_valueを書出す
#        lot_value = i_PlanSpace.value_delta

        ####print('lot_value', i_PlanSpace.value_delta, " = ", i_PlanSpace.value, " - ", i_PlanSpace.value_prev )


## ******************************
## 計画の状態を評価する。ココでget_valueの結果rewardを返している
## ******************************
#        i_PlanSpace.reward             = reward
#
#
##
##@221123 i_PlanSpace.lot_valueは、"reward"の差分ではなく、"profit"の差分とする
##        "reward"には、profit/revenue/profit_ratioの3パターンがあるが、
##        i_PlanSpace.lot_valueはprofitから生成される
##
## ******************************
## 計画の状態を評価する。ココでget_valueの結果rewardを返している
## ******************************
##
##@220927 'value'計算の試行　ここはtry&errorの途中で、
##        C-P-Uへの書出すタイミング lot_noの付番と同時に? その時のvalueを書出す?#
##
#        #@220927 'value' (= reward_delta)は、place_lotされたLOT一つ分の価値計算#
#
#        i_PlanSpace.reward_delta = i_PlanSpace.reward - i_PlanSpace.reward_prev#
#
#        i_PlanSpace.lot_value    = i_PlanSpace.reward_delta
#
#        i_PlanSpace.reward_prev  = i_PlanSpace.reward    # _prev前に退避する
#
#
##
##@221009 'lot_value'計算の確認　PlanLotでC-P-Uに書き出し
##        C-P-Uへの書出すタイミングでlot_valueを書出す
##        lot_value = i_PlanSpace.reward_delta
#
#        print('lot_value', i_PlanSpace.reward_delta, " = ", i_PlanSpace.reward, " - ", i_PlanSpace.reward_prev )
#


# ******************************
# animation用に計画の状態をcsv fileに書き出す
# ******************************
        #if episode ==  0 : #
        #if episode ==  1 : #
        #if episode ==  2 : #
        #if episode == 50 : #

        if episode == 9 :

            i_PlanSpace.write_csv4animation(month_no,reward)#@220304


# ******************************
# check end condition
# ******************************
        monthly_episode_end_flag = self.monthly_episode_end_flag(i_PlanSpace, month_no) 

        return next_state, reward, monthly_episode_end_flag


# ******************************
# place_lot2next_pos
# ******************************
    def place_lot2next_pos(self,next_action, month_no, i_PlanSpace, i_LotSpace):
        # position(x,y)が決まる。

        plan_x, plan_y = self.state_num2xy(self.plan_pos)  

        week_pos = next_action # Q学習のactionは、0,1,2,3,4のLotSpace週の選択

# ******************************
# W1,2,3,4,5の選択から位置(x,y)を特定する処理  < LotSpaceの世界において >
# ******************************
        week_no = week_pos + 1

        week_no_year = month2year_week( month_no , week_no )


# *****************************
# place_lot()
# *****************************

        lot_step = i_LotSpace.place_lot_action( i_PlanSpace.lot_no , week_no )


# ******************************
# place_lotからlot_countsを経由し、Pを生成して、PSIにPをセット
# ******************************
# place_lotの後、action = [lot_no, r_week_pos, r_lot_step]を生成
# 月次の週=week_pos を年次の週番号に変換し、
# P = lot_counts x planning_lot_sizeでPを生成

# memo
# lot_pos = [lot_no, week_no, lot_step]


#@221009 lot_valueをこの辺りでセットする。
#        (案1) lot_valueも、xxx.xxなどの浮動小数をformatで文字形式で保管する?
#        (案2) 

        # 年間の週番号を判定　　2月の第３週は年間の第7週
        week_no_year = month2year_week( month_no , week_no )

        # 年間のロット通し番号 lot_seq_year = concatenate(month_no,lot_no)生成
        # 年次lot_space_Yの「該当週」の「積上げ位置」に配置する

        month_no_form = format( month_no , '02' )             # 月は2桁
        lot_no_form   = format( i_PlanSpace.lot_no   , '03' ) # ロット番号は3桁

        # 年間ロット通し番号は5桁
        # "05012" 文字列　5月ロット番号=12
        lot_seq_year  = month_no_form + lot_no_form 

        # ******************************
        # ここでlot_space_Yにセット appendで直接　追加
        # ******************************
        w_n_y = int(week_no_year or 0)

        i_LotSpace.lot_space_Y[w_n_y].append( lot_seq_year )
        #@221009
        i_LotSpace.lot_space_Y_value[w_n_y].append( i_PlanSpace.lot_value ) 

        # ******************************
        # lot_stepはlistの要素数-1
        # ******************************
        lot_Y_len = len( i_LotSpace.lot_space_Y[w_n_y] )

        lot_Y_step = lot_Y_len - 1

        if lot_step == lot_Y_step:  # MonthとYearの整合確認
            #print(" lot_space_M and _Y are consistent")
            pass
        else:
            print(" lot_space_M and _Y are NOT consistent")


# ******************************
# i_PlanSpace.lot_countsに"lot_step + 1"で計算されるロット数をセットする。
# ******************************
        i_PlanSpace.lot_counts[week_no_year] = lot_step + 1


# ******************************
# 発注数 = ロット数 * ロットサイズ
# P_year[ W ] = lot_counts[ W ] * planning_lot_size
# ******************************
        i_PlanSpace.update_P_year_lot_counts()


# ******************************
# 更新した計画状態をユニークに示す座標(x,y)
# ******************************
        plan_x = week_no_year
        plan_y = lot_step

        self.plan_pos = self.state_xy2num( plan_x, plan_y )

        return self.plan_pos


# ******************************
# check end condition
# ******************************
    def monthly_episode_end_flag(self, i_PlanSpace, month_no):

# PlanSpaceのPとSの総数を比較する

# ******************************
# 月間のPとSの総数
# ******************************
#       month_week_list = [[1,2,3,4],[5,6,7,8],[9,10,11,12,13],
#           [14,15,16,17],[18,19,20,21],[22,23,24,25,26],
#           [27,28,29,30],[31,32,33,34],[35,36,37,38,39],
#           [40,41,42,43],[44,45,46,47],[48,49,50,51,52]]
#
#
#       M_W_list = month_week_list[month_no] # 4月なら[14,15,16,17]というリスト
#
#       S_month = 0
#       P_month = 0
#
#       for W in M_W_list:  # 4月なら[14,15,16,17]の各週を発生させて4月分を集計
#
#           S_month += i_PlanSpace.S_year[W]
#           P_month += i_PlanSpace.P_year[W]


# ******************************
# 月末までのPとSの累計で判定する
# ******************************
        month_end_week_list = [4,8,13,17,21,26,30,34,39,43,47,52]

        M_end_week = month_end_week_list[month_no-1] # 4月なら17というリスト

        S_accume = 0
        P_accume = 0


        ### W0から累計を計算する
        #
        for W in range(0, M_end_week+1 ):  # 4月なら0週～17週までの累計

            S_accume += i_PlanSpace.S_year[W]
            P_accume += i_PlanSpace.P_year[W]


# ******************************
# 年間のPとSの総数
# ******************************
        S_total         = sum(i_PlanSpace.S_year)     # S総数
        S_month_average = S_total/12                  # S月平均
        S_day_average   = S_month_average/28          # S日平均 @211204=28Days


# ******************************
# 余裕率の案-1
# ******************************
#        days = 0.5                                         # 安全在庫日数
#        #days = 10                                         # 安全在庫日数
#
#        S_accume_sfaty = S_accume + S_day_average * days
#
#        print('P_accume & S_accume_sfaty',P_accume,S_accume_sfaty)
#
#        if P_accume  >= S_accume_sfaty :  # P > S + 安全在庫
#            return True
#        else:
#            return False


# ******************************
# check_off_week_forward 例
# 当月と次月にoff_weekがある時、off_weekの需要 * 1/2を前倒しで供給
# 当月と次月にoff_weekがある時、off_weekの需要 * 1.5を前倒しで供給
# ******************************

# ******************************
# OFF_weekの先行状態を判定して、forward loading処理する $$$$$$$$
# ******************************

        off_week = 0

        for off_week in i_PlanSpace.off_week_no_year_list:

            off_month , off_week_no_month = year2month_week( off_week )

            if month_no == off_month:       ###当月に長期休暇がある

                forward_flag = True

            elif month_no+1 == off_month:   ###翌月に長期休暇がある

                forward_flag = True

            else:
                forward_flag = False

        forward_stok = 0

        # ******************************
        # 長期休暇のoff週の先行在庫の高さを指定する
        # ******************************
        if forward_flag == True:

            forward_stok = i_PlanSpace.S_year[off_week] * 1

            #forward_stok = i_PlanSpace.S_year[off_week] * 2
            #forward_stok = i_PlanSpace.S_year[off_week] * 1.5
            #forward_stok = i_PlanSpace.S_year[off_week] / 2 
            

# ******************************
# 流通チャネルの在庫方針　end条件　=> 安全在庫なし& off週の先読みは残す
# ******************************
#
#        if P_accume  >= S_accume :  # forward stock無し
#
#        #if P_accume  >= S_accume + forward_stok:
#
#            return True


# ******************************
# 一般的な在庫方針　end条件　=> 安全在庫あり& off週の先読みは残す
# ******************************

        # ******************************
        # P_acc > S_acc + 安全在庫
        # ******************************
        # memo 安全在庫 i_PlanSpace.SS_days
        #
        #S_accume_sfaty = S_accume + S_day_average * i_PlanSpace.SS_days
        #
        #print('P_accume & S_accume_sfaty',P_accume,S_accume_sfaty)
        #
        #if P_accume  >= S_accume_sfaty :  # P > S + 安全在庫

        # ******************************
        # P_acc > S_acc ＋前倒し
        # ******************************
        # memo 翌月に非稼働週off_weekがある時、その需要S分をforward_stokする
        #if P_accume  >= S_accume :  # forward_stock無し
        #if P_accume  >= S_accume + forward_stok:# 5日

        # ******************************
        # P_acc > S_acc + 安全在庫 ＋前倒し
        # ******************************
        # memo 安全在庫 i_PlanSpace.SS_days
        #
        #S_accume_sfaty = S_accume + S_day_average * i_PlanSpace.SS_days
        #
        #if P_accume  >= S_accume_sfaty + forward_stok: 
        #
        #    return True


# ******************************
# 余裕率の案-2 時間の経過とともに、月毎の安全在庫日数を絞り込む
# ******************************
        if   month_no <= 6 :                  # 1<= month_no <= 6

            DAYS = 10
            #DAYS = 20

            if P_accume  >= S_accume+ S_day_average*DAYS + forward_stok:# 20日
                return True
            else:
                return False

        elif month_no <= 11 :                  # 7 <= month_no <= 11

            DAYS = 5
            #DAYS = 10

            if P_accume  >= S_accume + S_day_average*DAYS + forward_stok: # 10日
                return True
            else:
                return False


# ******************************
# 10月～12月は期間内ではなく、計画された年間P総量 > 年内の総需要で判定
# ******************************
#        else:                                 # 10 <= month_no <= 12
#
#            DAYS = 1
#
#            if P_accume  >= S_accume + S_day_average*DAYS + forward_stok: # 1日#
#
#                return True
#            else:
#                return False

        # ******************************
        # 計画されたP総量 > 年内の総需要 で判定する
        # ******************************
        else:

            S_accume_year = 0
            P_accume_year = 0


            ### W0からW52まで累計を計算する

            for W in range(0, 52+1 ):         # 0週～52週までの累計

            #for W in range(0, M_end_week+1 ):  # 4月なら1週～17週までの累計
            #for W in range(1, M_end_week+1 ):  # 4月なら1週～17週までの累計

                S_accume_year += i_PlanSpace.S_year[W]
                P_accume_year += i_PlanSpace.P_year[W]

            # ******************************
            # 年間のPとSの総数
            # ******************************
            #
            # S_total         = sum(i_PlanSpace.S_year)# S総数
            # S_month_average = S_total/12             # S月平均
            # S_day_average   = S_month_average/28     # S日平均 @211204=28Days
            #
            ##P_total    = sum(i_PlanSpace.P_year)     # P総数


# ******************************
# 年内の総需給の案-1
# ******************************
#        days = 0.5                                         # 安全在庫日数
#        #days = 10                                         # 安全在庫日数
#
#        S_accume_sfaty = S_accume + S_day_average * DAYS


            if P_accume_year  >= S_accume_year :  # 総P >= 総S
                return True
            else:
                return False


# ******************************
# 余裕率の案-2    <<<マザープラント用のPSI試行版>>>
# ******************************
#
#        if   month_no <= 6 :                  # 1<= month_no <= 6
#
#            DAYS = 1     
#            #DAYS = 10
#            #DAYS = 20
#
#            # ******************************
#            # + S_day_average*DAYSを外す。マザープラントの年間Sは大きい
#            # ******************************
#            if P_accume  >= S_accume + forward_stok:# 5日
#
#                return True
#            else:
#                return False
#
#        elif month_no <= 9 :                  # 7 <= month_no <= 9
#            DAYS = 1
#
#            if P_accume  >= S_accume + S_day_average*DAYS + forward_stok:# 1日
#                return True
#            else:
#                return False
#
#        else :                                # 10 <= month_no <= 12
#            DAYS = 1
#
#            if P_accume  >= S_accume + S_day_average*DAYS + forward_stok:# 1日
#                return True
#            else:
#                return False

# ******************************
# 余裕率の案-3 需要ピークの在庫を厚くする
# ******************************
#        if   month_no <= 6 :                  # 1<= month_no <= 6
#
#            DAYS = 10
#
#            if P_accume  >= S_accume+ S_day_average*DAYS + forward_stok:# 10日
#                return True
#            else:
#                return False
#
#        elif month_no <= 9 :                  # 7 <= month_no <= 10
#
#            DAYS = 15
#
#            if P_accume  >= S_accume + S_day_average*DAYS + forward_stok:# 15日#                return True
#            else:
#                return False
#
#        else :                                # 10 <= month_no <= 12
#
#            DAYS = 5
#
#            if P_accume  >= S_accume + S_day_average*DAYS + forward_stok:# 5日
#                return True
#            else:
#                return False



# ******************************
# lot_spaceとstate座標を初期化
# ******************************
    def reset(self, i_LotSpace):

        self.plan_pos = 0  ### state_num = 0  初期位置に戻す

        i_LotSpace.init_lot_space_M( 5 )

        return self.plan_pos


# ******************************
# ML state conversion x,y <=> num
# ******************************
    def state_xy2num(self, x , y ):  ### x=week_no_year  y=lot_step
        num = x + 54 * y
        return num


    def state_num2xy(self, num ):  ### x=week_no_year  y=lot_step
        x = num % 54
        y = num // 54
        return x, y

# ******************************
# end of class PlanEnv
# ******************************
