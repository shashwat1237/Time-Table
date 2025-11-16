import pandas as pd
num_slot_each_day=7
num_days=6
timetable=[[0 for _ in range(num_slot_each_day)] for _ in range(num_days)]


teachers=pd.read_csv("teachers.csv")
#id,name,timetable
classes=pd.read_csv("classes.csv")
#id,name,branch,year,st={subjects:teachers},sl={subjects:lectures_per_week},timetable
subjects=pd.read_csv("subjects.csv")
#id,name,room_type,lecture_length
rooms=pd.read_csv("rooms.csv")
#room_id,room_type,timetable

def or_op(a1,a2):
    a3=[[i+j-(i*j) for i,j in zip(row1,row2)] for row1,row2 in zip(a1,a2)]
    return a3
def and_op(arrays):
    a3=[[0 for _ in range(7)] for _ in range(6)]
    for array in arrays:
        a3=[[i and j for i,j in zip(row1,row2)] for row1,row2 in zip(array,a3)]

    return a3
def matrix_sum(matrix):
    return sum([sum(row) for row in matrix])
def modify_for_2hr(cr):
    m=[[0 for _ in range(7)] for _ in range(6)]
    i=0
    while i<len(cr):
        j=0
        while j<len(cr[0]):
            if cr[i][j]==1:
                m[i][j]=1
            try:
                if cr[i][j+1]==1:
                    m[i][j]=1
            except:
                m[i][j]=1
            j+=1

        i+=1
    return m
def get_room_restriction(room_type):
    rooms_selected_timetables=rooms[rooms["type"]==room_type]["timetable"].values
    
    return and_op(rooms_selected_timetables)
def calculate_restrictions_for_subject(subjectid,classid):
    class_row=classes[classes["id"]==classid]
    st=class_row["st"]
    sl=class_row["sl"]
    
    teacherid=st[subjectid]
    subject_row=subjects[subjects["id"]==subjectid]
    room_type=subject_row["room_type"]
    #room_restriction=rooms[rooms["room_type"]==room_type]["timetable"]
    room_restriction=get_room_restriction(room_type)
        
        
    teacher_restriction=teachers[teachers["id"]==teacherid]["timetable"]
    class_restriction=class_row["timetable"]

    m1=or_op(teacher_restriction,class_restriction)
    m2=or_op(room_restriction,m1)
    if subject_row["lecture_length"]==2:
        m2=modify_for_2hr(m2)
    return m2
def find_available(room_type,length,i,j):
    room_timetables=rooms["timetable"].values.tolist()
    
    for index,room_timetable in enumerate(room_timetables):
        i=0
        while i<6:
            j=0
            while j<7:
                if (length==1) and room_timetable[i][j]==0:
                        
                    return index
                elif j<6:
                    if (length==2) and room_timetable[i][j]==0 and room_timetable[i][j+1]==0:
                        return index
                j+=1
            i+=1


def assign_subject(subject_row,class_row,class_index,total_restriction):
    sl=classes.loc[class_index,5]
    

    room_type=subject_row["room_type"]
    subjectid=subject_row["id"]
    teacherid=class_row["st"][subjectid]
    lecture_length=subject_row["lecture_length"]
    teacher_row=teachers[teachers["id"]==teacherid]
    teacherindex=teacher_row.index[0]

    teacherTimeTable=teacher_row["timetable"]
    classTimeTable=class_row["timetable"]
    
    



    i=0
    while i<6:
        j=0
        while j<7:
            if lecture_length==1:
                if total_restriction[i][j]==0:
                    total_restriction[i][j]=1
                    classTimeTable[i][j]=1
                    teacherTimeTable[i][j]=1

                    

                    
                    room_index=find_available(room_type,1,i,j)
                    roomTimeTable=rooms.loc[room_index,2]
                    rooms.loc[room_index,2]=roomTimeTable
                    break
            elif j<6:
                if total_restriction[i][j]==0 and total_restriction[i][j+1]==0:
                    total_restriction[i][j]=1
                    total_restriction[i][j+1]=1
                    classTimeTable[i][j]=1
                    classTimeTable[i][j+1]=1
                    teacherTimeTable[i][j]=1
                    teacherTimeTable[i][j+1]=1

                    room_index=find_available(room_type,2,i,j)
                    roomTimeTable=rooms.loc[room_index,2]
                    rooms.loc[room_index,2]=roomTimeTable
                    break
            j+=1
        i+=1

    classes.loc[class_index,6]=classTimeTable
    teachers.loc[teacher_index,2]=teacherTimeTable
    
    sl[subjectid]=sl[subjectid]-1
    classes.loc[class_index,5]=sl
    

    

    
        
        




