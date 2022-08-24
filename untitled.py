test['Age'].loc[(test['Age'] <= 19)] = 0
test['Age'].loc[(test['Age'] > 19 and test['Age'] <= 50)] = 1
test['Age'].loc[(test['Age'] > 50 )] = 2