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

def multiply(a1,a2):
    a3=[[i*j for i,j in zip(row1,row2)] for row1,row2 in zip(a1,a2)]
    return a3
def or_op(arrays):
    a3=[[0 for _ in range(len(cr[0][0]))] for _ in range(len(cr[0]))]
    for array in arrays:
        a3=[[i or j for i,j in zip(row1,row2)] for row1,row2 in zip(array,a3)]

    return a3
def matrix_sum(matrix):
    return sum([sum(row) for row in matrix])
def modify_for_2hr(cr):
    m=[[0 for _ in range(len(cr[0]))] for _ in range(len(cr))]
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
    rooms_selected_timetables=rooms[rooms["type"]==room_type]["timetable"].values()
    
    return or_op(rooms_selected_timetables)
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

    if subject_row["lecture_length"]==2:
        class_restriction=modify_for_2hr(class_restriction)
    
    m=multiply(teacher_restriction,class_restriction)
    return multiply(m,room_restriction)
def find_available(room_type):
    room_timetables=rooms["timetable"]
    
    
def assign_subject(subjectid,classid,total_restrictionss):

    class_row=classes[classes["id"]==classid]
    classindex=list(class_row.index)
    subject_row=subjects[subjects["id"]==subjectid]
    room_type=subject_row["room_type"]
    
    teacherid=class_row.st[subjectid]
    lecture_length=class_row.sl[subjectid]

    teacherindex=teachers[teachers["id"]==teacherid].index[0]
    room_id=find_available(room_type)

    
        
        




