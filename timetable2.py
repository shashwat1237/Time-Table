import pandas as pd
import ast
num_slot_each_day=7
num_days=6
timetable=[[0 for _ in range(num_slot_each_day)] for _ in range(num_days)]


teachers=pd.read_csv("teachers.csv",header=0)
teachers["timetable"]=teachers["timetable"].apply(ast.literal_eval)
#id,name,timetable
classes=pd.read_csv("classes.csv",header=0)
classes["timetable"]=classes["timetable"].apply(ast.literal_eval)
classes["st"]=classes["st"].apply(ast.literal_eval)
classes["sl"]=classes["sl"].apply(ast.literal_eval)
#id,name,branch,year,st={subject_ids:teacher_ids},sl={subject_ids:lectures_per_week},timetable
subjects=pd.read_csv("subjects.csv",header=0)
#id,name,room_type,lecture_length
rooms=pd.read_csv("rooms.csv",header=0)
rooms["timetable"]=rooms["timetable"].apply(ast.literal_eval)
#room_id,room_type,timetable

def or_op(a1,a2):
    a3=[[i or j for i,j in zip(row1,row2)] for row1,row2 in zip(a1,a2)]
    return a3
def and_op(arrays):
    a3=[[1 for _ in range(7)] for _ in range(6)]
    for array in arrays:
        a3=[[i and j for i,j in zip(row1,row2)] for row1,row2 in zip(array,a3)]

    return a3
#def matrix_sum(matrix):
#    return sum([sum(row) for row in matrix])
def modify_for_2hr(cr):
    m=[[1 for _ in range(7)] for _ in range(6)]
    i=0
    while i<len(cr):
        j=0
        while j<len(cr[0])-1:
            if cr[i][j]==0 and cr[i][j+1]==0:
                m[i][j]=0
            j+=1

        i+=1
    return m
def get_room_restriction(room_type):
    rooms_selected_timetables=rooms[rooms["room_type"]==room_type]["timetable"].values
    
    return and_op(rooms_selected_timetables)
def calculate_restrictions_for_subject(subjectid,subject_row,classid,class_row):

    st=class_row["st"]
    sl=class_row["sl"]
    
    teacherid=st[subjectid]
    
    room_type=subject_row["room_type"]
    #room_restriction=rooms[rooms["room_type"]==room_type]["timetable"]
    room_restriction=get_room_restriction(room_type)
        
        
    teacher_restriction=teachers[teachers["id"]==teacherid]["timetable"].iloc[0]
    class_restriction=class_row["timetable"]

    m1=or_op(teacher_restriction,class_restriction)
    m2=or_op(room_restriction,m1)
    if subject_row["lecture_length"]==2:
        m2=modify_for_2hr(m2)
    return m2
def find_available(room_type,length,super_i,super_j):
    room_timetables=rooms["timetable"].values.tolist()
    room_types=rooms["room_type"].values.tolist()
    index=0
    
    for room_timetable,room_type_i in zip(room_timetables,room_types):
        if room_type_i!=room_type:
            index+=1
            continue

        if room_timetable[super_i][super_j]!=0:
            index+=1
            continue

        if length==2:
            if room_timetable[super_i][super_j+1]!=0:
                index+=1
                continue

        return index

        

    return -1


