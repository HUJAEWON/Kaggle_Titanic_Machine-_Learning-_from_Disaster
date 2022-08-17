import pandas as pd
import numpy as np


# test, train csv 파싱 

train = pd.read_csv("./train.csv")
test = pd.read_csv("./test.csv")



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

def minmax_norm(df_input):
    return (df - df.min()) / ( df.max() - df.min())

df_minmax_norm = minmax_norm(df)

print(df_minmax_norm)



# 여기서 드는 생각 : Age 널값이랑, SibSp 널값을 어떻게 처리하지 ? 
















