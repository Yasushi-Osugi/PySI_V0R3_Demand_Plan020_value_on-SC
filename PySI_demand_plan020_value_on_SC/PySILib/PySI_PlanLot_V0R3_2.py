#
# coding: utf-8
#
# PySI_PlanLot_V0R3_2.py
#
#            Copyright (C) 2020 Yasushi Ohsugi
#            Copyright (C) 2021 Yasushi Ohsugi
#            Copyright (C) 2022 Yasushi Ohsugi


# ******************************
# debug_flag の設定
# ******************************
#import debug
#flag = 0

import time  
import sys
import copy
import numpy as np
import pandas as pd
import csv
import pprint

# ******************************
# PSI計画のライブラリ
# ******************************
from PySILib.PySI_library_V0R1_070 import *


# ******************************
# PlanSpaceクラス定義
# ******************************

class PlanSpace():

    def __init__( self, plan_prof, PSI_data ):

# ******************************
# 初期化
# ******************************
        self.escape_off_week_flag = False 

        self.lot_counts   = [0 for x in range(0,55)] 

        self.profit_ratio = 0

# **************************
# initialise "lot_no"
# **************************
        self.lot_no = 0


# **************************
# initialise "lot_value" and "lot_no_value" is pair list [lot_no, lot_value]
# **************************
        self.lot_value = 0
        self.lot_no_value = [0,0]


## **************************
## initialise "value" @220928
## **************************
#        self.reward_prev            = 0 # Rのセット前に退避する
#        self.reward                 = 0 # set by Eval_calculation結果
#        self.reward_delta           = 0 # "lot_value" = R_delta = R - R_prev


# **************************
# initialise "value" @221123 value=profutとしてrewardと分離する
# **************************
        self.value_prev            = 0 # Vのセット前に退避する
        self.value                 = 0 # set by Eval_calculationの"profit"結果
        self.value_delta           = 0 # "lot_value" = V_delta = V - V_prev


# **************************
# initialise "act_week_poss" 月内の選択可能なnext_action=week_posのリスト
# **************************
        self.act_week_poss = [0,1,2,3,4]


# **************************
# BU_SC_node_profile     business_unit_supplychain_node
# **************************

## **************************
## plan_basic_parameter ***sequencing is TEMPORARY
## **************************
        self.PlanningYear           = plan_prof['plan_year']
        self.plan_engine            = plan_prof['plan_engine']
        self.reward_sw              = plan_prof['reward_sw']

# ***************************
# business unit identify
# ***************************
        self.product_name           = plan_prof['product_name']
        self.SC_tree_id             = plan_prof['SC_tree_id']
        self.node_from              = plan_prof['node_from']
        self.node_to                = plan_prof['node_to']

        self.LT_boat                = plan_prof['LT_boat']

        self.SGMC_ratio             = plan_prof['SGMC_ratio']
        self.Cash_Intrest           = plan_prof['Cash_Intrest']
        self.LOT_SIZE               = plan_prof['LOT_SIZE']
        self.REVENUE_RATIO          = plan_prof['REVENUE_RATIO']

        #print('set_plan parameter')
        #print('self.LT_boat',              self.LT_boat)
        #print('self.SGMC_ratio',           self.SGMC_ratio)
        #print('self.Cash_Intrest',         self.Cash_Intrest)
        #print('self.LOT_SIZE',             self.LOT_SIZE)
        #print('self.REVENUE_RATIO',        self.REVENUE_RATIO)

# **************************
# product_cost_profile
# **************************
        self.PO_Mng_cost            = plan_prof['PO_Mng_cost']
        self.Purchase_cost          = plan_prof['Purchase_cost']
        self.WH_COST_RATIO          = plan_prof['WH_COST_RATIO']
        self.weeks_year             = plan_prof['weeks_year']
        self.WH_COST_RATIO_aWeek    = plan_prof['WH_COST_RATIO_aWeek']

        #print('product_cost_profile parameter')
        #print('self.PO_Mng_cost',          self.PO_Mng_cost)
        #print('self.Purchase_cost',        self.Purchase_cost)
        #print('self.WH_COST_RATIO',        self.WH_COST_RATIO)
        #print('self.weeks_year',           self.weeks_year)
        #print('self.WH_COST_RATIO_aWeek',  self.WH_COST_RATIO_aWeek)


# **************************
# distribution_condition
# **************************
        self.Indivisual_Packing    = plan_prof['Indivisual_Packing']
        self.Packing_Lot           = plan_prof['Packing_Lot']
        self.Transport_Lot         = plan_prof['Transport_Lot']
        self.planning_lot_size     = plan_prof['planning_lot_size']
        self.Distriburion_Cost     = plan_prof['Distriburion_Cost']
        self.SS_days               = plan_prof['SS_days']

        #print('distribution_condition parameter')
        #print('self.Indivisual_Packing', self.Indivisual_Packing)
        #print('self.Packing_Lot',        self.Packing_Lot)
        #print('self.Transport_Lot',      self.Transport_Lot)
        #print('self.planning_lot_size',  self.planning_lot_size)
        #print('self.Distriburion_Cost',  self.Distriburion_Cost)
        #self.Packing_Lotprint('self.SS_days',            self.SS_days)


# **************************
# PSI_DB_data 
# PSI_data 
# **************************

#@#@ profileのnode名称群が l[0,1,2,3]
#        self.product_name           = plan_prof['product_name']
#        self.SC_tree_id             = plan_prof['SC_tree_id']
#        self.node_from              = plan_prof['node_from']
#        self.node_to                = plan_prof['node_to']

        #PSI_data_slice = PSI_data[:6]
        #PSI_data_slice = PSI_data[:5]

        # 0:"index" + 1:"year"を除く
        

        ####print('PSI_data',PSI_data)
        #print('PSI_data_slice',PSI_data_slice)

        for l in PSI_data:
#        #for l in PSI_data_slice:
#
#
#            print('l in PSI_data', l )


# ******************************
# 前年PSI-W53を当年PSI-W0にcopyしているので、W0活き ゼロクリアしない@221003
# ******************************
            if      l[4]     == "1S":
                self.S_year  =  l[5:]

            elif    l[4]     == "2CO":
                self.CO_year =  l[5:]

            elif    l[4]     == "3I":
                self.I_year  =  l[5:]

            elif    l[4]     == "4P":
                self.P_year  =  l[5:]

            elif    l[4]     == "5IP":
                self.IP_year =  l[5:]

