#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ctypes
import os
import time
import pandas as pd
from tqdm import tqdm
import datetime

from ctypes import *

# Struct members
class sGeneral(Structure):
    _pack_ = 1
    _fields_ = [
                ("TimeStamp",       c_uint64),
                ("Product_Cnt",     c_float),
                ("Recipe_Number",   c_uint32),
                ("Machine_Nom_Vel", c_float),
                ("Machine_Act_Vel", c_float),
                ("Machine_Status",  c_uint32)
               ]

class sFeeder(Structure):
    _pack_ = 1
    _fields_ = [
                ("Feeder_Des_Pos",  c_uint32),
                ("Feeder_Act_Pos",  c_uint32),
                ("Encoder_Act_Pos", c_uint32),
                ("Feeder_Nom_Vel",  c_float),
                ("Feeder_Act_Vel",  c_float),
                ("Feeder_Act_Trq",  c_float)
               ]

class sLongitudinal_Sealer(Structure):
    _pack_ = 1
    _fields_ = [
                ("TempLoop1_VertJaw_SP",            c_float),
                ("TempLoop1_VertJaw_PV",            c_float),
                ("SealerInverter_VertJaw_Nom_Vel",  c_float),
                ("TempLoop1_VertJaw_Active",        c_bool),
                ("TempLoop1_VertJaw_MV",            c_bool)
               ]
    

    
# etc etc...

# Packing Struct members

class MyStructure(Structure):
    _pack_ = 1
    _fields_ = [
                ("general",             sGeneral),
                ("feeder",              sFeeder),
                ("longitudinal_sealer", sLongitudinal_Sealer)
               ]

#etc etc...


# In[2]:


def readFile(filePath,row):

     f = open(filePath,"rb")
     dataSize= os.path.getsize(filePath)
     # print (dataSize)
     f.seek(row * 218)
     data = f.read()
     return bytearray(data)


# In[ ]:





# In[3]:


#We create a list with the names of the columns that will have the output dataframe.

l=[
    "TimeStamp","Product_Cnt", "Recipe_Number", "Machine_Nom_Vel", "Machine_Act_Vel", "Machine_Status",
    
    "Feeder_Des_Pos","Feeder_Act_Pos","Encoder_Act_Pos","Feeder_Nom_Vel","Feeder_Act_Vel","Feeder_Act_Trq",
    
    "TempLoop1_VertJaw_SP", "TempLoop1_VertJaw_PV","SealerInverter_VertJaw_Nom_Vel","TempLoop1_VertJaw_Active","TempLoop1_VertJaw_MV"
    
  ]


# In[4]:


#Creating a funciton that, havin the structure as an input, create a dictionary with the corresponding value. This will allows us fill the dataframe.

def generate_dic(st):
    d={
        "TimeStamp":st.general.TimeStamp,
       "Product_Cnt":st.general.Product_Cnt,
       "Recipe_Number":st.general.Recipe_Number,
       "Machine_Nom_Vel":st.general.Machine_Nom_Vel,
       "Machine_Act_Vel":st.general.Machine_Act_Vel,
       "Machine_Status":st.general.Machine_Status,
    
    "Feeder_Des_Pos":st.feeder.Feeder_Des_Pos,
       "Feeder_Act_Pos":st.feeder.Feeder_Act_Pos,
       "Encoder_Act_Pos":st.feeder.Encoder_Act_Pos,
       "Feeder_Nom_Vel":st.feeder.Feeder_Nom_Vel,
       "Feeder_Act_Vel":st.feeder.Feeder_Act_Vel,
       "Feeder_Act_Trq":st.feeder.Feeder_Act_Trq,
    
    "TempLoop1_VertJaw_SP":st.longitudinal_sealer.TempLoop1_VertJaw_SP, 
       "TempLoop1_VertJaw_PV":st.longitudinal_sealer.TempLoop1_VertJaw_PV,
       "SealerInverter_VertJaw_Nom_Vel":st.longitudinal_sealer.SealerInverter_VertJaw_Nom_Vel,
       "TempLoop1_VertJaw_Active":st.longitudinal_sealer.TempLoop1_VertJaw_Active,
       "TempLoop1_VertJaw_MV":st.longitudinal_sealer.TempLoop1_VertJaw_MV,
    }
    
    return(d)


# In[5]:


def full_read_improved_1_1 (file, l, n_bytes=256):
    start_time = time.time()
    df1 = pd.DataFrame(columns=l)
        
    n_samples= os.path.getsize(file)/n_bytes
    f = open(file,"rb")
    
    for e in tqdm (range(int(n_samples))):            
            
        f.seek(e * 256)
        data = f.read(256)
        
        ByteStream=bytearray(data)     
        
        # Obtain the desired structure thanks to the classes defined for every sample (wich will be a row)
        st = MyStructure.from_buffer(ByteStream)
    
        d=generate_dic(st)
        
        #Appending each row to the dataframe
        df1 = df1.append(d, ignore_index = True)
            
    
    f.close()        
    df=df1  
    
    #Apply extra transformation if needed
    df['TimeStamp'] = df['TimeStamp'].apply(lambda x: datetime.datetime.fromtimestamp((x/1000000)/1000))
    

    print("Complete: " + file)
    
    return(df)


# In[6]:


dataframe=full_read_improved_1_1 ("TestFile_2.bin", l)


# In[7]:


dataframe


# In[ ]:




