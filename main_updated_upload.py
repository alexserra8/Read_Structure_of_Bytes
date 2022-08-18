import ctypes
import os

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


def readFile(filePath,row):

     f = open(filePath,"rb")
     dataSize= os.path.getsize(filePath)
     # print (dataSize)
     f.seek(row * 218)
     data = f.read()
     return bytearray(data)

def main():

    #enter the file path
    testFilePath = 'TestFile_2.bin'
    #enter the row to read
    readRow = 0

    #reading file
    ByteStream = readFile(testFilePath,readRow)

    # check if bytearray can be applied to structure.
    if len(ByteStream) < ctypes.sizeof(MyStructure):
        print("error: bytearray is too short for \"MyStructure\"")
        return

    # Obtain the desired structure thanks to the classes defined
    st = MyStructure.from_buffer(ByteStream)

    #MyStructure.General members
    print("st.general.TimeStamp:",st.general.TimeStamp/1000000)
    print("st.general.Product_Cnt:",st.general.Product_Cnt)
    print("st.general.Recipe_Number:",st.general.Recipe_Number)
    print("st.general.Machine_Nom_Vel:",st.general.Machine_Nom_Vel)
    print("st.general.Machine_Act_Vel:",st.general.Machine_Act_Vel)
    print("st.general. Machine_Status:",st.general. Machine_Status)

    # MyStructure.feeder members
    print("st.feeder.Feeder_Des_Pos:",st.feeder.Feeder_Des_Pos)
    print("st.feeder.Feeder_Act_Pos:",st.feeder.Feeder_Act_Pos)
    print("st.feeder.Encoder_Act_Pos:",st.feeder.Encoder_Act_Pos)
    print("st.feeder.Feeder_Nom_Vel:",st.feeder.Feeder_Nom_Vel)
    print("st.feeder.Feeder_Act_Vel:",st.feeder.Feeder_Act_Vel)
    print("st.feeder.Feeder_Act_Trq:",st.feeder.Feeder_Act_Trq)

    # MyStructure.longitudinal_sealer members
    print("st.longitudinal_sealer.TempLoop1_VertJaw_SP:",st.longitudinal_sealer.TempLoop1_VertJaw_SP)
    print("st.longitudinal_sealer.TempLoop1_VertJaw_PV:",st.longitudinal_sealer.TempLoop1_VertJaw_PV)
    print("st.longitudinal_sealer.SealerInverter_VertJaw_Nom_Vel:",st.longitudinal_sealer.SealerInverter_VertJaw_Nom_Vel)
    print("st.longitudinal_sealer.TempLoop1_VertJaw_Active:",st.longitudinal_sealer.TempLoop1_VertJaw_Active)
    print("st.longitudinal_sealer.TempLoop1_VertJaw_MV:",st.longitudinal_sealer.TempLoop1_VertJaw_MV)

    #etc...


if __name__ == '__main__':
    main()