# *********************************************
            else:
                print('error:PSI_data unkown data without S-CO-I-P-IP',l)


        #print('set_SIP_plan_data')
        #print(self.S_year,self.CO_year, self.I_year, self.P_year, self.IP_year)

# **************************
# S 4-4-5 month data 
# **************************

        self.S445_month = [0,0,0,0,0,0,0,0,0,0,0,0,0] #要素13 12か月


# ******************************
# S_year 54週　確保
# ******************************
        len_S = len( self.S_year ) 

        if len_S < 54 :

            for i in range(len_S, 55):

                self.S_year[i] = 0

        #S_year[i]の値を4-4-5でスライスしたリストをセット
        self.S445_month[1] = self.S_year[1:5]  # S_year=[W0,W1,W2,,,,,W52,W53] 
        self.S445_month[2] = self.S_year[5:9]
        self.S445_month[3] = self.S_year[9:14]

        for j in range(1,4): # 1四半期　4四半期　13ヶ月増分
            self.S445_month[1+j*3] = self.S_year[1+j*13:5+j*13]
            self.S445_month[2+j*3] = self.S_year[5+j*13:9+j*13]
            self.S445_month[3+j*3] = self.S_year[9+j*13:14+j*13]


# ******************************
# calendar_cycle_week_list生成
# ******************************

        calendar_cycle_week_list = []  
        calendar_cycle_w_list    = []  

#### 年週をprofileから読込み[4,8,13,17,21,26,30,34,39,43,47,52]

# ******************************
# profileからoff_weekを読み込み
# ******************************
        calendar_cycle_week_list = plan_prof['calendar_cycle_week']

        string                   = calendar_cycle_week_list
        calendar_cycle_w_list    = string.split(',')

        #string='x,y,z'
        #output=string.split(',')

        #print('calendar_cycle_w_list',calendar_cycle_w_list)

        for i in range(len(calendar_cycle_w_list)):
            calendar_cycle_w_list[i] = int(calendar_cycle_w_list[i])

        self.calendar_cycle_week_list = calendar_cycle_w_list


# ******************************
# off_flag生成
# ******************************
        off_week_no_year_list = []  ### 年週をprofileから読み込み[18,23]
        off_week_list         = []

        self.off_flag         = []

# ******************************
# profileからoff_weekを読み込み
# ******************************
        off_week_no_year_list     = plan_prof['calendar_off_week']

        string     = off_week_no_year_list
        off_w_list = string.split(',')

        #string='x,y,z'
        #output=string.split(',')

        #print('off_w_list',off_w_list)

        for i in range(len(off_w_list)):
            off_w_list[i] = int(off_w_list[i])

        self.off_week_no_year_list = off_w_list

        #print('PlanLot:off_week: list',self.off_week_no_year_list)


# off週の需要を前倒しして、バランスさせるために
# off_flag = [ 週(=i), "OFF", S_year[i], off_month_num, off_week_num ]を作成。
#
# off週が、何月の第何週かを判定している
# off週が4-4-5のどこの月にいるか
# i_PlanSpace.off_flag [[18, 'OFF', 150, 4, 4], [32, 'OFF', 250, 8, 1]]


# ******************************
# off_flag generation
# ******************************

        for w_str in off_w_list:
        #for off_w in off_week_no_year_list:

            off_w = int(w_str)

            off_month_num, off_week_num = year2month_week( off_w )

            #print('off_week_no_year_list',off_week_no_year_list)
            #print('off_w',off_w)

            S_off_w = self.S_year[off_w] 

            self.off_flag.append([ off_w , "OFF", S_off_w , off_month_num, off_week_num ] )

            off_week_list.append([ off_w - 1, self.S_year[off_w] ])


# ******************************
# evaluation data initialise rewardsを計算の初期化
# ******************************

# ******************************
# Profit_Ratio #float
# ******************************
        self.profit_ratio   = Profit_Ratio = 0.6

# ******************************
# set_EVAL_cash_in_data #list for 54 weeks ### 計算時のi+1で55まで必要になる
# *******************************
        self.Profit        = Profit       = [ 0 for i in range(55)]
        self.Week_Intrest  = Week_Intrest = [ 0 for i in range(55)]
        self.Cash_In       = Cash_In      = [ 0 for i in range(55)]
        self.Shipped_LOT   = Shipped_LOT  = [ 0 for i in range(55)]
        self.Shipped       = Shipped      = [ 0 for i in range(55)]


# ******************************
# set_EVAL_cash_out_data #list for 54 weeks
# ******************************
        self.SGMC          = SGMC         = [ 0 for i in range(55)]
        self.PO_manage     = PO_manage    = [ 0 for i in range(55)]
        self.PO_cost       = PO_cost      = [ 0 for i in range(55)]
        self.P_unit        = P_unit       = [ 0 for i in range(55)]
        self.P_cost        = P_cost       = [ 0 for i in range(55)]

        self.I             = I            = [ 0 for i in range(55)]

        self.I_unit        = I_unit       = [ 0 for i in range(55)]
        self.WH_cost       = WH_cost      = [ 0 for i in range(55)]
        self.Dist_Cost     = Dist_Cost    = [ 0 for i in range(55)]


# ******************************
# update status 状態の更新-1  Pの更新  P = lot_counts X lot_size
# ******************************
    def update_P_year_lot_counts(self):

        for W in range(0,54): ### 

            self.P_year[ W ]=self.lot_counts[ W ] * self.planning_lot_size


# ******************************
# update status 状態の更新-2 PSIの更新
# ******************************
# ******************************
# calculaton I[i+1] = I+P-S-CO     これがPSI計算式
# ******************************
    def CalcPlanSIP(self):

        for i in range(0,53):

# I[i+1] =IF(G97I+G98P-G95S-G96CO<0,0,G97+G98-G95-G96)
#
            Ix = self.I_year[i]+self.P_year[i]-self.S_year[i]-self.CO_year[i]

            if Ix < 0 :
                self.I_year[i+1] = 0
            else:
                self.I_year[i+1] = Ix


# CO[i+1]=IF(G95S+G96CO>G97I+G98P,G95S+G96CO-(G97I+G98P),0)
#
            COx =self.S_year[i]+self.CO_year[i]-(self.I_year[i]+self.P_year[i])

            if COx > 0 :
                self.CO_year[i+1] = COx
            else:
                self.CO_year[i+1] = 0


