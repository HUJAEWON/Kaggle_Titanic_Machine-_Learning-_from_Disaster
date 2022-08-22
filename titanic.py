from asyncio.windows_events import NULL
from cgi import print_arguments
from cmath import nan
import pandas as pd
import numpy as np


# test, train csv 파싱 

train = pd.read_csv("./train.csv")
test = pd.read_csv("./test.csv")


# 칼럼 
# survival	Survival	0 = No, 1 = Yes
# pclass	Ticket class	1 = 1st, 2 = 2nd, 3 = 3rd
# sex	Sex	
# Age	Age in years	
# sibsp	# of siblings / spouses aboard the Titanic	
# parch	# of parents / children aboard the Titanic	
# ticket	Ticket number	
# fare	Passenger fare	
# cabin	Cabin number	
# embarked	Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton



# 잘 파싱 됬나 확인
# print(train.head(5))



# shape 함수로 csv 모양 확인
# (891, 12) = [891 rows x 12 columns]>
# print(train.shape)



# info 함수로 Dtype, 널값 확인
# Age, Cabin 에서 널값 있음
# print(train.info())




# insull, sum 함수로 널값 확인
# Age, Cabin, Embarked 칼럼에서 널값 존재함. 
# Age : 172 , Cabin : 687 , Enbarked : 2 
# print(train.isnull().sum())


# 피쳐 엔지니어링 시작해줌.

# Sex 항목 범주형 변수로 변환
# Sex male = 1, female = 2
train = train.replace({'Sex':'male'},1)
train = train.replace({'Sex':'female'},2)

test = test.replace({'Sex':'male'},1)
test = test.replace({'Sex':'female'},2)



# Parch, SibSp 항목을 더해서 가족수로 새로운 칼럼 만들어줌.
train['FamilyCount'] = train['SibSp'] + train['Parch']
test['FamilyCount'] = test['SibSp'] + test['Parch']



# 사용한 Parch, SibSp 열 드랍(삭제)
del train['Parch']
del train['SibSp']

del test['Parch']
del test['SibSp']


# 추가로 아무상관 없어보이는 Ticket 번호 항목도 열 드랍
del train['Ticket']
del test['Ticket']



# Fare 항목도 정규화 or 표준화 가 필요해보인다. 
# 근데 다시 생각해보니 정규화 보다는 피쳐 비닝(binning 이 적합해보임)

# 값 분포를 보기 위해 describe() 함수로 분포 확인
# print(train["Fare"].describe())

# count    891.000000
# mean      32.204208
# std       49.693429
# min        0.000000
# 25%        7.910400
# 50%       14.454200
# 75%       31.000000
# max      512.329200
# Name: Fare, dtype: float64

# 중위값인 14.454200 값을 기준으로 크면 1, 작으면 0 으로 binning 해줌
# 작은걸 먼저 치환해야 두번째 줄 코드가 작동함.
train['Fare'].loc[(train['Fare'] <= 14.454200)] = 0
train['Fare'].loc[(train['Fare'] > 14.454200)] = 1

test['Fare'].loc[(test['Fare'] <= 14.454200)] = 0
test['Fare'].loc[(test['Fare'] > 14.454200)] = 1


# 여기서 드는 생각 : Age 널값이랑, Cabin 널값을 어떻게 처리하지 ? 

# Age 널값은 Mr, Mrs, Ms, Miss 로 평균값 넣어주면 될 것 같다.
# 일단 Name 컬럼을 Mr = 1, Mrs = 2, Ms = 3 , Miss = 4, 모르면 5 로 바이닝

train['Name'].loc[(train['Name'].str.contains("Mrs") == True)] = 2
train['Name'].loc[(train['Name'].str.contains("Mr") == True)] = 1
train['Name'].loc[(train['Name'].str.contains("Ms") == True)] = 3
train['Name'].loc[(train['Name'].str.contains("Miss") == True)] = 4
train['Name'].loc[(train['Name'].str.contains("()") == True)] = 5

test['Name'].loc[(test['Name'].str.contains("Mrs") == True)] = 2
test['Name'].loc[(test['Name'].str.contains("Mr") == True)] = 1
test['Name'].loc[(test['Name'].str.contains("Ms") == True)] = 3
test['Name'].loc[(test['Name'].str.contains("Miss") == True)] = 4
test['Name'].loc[(test['Name'].str.contains("()") == True)] = 5

# 있는 값중에 평균값 알아보기
Mr_sum = 0
Mr_count = 0
Mrs_sum = 0
Mrs_count = 0
Ms_sum = 0
Ms_count = 0
Miss_sum = 0
Miss_count = 0
Nan_sum = 0
Nan_count = 0

for index, row in train.iterrows():
    if np.isnan(row['Age']) == True:
        pass
    
    elif np.isnan(row['Age']) == False:
        if row["Name"] == 1:
            Mr_sum += row["Age"]
            Mr_count += 1
        elif row["Name"] == 2:
            Mrs_sum += row["Age"]
            Mrs_count += 1
        elif row["Name"] == 3:
            Ms_sum += row["Age"]
            Ms_count += 1
        elif row["Name"] == 4:
            Miss_sum += row["Age"]
            Miss_count += 1
        elif row["Name"] == 5:
            Nan_sum += row["Age"]
            Nan_count += 1


# def average(x,y):
#     return x/y

# Mr_Average = average(Mr_sum,Mr_count)
# Mrs_Average = average(Mrs_sum,Mrs_count)
# Ms_Average = average(Ms_sum,Ms_count)
# Miss_Average = average(Miss_sum,Miss_count)
# Nan_Average = average(Nan_sum,Nan_count)

# print(Mr_Average)
# print(Mrs_Average)
# print(Ms_Average)
# print(Miss_Average)
# print(Nan_Average)

# 32.409774436090224
# 35.642857142857146
# 28.0
# 21.77777777777778
# 19.2701724137931

# 값은 중위값으로 넣어줌.
train['Age'].fillna(train.groupby("Name")['Age'].transform("median"), inplace=True)
test['Age'].fillna(test.groupby("Name")['Age'].transform("median"), inplace=True)

# Embarked 열 어디서 승선햇는지가 상관관게가 없을 것 같으니 Embarked 항목은 drop
del train['Embarked']
del test['Embarked']

# Cabin 항목은 선실의 위치인데 이것은 Ticket 의 가격과 관련이 있으니, 필요 없음.add()

del train["Cabin"]
del test["Cabin"]


# Fare 항목을 2개로 바이닝한것이 조금 세분성이 떨어지는것같지만, 일단 돌려보겟음


# 이제 Age 항목 스케일링이 필요함.
# 청년, 중년 , 장년 정도로 해주면 될 것 같다.
# 어린 순서대로 
train['Age'].loc[(train['Age'] <= 19)] = 0
train['Age'].loc[((train['Age'] > 19) & (train['Age'] <= 50))] = 1
train['Age'].loc[(train['Age'] > 50 )] = 2


test['Age'].loc[(test['Age'] <= 19)] = 0
test['Age'].loc[((test['Age'] > 19) & (test['Age'] <= 50))] = 1
test['Age'].loc[(test['Age'] > 50 )] = 2



# # 바이닝이 잘 되었나 확인
train.to_csv('bining_csv.csv',encoding= "cp949")





