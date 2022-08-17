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
# print(train.isnull().sum())



# Sex male = 1, female = 0
train = train.replace({'Sex':'male'},1)
train = train.replace({'Sex':'female'},0)

test = test.replace({'Sex':'male'},1)
test = test.replace({'Sex':'female'},0)













