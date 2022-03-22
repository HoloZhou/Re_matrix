# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:07:12 2022

@author: Zhou N
"""

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import pip
pip.main(["install", "openpyxl"])


st.title('多项列转换程序')

imagebe = Image.open("before.png")
st.image(imagebe, caption='处理前（符合人工录入习惯的格式）',
         use_column_width=True)
imageaf = Image.open("after.png")
st.image(imageaf, caption='处理后（符合数据处理需求的格式）',
         use_column_width=True)


# 读取

# 挪动

coma=st.text_input("您在目标列使用的分隔标点是什么（区分中英文）", key=None)

file = st.file_uploader(
    "点击此处上传文件", type=["xls", "xlsx"], accept_multiple_files=False)
st.text("请上传xls或xlsx格式文件，样本索引列使用纯数字编号")
st.spinner(text='In progress...')
  

if file is not None:
    oridata=pd.read_excel(file)
    oridata=pd.DataFrame(oridata)
    col=oridata.columns
    col1name=col[0]    
    col2name=col[1]
    coltail=oridata[col[1]].str.split(coma,expand=True)
    oridata=pd.concat([oridata[col1name], coltail], axis=1, join="outer")
    oridata=oridata.fillna(value=np.nan)
    oridata=oridata.replace(np.nan, "0")
    output=pd.DataFrame(columns=[col1name, col2name])  
    for index, row in oridata.iterrows():
        for i in row:
            if isinstance(i, int) == True and i != "0":
                case=i
                case=str(case)
                case=[case]              
                col1name=[col[0]]
                case=pd.DataFrame(case, columns=col1name)
                output=pd.concat([output, case], axis=0,
                             ignore_index=True, join="outer")
            elif isinstance(i, str) == True and i != "0":
                react=str(i)
                react=[react]                
                col2name=[col[1]]
                react=pd.DataFrame(react, columns=col2name)
                output=pd.concat([output, react], axis=0,
                               ignore_index=True, join="outer")
            elif str(i) == "0":
                break

    if col1name!=col2name:
        # 后处理
        output[col1name]=output[col1name].fillna(method='ffill')
        output.dropna(subset=[col[1]], axis=0, inplace=True, how="any")
        # 翻矩阵
        output['COUNT']=1
        output=output.pivot_table('COUNT', index=col1name, columns=col2name).fillna(0)
    
    st.dataframe(output)
    def convert_df(output):   
         return output.to_csv().encode('utf-8')
    
    excel = convert_df(output)
    
    if excel is not None:
        st.download_button(label="点击此处下载已完成数据",data=excel,file_name='已处理完成的数据.csv',mime='csv')
        st.text("注：转换完成的数据是CSV格式")
    
    
    
    
    
    
    
    
    
    