# IP[i+1}=G97I+G98P-G95S-G96CO
#
            IPx=self.I_year[i]+self.P_year[i]-self.S_year[i]-self.CO_year[i]
            self.IP_year[i+1] = IPx

        #print('calc_SIP')
        #print(self.S_year,self.CO_year, self.I_year, self.P_year, self.IP_year)

# ******************************
# Calc_S_month   Monthly Sの初期設定
# ******************************
    def Calc_S_month(self):

        self.S_month = [0,0,0,0,0,0,0,0,0,0,0,0,0]

        #S_year[i]の値を4-4-5でスライスして合計
        self.S_month[1] = sum(self.S_year[0:4])
        self.S_month[2] = sum(self.S_year[4:8])
        self.S_month[3] = sum(self.S_year[8:13])

        for j in range(1,4): # 1四半期　4四半期　13ヶ月増分
            self.S_month[1+j*3] = sum(self.S_year[0+j*13:4+j*13])
            self.S_month[2+j*3] = sum(self.S_year[4+j*13:8+j*13])
            self.S_month[3+j*3] = sum(self.S_year[8+j*13:13+j*13])


# ******************************
# off_flag[i]の値を4-4-5でスライスしたリスト
# ******************************
    def set_off_list_month(self):

        self.off_list_month = [0,0,0,0,0,0,0,0,0,0,0,0,0] #要素13

        #off_flag[i]の値を4-4-5でスライスしたリストをセット
        self.off_list_month[1] = self.off_flag[0:4]
        self.off_list_month[2] = self.off_flag[4:8]
        self.off_list_month[3] = self.off_flag[8:13]

        for j in range(1,4): # 1四半期　4四半期　13ヶ月増分
            self.off_list_month[1+j*3] = self.off_flag[0+j*13:4+j*13]
            self.off_list_month[2+j*3] = self.off_flag[4+j*13:8+j*13]
            self.off_list_month[3+j*3] = self.off_flag[8+j*13:13+j*13]


# ******************************
# write for animation
# ******************************
    def write_csv4animation(self, month_no, reward):

        self.month_no      = month_no
        self.reward        = reward

        ##self.lot_no        = lot_no ## lot_noはi_PlanSpaceが持っている

        l = []
        r = ['week_no','supply_accume','supply_I','supply_P','demand_accume','demand_CO','demand_S']

        l.append(r) # 二次元リストの初期設定

        shipped = []
        s_accume = []

        # lot_noで出力するcsv file nameを作成
        csv_file_name = ".\data\plan_animation_data" + str(self.month_no) +"-"+ str(self.lot_no) +".csv"


# ******************************
# i=0 初期設定
# ******************************
        i = 0
        
        w_no = "W" + str( i ) # Wnの文字列

        # 一行のリストを作成

        # G15shipped = MIN(G6S+G7CO,G8I+G9P)
        shipped.append( min( self.S_year[i]+self.CO_year[i] , self.I_year[i]+self.P_year[i]) )

        s_accume.append( shipped[i] )

        r = []

        r.append(w_no)            # Week_no
        r.append(s_accume[i])     # supply_accume
        r.append(self.I_year[i])  # supply_inventory
        r.append(self.P_year[i])  # supply_purchase
        r.append(s_accume[i])     # demand_accume
        r.append(self.CO_year[i]) # demand_carry_over
        r.append(self.S_year[i])  # demand_sales

        l.append(r)

# ******************************
# i=1-52 CSV書出し用のリスト作成
# ******************************
        #for i in range(1,27):  # for Half
        #for i in range(1,14):  # for Quarter
        for i in range(1,53):   # for year

        #for i in range(0,54):

            # 一行のリストを作成
            w_no = "W" + str( i ) # Wnの文字列

            # G15shipped = MIN(G6S+G7CO,G8I+G9P)
            shipped.append( min( self.S_year[i]+self.CO_year[i] , self.I_year[i]+self.P_year[i]) )


            s_accume.append( s_accume[i-1] + shipped[i-1] )

            r = []

            r.append(w_no)            # Week_no
            r.append(s_accume[i])     # supply_accume
            r.append(self.I_year[i])  # supply_inventory
            r.append(self.P_year[i])  # supply_purchase
            r.append(s_accume[i])     # demand_accume
            r.append(self.CO_year[i]) # demand_carry_over
            r.append(self.S_year[i])  # demand_sales

            l.append(r)