def assign_subject(subject_row,class_row,class_index,total_restriction):
    sl=classes.loc[class_index,"sl"]
    #print(sl)

    room_type=subject_row["room_type"]
    subjectid=subject_row["id"]
    teacherid=class_row["st"][subjectid]
    lecture_length=subject_row["lecture_length"]
    teacher_row=teachers[teachers["id"]==teacherid]
    teacher_index=teacher_row.index[0]
    teacher_row=teacher_row.iloc[0]
    #print(teacher_row.index)
    teacherTimeTable=teacher_row["timetable"]
    classTimeTable=class_row["timetable"]

    room_text=class_row["name"]+"  ,  "+subject_row["name"]
    class_text=subject_row["name"]+"  ,  "
    teacher_text=class_row["name"]+"  ,  "+subject_row["name"]+"  ,  "
    
    



    i=0
    while i<6:
        j=0
        while j<7:
            print(j)
            if lecture_length==1:
                if total_restriction[i][j]==0:
                    

                    

                    
                    room_index=find_available(room_type,1,i,j)
                    if room_index==-1:
                        j+=1
                        continue
                    room_id=str(rooms.loc[room_index,"room_id"])
                    classTimeTable[i][j]=class_text+room_id
                    teacherTimeTable[i][j]=teacher_text+room_id
                    
                    roomTimeTable=rooms.loc[room_index,"timetable"]
                    roomTimeTable[i][j]=room_text
                    rooms.at[room_index,"timetable"]=roomTimeTable
                    break
            
            elif total_restriction[i][j]==0:


                room_index=find_available(room_type,2,i,j)
                if room_index==-1:
                    j+=1
                    continue
                room_id=str(rooms.loc[room_index,"room_id"])

                classTimeTable[i][j]=class_text+room_id
                classTimeTable[i][j+1]=class_text+room_id
                teacherTimeTable[i][j]=teacher_text+room_id
                teacherTimeTable[i][j+1]=teacher_text+room_id
                
                roomTimeTable=rooms.loc[room_index,"timetable"]
                roomTimeTable[i][j]=room_text
                roomTimeTable[i][j+1]=room_text
                rooms.at[room_index,"timetable"]=roomTimeTable
                break
            j+=1
        i+=1

    classes.at[class_index,"timetable"]=classTimeTable
    #print(teacher_index)
    teachers.at[teacher_index,"timetable"]=[teacherTimeTable][0]
    subjectid=int(subjectid)
    #print(sl)
    sl[subjectid]=sl[subjectid]-1
    classes.at[class_index,"sl"]=sl
    #print(1)

def assign_to_class(class_row,class_index):
    st=class_row["st"]
    sl=class_row["sl"]

    subjects_list=list(st.keys())

    subjects_2hr=[]
    subjects_1hr=[]

    lecture_length_df=pd.Series(subjects["lecture_length"],
                                index=subjects["id"])


    i=0
    while i<len(subjects_list)-1:
        j=0
        while j<len(subjects_list)-i-1:
            if lecture_length_df[subjects_list[j]]<lecture_length_df[subjects_list[j+1]]:
                
                subjects_list[j],subjects_list[j+1]=subjects_list[j+1],subjects_list[j]

            elif sl[subjects_list[j]]<sl[subjects_list[j+1]]:
                subjects_list[j],subjects_list[j+1]=subjects_list[j+1],subjects_list[j]
            j+=1
        i+=1



    for subjectid in subjects_list:
        subject_row=subjects[subjects["id"]==subjectid].iloc[0]
        #print(class_row["sl"],"hi")
        assign_subject(subject_row,
                       class_row,class_index,
                       calculate_restrictions_for_subject(subjectid,subject_row,class_index,class_row))
        

def decide_timetable_for_each_class():
    global classes
    index=0
    l=len(classes)
    classes["sort_factor"]=classes["sl"].apply(lambda x:sum(x.values()))
    classes.sort_values(by="sort_factor",ascending=False,inplace=True)
    classes.reset_index(drop=True,inplace=True)

    while index<l:
        #print(classes.iloc[index]["sl"])
        assign_to_class(classes.iloc[index],index)
        index+=1     

def reset_timetable():
    global classes,rooms,teachers
    classes["timetable"]=[[[0 for _ in range(7)] for _ in range(6)] for _ in range(len(classes))]
    rooms["timetable"]=[[[0 for _ in range(7)] for _ in range(6)] for _ in range(len(rooms))]
    teachers["timetable"]=[[[0 for _ in range(7)] for _ in range(6)] for _ in range(len(teachers))]
decide_timetable_for_each_class()
#reset_timetable()
teachers.to_csv("teachers.csv",index=False)
rooms.to_csv("rooms.csv",index=False)
classes.to_csv("classes.csv",index=False)