# ******************************
# CSV ファイル書き出し
# ******************************
        with open( csv_file_name , 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(l)

        with open( '.\data\csv_file_name_list' , 'a') as f0:
            print( csv_file_name, file=f0)   ### PRINTで書き出し

        with open( '.\data\csv_reward_list' , 'a') as f1:
            print( self.reward , file=f1)    ### PRINTで書き出し


# ******************************
# evaluation 操作
# ******************************
# ******************************
# EvalPlanSIP  rewardを計算
# EvalPlanSIP  reward & valueを計算@221123
# ******************************
    def EvalPlanSIP(self):

        for i in range(0,53): ### 以下のi+1で1週スタート = W1,W2,W3,,,

            # calc PO_manage 各週の(梱包単位)LOT数をカウントし輸送ロットで丸め
            # =IF(SUM(G104:G205)=0,0,QUOTIENT(SUM(G104:G205),$C$17)+1)

            ### i+1 = W1,W2,W3,,,

            if self.lot_counts[i+1] == 0 : ## ロットが発生しない週の分母=0対応
                self.PO_manage[i+1] = 0
            else:
                self.PO_manage[i+1]=self.lot_counts[i+1]//self.Transport_Lot+ 1

            # Distribution Cost =$C$19*G12
            self.Dist_Cost[i+1] = self.Distriburion_Cost * self.PO_manage[i+1] 
            

            # Inventory UNIT =G97/$C$7 
            self.I_unit[i+1]  = self.I_year[i+1] / self.planning_lot_size


            # WH_COST by WEEK =G19*$C$11*$C$8 
            self.WH_cost[i+1] = self.I_unit[i+1] * self.WH_COST_RATIO * self.REVENUE_RATIO

            # Purchase by UNIT =G98/$C$7
            self.P_unit[i+1]    = self.P_year[i+1] / self.planning_lot_size

            # Purchase Cost =G15*$C$8*$C$10 
            self.P_cost[i+1]    = self.P_unit[i+1] * self.Purchase_cost * self.REVENUE_RATIO

            # PO manage cost =G15*$C$9*$C$8 ### PO_manage => P_unit
            ### self.PO_manage[i+1] = self.PO_manage[i+1] ###
            self.PO_cost[i+1]   = self.P_unit[i+1] * self.PO_Mng_cost * self.REVENUE_RATIO
#            # PO manage cost =G12*$C$9*$C$8 
#            self.PO_cost[i+1]   = self.PO_manage[i+1] * self.PO_Mng_cost * self.REVENUE_RATIO

            # =MIN(G95+G96,G97+G98) shipped
            self.Shipped[i+1] = min( self.S_year[i+1] + self.CO_year[i+1] , self.I_year[i+1] + self.IP_year[i+1] )

            # =G9/$C$7 shipped UNIT
            self.Shipped_LOT[i+1] = self.Shipped[i+1] / self.planning_lot_size

            # =$C$8*G8 Cach In 
            self.Cash_In[i+1] = self.REVENUE_RATIO * self.Shipped_LOT[i+1]

            # =$C$6*(52-INT(RIGHT(G94,LEN(G94)-1)))/52 Week_Intrest Cash =5%/52
            self.Week_Intrest[i+1] = self.Cash_Intrest * ( 52 - (i+1) ) / 52

            # =G7*$C$5 Sales and General managnt cost
            self.SGMC[i+1] = self.Cash_In[i+1] * self.SGMC_ratio

            # =G7*(1+G6)-G13-G16-G20-G5-G21 Profit
            self.Profit[i+1] = self.Cash_In[i+1] * (1+self.Week_Intrest[i+1])               - self.PO_cost[i+1] - self.P_cost[i+1]    - self.WH_cost[i+1]                   - self.SGMC[i+1]    - self.Dist_Cost[i+1]



# ******************************
# monitor 
# ******************************
        #print('running sum(self.Cash_In[1:])', sum(self.Cash_In[1:]))

# ******************************
# reward 切り替え
# ******************************
#        # =SUM(H4:BH4)/SUM(H7:BH7) profit_ratio

#        if sum(self.Cash_In[1:]) == 0:
#
#            self.profit_ratio = 0
#
#        else: 

        if    self.reward_sw == "PROFIT":
        # ********************************
        # 売切る商売や高級店ではPROFITをrewardに使うことが想定される
        # ********************************
            self.profit = sum(self.Profit[1:])  #*** PROFIT

            reward = self.profit

        elif  self.reward_sw == "REVENUE":
        # ********************************
        # 前線の小売りの場合、revenueをrewardに使うことが想定される
        # ********************************
            self.revenue = sum(self.Cash_In[1:]) #*** REVENUE

            reward = self.revenue

        elif  self.reward_sw == "PROFITRATIO":
        # ********************************
        # 一般的にはprofit ratioをrewardに使うことが想定される
        # ********************************

            if sum(self.Cash_In[1:]) == 0:

                self.profit_ratio = 0

            else:

                self.profit_ratio = sum(self.Profit[1:]) /sum(self.Cash_In[1:])
            # ********************************************
            reward = self.profit_ratio  #*** PROFIT RATIO

        else: #その他のdefaltは profit ratio とする
        # ********************************
        # 一般的にはprofit ratioをrewardに使うことが想定される
        # ********************************

            if sum(self.Cash_In[1:]) == 0:

                self.profit_ratio = 0

            else:

                self.profit_ratio = sum(self.Profit[1:]) /sum(self.Cash_In[1:])

            # ********************************************
            reward = self.profit_ratio  #*** PROFIT RATIO


            #self.profit_ratio= sum(self.Profit[1:]) /sum(self.Cash_In[1:])
            #reward = self.profit_ratio  #*** PROFIT RATIO



        # ********************************
        # lot_valueを計算するために、profit=valueをセットする @221123
        # ********************************
        self.profit = sum(self.Profit[1:])  #*** PROFIT

        value = self.profit


        return( reward, value )
        #return( reward )
# ******************************
# class PlanSpace定義　終了
# ******************************


# ******************************
# LotSpaceクラス定義
# ******************************

class LotSpace():

    def __init__( self, week_no_Y ):

        ### week_no_Y = 54

        self.lot_space_Y       = [[] for j in range(week_no_Y)] 
        self.lot_space_Y_value = [[] for j in range(week_no_Y)] 


# ******************************
# lot_space_Mの初期化
# ******************************
    def init_lot_space_M(self, week_no): 

        self.lot_space_M = [[] for j in range( week_no )] 


# ******************************
# action 操作 place_lot()
# ******************************
# ******************************
# place_lot_actionでself.lot_space[][]のLOT0をappendで操作
# ******************************

    def place_lot_action(self, lot_no, week_no):

# 指定したlot_noを、指定した週week_no中の「空き枠」に積む

        #print('lot_space', self.lot_space) 
        #print('lot_no & week_no',lot_no,week_no)

        lot_step = 0

# ******************************
# lot_loading_listとしてappend する
# ******************************
        lot_loading_list                  = self.lot_space_M[week_no-1]
        lot_loading_list.append( lot_no )

        self.lot_space_M[week_no-1]       = lot_loading_list
        lot_len = len( lot_loading_list )

        lot_step = lot_len - 1

        return ( lot_step )
# ******************************
# class LorSpace定義　終了
# ******************************


# ******************************
# 複数年用 write_PSI_DB_data2df 
# PlanSpaceからPSIをリスト化して、dfの該当indexを更新
# ******************************
def update_PSI_DB_data2df( df, year, node, i_PlanSpace  ):

    PSI_data = []

    #
    # PSI_DBのdataframeから、変数@year+@nodeで検索して、psiの行数indexを入手
    #
    psi_index = df.query("year == @year & node_to == @node").index.tolist()

    ####print('psi_index',psi_index)

    # "l"で、i_PlanSpaceの中のPSIをリスト化
    l       = []
    l_index = []

    l_index.append( year ) #@220929

    l_index.append( i_PlanSpace.product_name )
    l_index.append( i_PlanSpace.SC_tree_id )
    l_index.append( i_PlanSpace.node_from )
    l_index.append( i_PlanSpace.node_to )

    ####print('l_index@i_PlanSpace@output',l_index)

    l.append( l_index + ["1S"]  + i_PlanSpace.S_year  )
    l.append( l_index + ["2CO"] + i_PlanSpace.CO_year )
    l.append( l_index + ["3I"]  + i_PlanSpace.I_year  )
    l.append( l_index + ["4P"]  + i_PlanSpace.P_year  )
    l.append( l_index + ["5IP"] + i_PlanSpace.IP_year )

    # 生成されたpsi_dataをリスト化してreturnする
    PSI_data = l

    for i , ind in enumerate(psi_index):

        ####print('ind, df.loc[ind]', ind, df.loc[ind] )

        ## checking df
        #df_l = df.loc[ind].values.tolist()
        #print('df_l_BEFORE', df_l, len(df_l) )

        # psiのリストから、一つ取り出して、dfのデータレイアウトに整合
        l_work = []
        l_work = l[i]
        ####print('l_work1', i, l_work , len(l_work) )

        # psiリストの先頭にPSI_DBのindexを1回追加して、dfと整合
        l_work.insert(0, ind)

        #l_work.insert(0, ind)

        ####print('l_work2', i, l_work , len(l_work) )

        # PDI_DB更新  行数index指定でpsiリストを代入
        df.loc[ind] = l_work 


        # **************************
        # ***** 値渡しでdf copy
        # **************************
        #df2 = df.copy()

        # **************************
        # ***** 参照渡しでdf copy
        # **************************
        df2 = df


        ## checking df
        #df_l = df.loc[ind].values.tolist()
        #print('df_l_AFTER', df_l, len(df_l) )

#df_psi_l [2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '1S', 2, 50, 30, 30, 30, 63, 63, 63, 63, 80, 80, 80, 80, 80, 125, 125, 125, 125, 150, 150, 150, 150, 140, 140, 140, 140, 140, 223, 223, 223, 223, 250, 250, 250, 250, 180, 180, 180, 180, 180, 175, 175, 175, 175, 100, 100, 100, 100, 10, 10, 10, 10, 10, 10] 60

#i, l[i] 0 [0, 2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '1S', 2, 50, 30, 30, 30, 63, 63, 63, 63, 80, 80, 80, 80, 80, 125, 125, 125, 125, 150, 150, 150, 150, 140, 140, 140, 140, 140, 223, 223, 223, 223, 250, 250, 250, 250, 180, 180, 180, 180, 180, 175, 175, 175, 175, 100, 100, 100, 100, 10, 10, 10, 10, 10, 10] 61

    return PSI_data, df2


# ******************************
# 単年用 write_PSI_data2csv
# ******************************
def write_PSI_data2csv( i_PlanSpace, file_name ):

    l       = []
    l_index = []

    l_index.append( i_PlanSpace.product_name )
    l_index.append( i_PlanSpace.SC_tree_id )
    l_index.append( i_PlanSpace.node_from )
    l_index.append( i_PlanSpace.node_to )

    ####print('l_index@i_PlanSpace@output',l_index)

    header = ["prod_name" , "scm_id" , "node_from" , "node_to" , "SIP" , "W00" , "W01" , "W02" , "W03" , "W04" , "W05" , "W06" , "W07" , "W08" , "W09" , "W10" , "W11" , "W12" , "W13" , "W14" , "W15" , "W16" , "W17" , "W18" , "W19" , "W20" , "W21" , "W22" , "W23" , "W24" , "W25" , "W26" , "W27" , "W28" , "W29" , "W30" , "W31" , "W32" , "W33" , "W34" , "W35" , "W36" , "W37" , "W38" , "W39" , "W40" , "W41" , "W42" , "W43" , "W44" , "W45" , "W46" , "W47" , "W48" , "W49" , "W50" , "W51" , "W52" , "W53"]

    with open( file_name , 'w'  , newline="") as f:
        writer = csv.writer(f)

        # *********************
        # *** write headder ***
        # *********************
        writer.writerow(header)

        # *********************
        # *** write S-CO-I-P-IP
        # *********************
        #print('i_PlanSpace.S_year',i_PlanSpace.S_year)

        l = l_index + ["1S"] + i_PlanSpace.S_year
        writer.writerow(l)

        l = l_index + ["2CO"] + i_PlanSpace.CO_year
        writer.writerow(l)

        l = l_index + ["3I"] + i_PlanSpace.I_year
        writer.writerow(l)

        l = l_index + ["4P"] + i_PlanSpace.P_year
        writer.writerow(l)

        l = l_index + ["5IP"] + i_PlanSpace.IP_year
        writer.writerow(l)

# ******************************
# C-P-U csv output start 
# ******************************
# ******************************
# make a raw 4 csv write common_plan_unit.csv 
# ******************************
#
#lotxxxxxxx 
#0: seq_no, # Global SCM Planでユニークになるindex sequence:着荷点とロットNo
            #
            # sample: SHA+2023+18+00003
            #
            # 場所:PSI_entity:PSI_control_location:PSI在庫管理拠点名:HCM 3桁

            # 時間:YYYYWW:202318      4+2桁
            # 時間:YYYYMMWW:20230207  4+2+2桁
            # ロット番号:step_no :nnnnn 5桁?

            # 上記の定義が違っている? 現状は以下のとおり、
            # YYYY MM LLL
            # lot_spaceの中に「月+ロット番号」をセットしているので、これを使う


#1: control_flag , # 特定ロットを計画GUIで固定などしたい時の管理フラグ(未使用)

#2: priority_no, # place_lotの入力lot_queueのqueueing priorityで計画したい時
                 # PSI_entity:PSI在庫管理拠点の同階層の中での優先順位:nnnn 4桁
#3: modal,       # BOAT, AIR, QOURIER, HANDCARRY, B/A/Q/H
#4: LT ,         # example: 3 weeks(JPN-HCM), 12 weeks(JPN-AMS)

#5: from_x ,       #  PSI_entity:JPN
#6: ETD_YYYYWWW ,  # 出荷日:ETD:202202xx
#7: step_xx ,      # lot_step_no: lot_no in a week bucket

#8: to_y ,         #  PSI_entity:HCM
#9: ETA_YYYYWW ,   #  着荷日:ETA:202203yy
#10: step_yy       #  lot_step_no: lot_no in a week bucket

#11: Value # root生産拠点の生産capaを供給配分するknapsack問題をDP solverで解く



# ******************************
# 複数年 make row 一行の作成
# ******************************
def make_row_N(week_no,lot_step,i_LotSpace,i_PlanSpace, mm_lot_no, mm_lot_value):

    r = []

    seq_no = str(i_PlanSpace.node_to) +str(i_PlanSpace.PlanningYear) +str(mm_lot_no)


    r.append(seq_no)            # seq_no

    control_flag = 'F' # R:Rock, F:Free
    r.append(control_flag)      # control_flag

    # *****
    # SHA:001
    # HCM:002
    # AMS:003
    # *****

    priority_no = '001'+str(i_PlanSpace.PlanningYear) +str(mm_lot_no)

    r.append(priority_no)       # priority_no

    modal = 'B'                 # B:BOAT, A:AIR, Q:Qourier, H:HandCarry

    r.append(modal)             # modal

    r.append(i_PlanSpace.LT_boat)                # LT

    r.append(i_PlanSpace.node_from)              # from_x


    # **************************
    #ETD_year
    # **************************
    ETD_week = week_no - i_PlanSpace.LT_boat    # 年の判定のために事前に計算

    if ETD_week > 0:
        ETD_year = i_PlanSpace.PlanningYear
    else:

        ETD_year = i_PlanSpace.PlanningYear - 1 # 前年をセット

        ETD_week += 52                  # 前年週+52に変換

    r.append(ETD_year)                           # ETD from_year

    r.append(ETD_week)                           # ETD from_week_no


    # 各需要地からのETDのstep_noが重複する!?!?!?
    r.append(lot_step)                           # step_xx

    r.append(i_PlanSpace.node_to)                # to_y

    # **************************
    #ETA_year
    # **************************
    ETA_year = i_PlanSpace.PlanningYear
    r.append(ETA_year)                           # ETA from_year

    r.append(week_no)                            # ETA to_week_no

    r.append(lot_step)                           # step_yy


#    #@#@ adding 'value' は、Plan_envの中で、評価結果rewardの差分として計算

#    reward                     = i_PlanSpace.EvalPlanSIP()
#    i_PlanSpace.reward         = reward

#@#@ lot_valueはlot_noとのペア・リストで、lot_place後の値をlogした後、
#    再度、[mm_lot_no, mm_lot_value]として一緒に取り出す。
#
#@#@ 'value' (= reward_delta)は、place_lotされたLOT一つ分の価値計算
#    i_PlanSpace.reward_delta   = i_PlanSpace.reward - i_PlanSpace.reward_prev
#    i_PlanSpace.reward_prev    = i_PlanSpace.reward    # _prev前に退避する

    #lot_value = i_PlanSpace.reward_delta

    #r.append(i_PlanSpace.reward_delta)           # lot_value
    r.append(mm_lot_value)                       # lot_value


    return(r)


# ******************************
# make row 一行の作成
# ******************************
def make_row(week_no,lot_step,i_LotSpace,i_PlanSpace, mm_lot_no, mm_lot_value):

    r = []

    seq_no = str(i_PlanSpace.node_to) +str(i_PlanSpace.PlanningYear) +str(mm_lot_no)


    r.append(seq_no)            # seq_no

    control_flag = 'F' # R:Rock, F:Free
    r.append(control_flag)      # control_flag

    # *****
    # SHA:001
    # HCM:002
    # AMS:003
    # *****

    priority_no = '001'+str(i_PlanSpace.PlanningYear) +str(mm_lot_no)

    r.append(priority_no)       # priority_no

    modal = 'B'                 # B:BOAT, A:AIR, Q:Qourier, H:HandCarry

    r.append(modal)             # modal

    r.append(i_PlanSpace.LT_boat)                # LT

    r.append(i_PlanSpace.node_from)              # from_x

    ETD_week = week_no - i_PlanSpace.LT_boat
    r.append(ETD_week)                           # ETD from_week_no

    # 各需要地からのETDのstep_noが重複する!?!?!?
    r.append(lot_step)                           # step_xx

    r.append(i_PlanSpace.node_to)                # to_y

    r.append(week_no)                            # ETA to_week_no

    r.append(lot_step)                           # step_yy


#@220927 adding 'value' は、Plan_envの中で、評価結果rewardの差分として計算
#
#    reward                     = i_PlanSpace.EvalPlanSIP()
#    i_PlanSpace.reward         = reward

#@221009 lot_valueはlot_noとのペア・リストで、lot_place後の値をlogした後、
#        再度、[mm_lot_no, mm_lot_value]として一緒に取り出す。
#
#@220927 'value' (= reward_delta)は、place_lotされたLOT一つ分の価値計算
#    i_PlanSpace.reward_delta   = i_PlanSpace.reward - i_PlanSpace.reward_prev
#    i_PlanSpace.reward_prev    = i_PlanSpace.reward    # _prev前に退避する

    #lot_value = i_PlanSpace.reward_delta

    #r.append(i_PlanSpace.reward_delta)           # lot_value
    r.append(mm_lot_value)                       # lot_value


    return(r)


# ******************************
# 複数年 csv write common_plan_unit.csv 共通計画単位による入出力
# ******************************
def csv_write2common_plan_unit_N(i_LotSpace,i_PlanSpace, fin_lot_space_Y, fin_lot_space_Y_value): 

    l = []

    # ********* ヘッダー image
    #r = ['seq_no','control_flag','priority_no','modal','LT','Dpt_entity','Dpt_year','Dpt_week','Dpt_step','Arv_entity','Arv_year','Arv_week','Arv_step','Value']


    # lot_noで出力するcsv file nameを作成
    csv_file_name = "common_plan_unit.csv"


    #@#@
    #print(type(fin_lot_space_Y),fin_lot_space_Y)

    for week_no in range(0,53):

        for lot_step, name in enumerate( fin_lot_space_Y[ week_no ] ):

            #print('week_no&lot_step&lot_space_Y = ',week_no,lot_step,fin_lot_space_Y[week_no][lot_step])

    #@#@
    # lot_noの持ち方を[lot_no,lot_value]のリストにして、出し入れする。
    # lot_noは、色々と使っているので、
    # lot_no_valueというペアリストを新しく定義する。
    # class PlanSpaceに、lot_no, lot_value, lot_no_valueを定義

#week_no&lot_step&lot_space_Y =  20 61 0
#week_no&lot_step&lot_space_Y =  20 62 0
#week_no&lot_step&lot_space_Y =  20 63 0
#week_no&lot_step&lot_space_Y =  21 0 05001
#week_no&lot_step&lot_space_Y =  21 1 05006
#week_no&lot_step&lot_space_Y =  21 2 05009
#week_no&lot_step&lot_space_Y =  21 3 0
#week_no&lot_step&lot_space_Y =  21 4 0
#week_no&lot_step&lot_space_Y =  21 5 0

            mm_lot_no    = fin_lot_space_Y[week_no][lot_step]

            #@221009 xxxxx
            mm_lot_value = fin_lot_space_Y_value[week_no][lot_step]


            ### make＿rowの中で一行分を加工している

            r = make_row_N(week_no,lot_step,i_LotSpace,i_PlanSpace, mm_lot_no, mm_lot_value )


            #r = make_row(week_no,lot_step,i_LotSpace,i_PlanSpace, mm_lot_no, mm_lot_value )

            l.append(r)


# ******************************
# CSV ファイル書き出し
# ******************************

    #print('l',l)

    with open( csv_file_name , 'a', newline="") as f1:
    #with open("'ファイル名'.csv", "w", newline="") as f:

        writer = csv.writer(f1)
        writer.writerows(l)


# ******************************
# OLD
# ******************************
def csv_write2common_plan_unit(i_LotSpace,i_PlanSpace, fin_lot_space_Y, fin_lot_space_Y_value): 
#def csv_write2common_plan_unit(i_LotSpace,i_PlanSpace, fin_lot_space_Y): 

    l = []

    #seq_no, control_flag , priority_no, modal, LT , from_x , from_Wxx , step_xx , to_y , to_Wyy , step_yy 

    # ********* ヘッダーが各PSI計画の出力の毎に付いてしまうのは避けたい
    #r = ['seq_no','control_flag','priority_no','modal','LT','from_x','from_Wxx','step_xx','to_y','to_Wyy','step_yy']

    # lot_noで出力するcsv file nameを作成
    csv_file_name = "common_plan_unit.csv"
    #csv_file_name = ".\common_plan_unit.csv"
    #csv_file_name = ".\data\common_plan_unit.csv"


    #4monitoring
    #print(type(fin_lot_space_Y),fin_lot_space_Y)


    for week_no in range(0,53):



        for lot_step, name in enumerate( fin_lot_space_Y[ week_no ] ):

            #print('week_no&lot_step&lot_space_Y = ',week_no,lot_step,fin_lot_space_Y[week_no][lot_step])

        #@#@
        # lot_noの持ち方を[lot_no,lot_value]のリストにして、出し入れする。
        # lot_noは、色々と使っているので、
        # lot_no_valueというペアリストを新しく定義する。
        # class PlanSpaceに、lot_no, lot_value, lot_no_valueを定義

#week_no&lot_step&lot_space_Y =  20 61 0
#week_no&lot_step&lot_space_Y =  20 62 0
#week_no&lot_step&lot_space_Y =  20 63 0
#week_no&lot_step&lot_space_Y =  21 0 05001
#week_no&lot_step&lot_space_Y =  21 1 05006
#week_no&lot_step&lot_space_Y =  21 2 05009
#week_no&lot_step&lot_space_Y =  21 3 0
#week_no&lot_step&lot_space_Y =  21 4 0
#week_no&lot_step&lot_space_Y =  21 5 0

            mm_lot_no    = fin_lot_space_Y[week_no][lot_step]

            mm_lot_value = fin_lot_space_Y_value[week_no][lot_step]

            ### make＿rowの中で一行分を加工している
            r = make_row(week_no,lot_step,i_LotSpace,i_PlanSpace, mm_lot_no, mm_lot_value )

            l.append(r)


# ******************************
# CSV ファイル書き出し
# ******************************

    #print('l',l)

    with open( csv_file_name , 'a', newline="") as f1:
    #with open("'ファイル名'.csv", "w", newline="") as f:

        writer = csv.writer(f1)
        writer.writerows(l)


# ******************************
# type check
# ******************************
def isint(s):  # 整数値を表しているかどうかを判定
    try:
        int(s, 10)  # 文字列を実際にint関数で変換してみる
    except ValueError:
        return False
    else:
        return True

def isfloat(s):  # 浮動小数点数値を表しているかどうかを判定
    try:
        float(s)  # 文字列を実際にfloat関数で変換してみる
    except ValueError:
        return False
    else:
        return True


def to_int_float_str(x):

    if isint(x) == True:
        value_x = int(x)

    else:
        if isfloat(x) == True:
            value_x = float(x)
        else:
            value_x = str(x)

    return(value_x)


# ******************************
# end of type check
# ******************************


# ******************************
# read profile DB CSV              # on going code
# ******************************
def read_plan_prof_DB_csv( filename, node, year ): 

    plan_profile_dic_Y = {} #辞書型を宣言

    ## Headerを設定する
    #csv_header = ['attribute','value']
    ##csv_header = ['attribute','value','a_type','memo']

    with open( file_name , 'r',encoding="utf-8_sig") as f: 

        for row in csv.DictReader(f, csv_header):

            value_r = to_int_float_str(row['value'])

            plan_profile_dic[row['attribute']] = value_r

    #print('read profile CSV2DIC: ',plan_profile_dic)

    return plan_profile_dic


# ******************************
# read profile CSV
# ******************************
def read_plan_prof_csv( file_name ):

    plan_profile_dic = {} #辞書型を宣言

    # Headerを設定する
    csv_header = ['attribute','value']
    #csv_header = ['attribute','value','a_type','memo']

    with open( file_name , 'r',encoding="utf-8_sig") as f: 

        for row in csv.DictReader(f, csv_header):

            value_r = to_int_float_str(row['value'])

            plan_profile_dic[row['attribute']] = value_r

    #print('read profile CSV2DIC: ',plan_profile_dic)

    return plan_profile_dic


# ******************************
# read S-CO-I-P-IP data CSV
# ******************************
# ******************************
# read_PSI_data_csv
# ******************************
def read_PSI_data_csv( file_name ): 

    PSI_data = [] #リスト型を宣言

# ******************************
# Headerがcsv fileに含まれている場合の記述
# ******************************
# prod_name	scm_id	node_from	node_to	SIP	W00	W01	W02	W03	W04	W05	W06	W07	W08	W09	W10	W11	W12	W13	W14	W15	W16	W17	W18	W19	W20	W21	W22	W23	W24	W25	W26	W27	W28	W29	W30	W31	W32	W33	W34	W35	W36	W37	W38	W39	W40	W41	W42	W43	W44	W45	W46	W47	W48	W49	W50	W51	W52	W53

    df = pd.read_csv( file_name , header=0  )
    #df = pd.read_csv( file_name , header=0 , encoding='shift-jis' )
    #df = pd.read_csv( file_name , encoding='shift-jis' , sep=',' )

    PSI_data = df.values.tolist()
    #PSI_data = df.to_numpy().tolist() #どっちが自然か?

    #for l in PSI_data:
    #    #print(l)
    #    print(l[3])
    #    print(l[4])
    #    print(l[5:])

    return PSI_data


# ******************************
# read_PSI_data_scmtree 将来のSCM拡張
# ******************************
def read_PSI_data_scmtree( file_name, node_name ): 

### SCMツリー定義の場合はnode_name = node_from + node_to
### 単体のPSIの場合はnode_name = node_to


    PSI_data = [] #リスト型を宣言

# ******************************
# Headerがcsv fileに含まれている場合の記述
# *******************************
# prod_name	scm_id	node_from	node_to	SIP	W00	W01	W02	W03	W04	W05	W06	W07	W08	W09	W10	W11	W12	W13	W14	W15	W16	W17	W18	W19	W20	W21	W22	W23	W24	W25	W26	W27	W28	W29	W30	W31	W32	W33	W34	W35	W36	W37	W38	W39	W40	W41	W42	W43	W44	W45	W46	W47	W48	W49	W50	W51	W52	W53

    df = pd.read_csv( file_name , header=0  )
    #df = pd.read_csv('PSI_data_sample2.csv', header=0 , encoding='shift-jis' )
    #df = pd.read_csv('common_plan_unit.csv',encoding='shift-jis',sep=',')

    #print(df)


    df_node_to = df.query('node_to == @node_name ')

    #print(df_node_to)


    PSI_data = df_node_to.values.tolist()

# monitor
#
#    for l in PSI_data:
#        #print(l)
#        print(l[3])
#        print(l[4])
#        print(l[5:])


    if PSI_data == []:
        print('Error reading PySI_data_IO : node_name is not matching')
    else:
        print('read PSI_data_csv2list: ',PSI_data)

    return PSI_data


# ******************************
# 事業拠点名(=node_name)を指定してload_profile  固定したstd_fileでの読み書き
# ******************************
# ******************************
# !!!これは使っていない!!!
# ******************************
# 
def load_plan( node_name ):

# ******************************
# node_nameは将来の拡張で"scm_tree"に定義のnode名でglobal SCPを処理
# ******************************

    node_file_name = "PySI_Profile_std.csv"         #プロファイル名を宣言
    #node_file_name = ".\data\PySI_Profile_std.csv" #プロファイル名を宣言

    plan_prof = {}                                  #retuen用に辞書型を宣言

    plan_prof = read_plan_prof_csv( node_file_name )

    ####print( plan_prof )

# ******************************
# PSI_data_file_nameは将来的にscm_treeに定義されたnodeとして外から与える
# ******************************

    PSI_data_file_name = "PySI_data_std_IO.csv" # PSI data IOファイル名を宣言

# ******************************
# node_name はnode_to 将来的にSCM tree node指定で使いたい
# ******************************
# node_name = "WCHxx" #node_nameを指定

    PSI_data = [] #retuen用にリスト型を宣言

    PSI_data = read_PSI_data_scmtree( PSI_data_file_name, node_name )

    #print( 'read PSI_data',PSI_data )


# ******************************
# instanciate PlanSpace
# ******************************

    ####print('plan_prof DIC',plan_prof)

    i_PlanSpace = PlanSpace( plan_prof, PSI_data )

    i_PlanSpace.Calc_S_month()

    # 前処理で、off_listは年間off_listからスライス
    i_PlanSpace.set_off_list_month()

# ******************************
# LotSpace class instanciate 
# ******************************

    i_LotSpace = LotSpace( 54 )

    return(i_PlanSpace,i_LotSpace)


# *********************
# end of "PySI_PlanLot_xxx"
# *********************



# *********************
# followings are data image 
# *********************

# *********************
# PSI_DB_data 
# *********************
#PSI_DB_data [
#[0, 2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '1S', 2, 50, 30, 30, 30, 63, 63, 63, 63, 80, 80, 80, 80, 80, 125, 125, 125, 125, 150, 150, 150, 150, 140, 140, 140, 140, 140, 223, 223, 223, 223, 250, 250, 250, 250, 180, 180, 180, 180, 180, 175, 175, 175, 175, 100, 100, 100, 100, 10, 10, 10, 10, 10, 10], 
#
#[1, 2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '2CO', 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
#
#[2, 2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '3I', 0, 0, 98, 218, 278, 398, 365, 422, 419, 416, 426, 436, 386, 426, 406, 461, 426, 511, 416, 266, 236, 266, 416, 426, 436, 386, 426, 406, 483, 440, 487, 474, 434, 184, 354, 464, 374, 284, 254, 224, 224, 469, 474, 539, 454, 384, 284, 184, 84, 104, 94, 84, 74, 64], 
#
#[3, 2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '4P', 0, 150, 150, 90, 150, 30, 120, 60, 60, 90, 90, 30, 120, 60, 180, 90, 210, 30, 0, 120, 180, 300, 150, 150, 90, 180, 120, 300, 180, 270, 210, 210, 0, 420, 360, 90, 90, 150, 150, 180, 420, 180, 240, 90, 30, 0, 0, 0, 30, 0, 0, 0, 0, 0], 
#
#[4, 2023, 'prod56789012345', 'sc010', 'YTO', 'YTOLEAF', '5IP', 0, -2, 98, 218, 278, 398, 365, 422, 419, 416, 426, 436, 386, 426, 406, 461, 426, 511, 416, 266, 236, 266, 416, 426, 436, 386, 426, 406, 483, 440, 487, 474, 434, 184, 354, 464, 374, 284, 254, 224, 224, 469, 474, 539, 454, 384, 284, 184, 84, 104, 94, 84, 74, 64]]
#

