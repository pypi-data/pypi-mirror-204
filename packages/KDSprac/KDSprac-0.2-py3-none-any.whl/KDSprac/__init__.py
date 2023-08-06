def KDS1():
    print("""
    
Write MongoDB query to :
1) Create, display and drop Database 
2) Create, display and drop Collection
3) Insert, display, update and delete a document

1)Create, display and drop Database
 Create a database 
 Syntax: use database_name 
 Display databases 
 Syntax: show dbs 
 Drop database 
 Syntax: db.database_name.drop()

2) Create, display and drop Collection
 Create a collection 
 Syntax : db.createCollection("collection_name")
 Display Collections 
 Syntax: show collections
 Drop Collection 
 Syntax: db.collection_name.drop()

3) Insert, display, update and delete a document

 Insert a document ( insertOne )
 Syntax: db.collection_name.insert({"name"})
 Insert more than one document ( insertMany ) 
 Syntax: db.collection_name.insertMany({"name1"}, {"name2"})
 Display documents 
 Syntax: db.collection_name.find() 
 Delete a document 
 Syntax: db.collection_name.remove({"deletion_criteria"}) 

    
    """)

def KDS2():
    print(""" 
    
Write MongoDB query to perform :
a)	Projection
b)	Limit
c)	Skip
d)	Sort
e)	Indexes


a)	Projection
Syntax: db.collection_name.find({ },{"key":"value"})

b)	Limit Syntax:
db.collection_name.find("key":"value").limit(value)
 

c)	Skip Syntax:
db.collection_name.find("key":"value").skip(value) 

d)	Sort Syntax:
db.collection_name.find("key":"value").sort("key":"value)
 
e)	Indexes Syntax:
To create an index:-> 
    db.collection_name.createIndex({"key":"index_value"}) 
To display/view indexes:-> db.collection_name.getIndexes()
To delete indexes:-> db.collection_name.dropIndexes()

    """)

def KDS3():
    print("""
R Studio -> new Project -> new Directory -> new Project 

data("iris")
names(iris)
new_data<- subset(iris,select = c(-Species))
new_data
cl<-kmeans(new_data,3)
cl
data<-new_data
wss<-sapply(1:15,function(k){kmeans(data,k) $tot.withinss})
wss
plot(1:15,wss,type="b",pch=19,frame=FALSE,xlab="Number of cluster k", ylab="Total within_clusters
     sum of squares")
install.packages("cluster")
library(cluster)
clusters<-hclust(dist(iris[,3:4]))
plot(clusters)
clusterCut<-cutree(clusters,3)
table(clusterCut,iris$Species)

        """)
    
def KDS4():
    print("""
data("AirPassengers")
class(AirPassengers)
start(AirPassengers)
end(AirPassengers)
frequency(AirPassengers)
summary(AirPassengers)
plot(AirPassengers)
abline(reg = lm(AirPassengers~time(AirPassengers)))
cycle(AirPassengers)
plot(aggregate(AirPassengers,FUN=mean))
boxplot(AirPassengers~cycle(AirPassengers))
    
       """)
    
def KDS5():
    print(""" 
CODE:

ftest<- read.csv(file.choose(), sep=",", header=T)
var.test(ftest$time_g1,ftest$time_g2,alternative="two.sided")

"one way anova"
data1<-read.csv(file.choose(),sep = ",", header = T)
names(data1)
summary(data1)
head(data1)
anv<-aov(formula = satindex~dept,data=data1)
summary(anv)

"two way anova"
data2<-read.csv(file.choose(),sep = ",", header = T)
names(data2)
summary(data2)
anv1<-aov(formula = satindex~dept+exp+dept*exp,data=data2)
summary(anv1)
  
    
    
    """)

def KDS6():
    print("""

Code: 

"testfor normal distrbution"
data1<- read.csv(file.choose(),sep=",",header=T)
shapiro.test(data1$C1)

"one sample t test"
apple<-read.csv(file.choose(),sep=",",header = T)
summary(apple)
t.test(apple$C1, alternative="greater", mu=97)

"independent t test"
time<-read.csv(file.choose(),sep=",",header = T)
summary(time)

"paired t test"
time1<-read.csv(file.choose(),sep = ",", header = T)
t.test(time1$HtFt,time1$HtBk, alternative = "greater", paired = T)

"t test for variance"
var<-read.csv(file.choose(), sep = ",", header = T)
summary(var)
var.test(var$X1, var$X2, alternative ="two.sided")
    
    
    """)

def KDS7():
    print(""" 
CODE:

height<-c(102,117,105,141,135,115,138,144,137,100,131,119,115,121,113)
weight<-c(61,46,62,54,60,69,51,50,46,69,48,56,64,48,59)
student<-lm(weight~height)student
predict(student,data.frame(height=199),interval="confidence")
plot(student)
    
    """)

def KDS8():
    print(""" 

Code:
library(rpart)
install.packages('rattle')
install.packages('rpart.plot')
install.packages('RColorBrewer')
library(rattle)
library(rpart.plot)
library(RColorBrewer)
hitters<-read.csv(file.choose(),sep=",",header = T)
summary(hitters)
reg.tree <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked,data=hitters,method="class")
#reg.tree <- rpart(Salary ~ Years + Hits, data = hitters)
rpart.plot(reg.tree, type = 4)
reg.tree$variable.importance
install.packages("MASS")
library(MASS)
#set.seed(1984)
library(rpart)
train <- sample(1:nrow(hitters), nrow(hitters)/2)
tree_baseball <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked,data=hitters)
#tree_baseball <- rpart(Salary ~ Hits + HmRun + Runs + RBI + Walks + Years + Errors, subset = train, data = hitters)
library(rpart.plot)
rpart.plot(tree_baseball)
tree_baseball$variable.importance
    
    
    """)

def KDS9():
    print(""" 

loan<-read.csv(file.choose(),header=T,sep=",")
head(loan)
summary(loan)
str(loan)
loan$AGE<-as.factor(loan$AGE)
str(loan)
names(loan)
"creating model1"
model1<-glm(DEFAULTER~.,family=binomial,data=loan)
summary(model1)
"global testing for the acceptance of the model"
null<-glm(DEFAULTER~1,family=binomial,data=loan)
anova(null,model1,test="chisq")
"predicting the probilities"
loan$predprob<-round(fitted(model1),2)
head(loan)
"classification and misclassification analysis"
table(loan$DEFAULTER,fitted(model1)>0.5)
sens<-95/(89+95)*100
sens
spc<-478/(478+39)*100
spc

"check the trade off between sensitivity and specificity using different cut off values"
table(loan$DEFAULTER,fitted(model1)>0.1)
table(loan$DEFAULTER,fitted(model1)>0.2)
table(loan$DEFAULTER,fitted(model1)>0.3)
table(loan$DEFAULTER,fitted(model1)>0.4)
table(loan$DEFAULTER,fitted(model1)>0.5)


"goodness of fit using reciver operationl curver"
pred<-predict(model1,loan,type="response")
install.packages("ROCR")
library(ROCR)
rocrpred<-prediction(pred,loan$DEFAULTER)
rocrperf<-performance(rocrpred,"tpr","fpr")
"to check proper cut off point"
plot(rocrperf,colorize=TRUE,print.cutoffs.at=seq(0.1,by=0.1))
"to check coeficients"
coef(model1)
exp(coef(model1))
    
    """)

def KDS10():
    print(""" 

Aim:  Parsing of xml text
Source Code:-
importcsv
import requests
importxml.etree.ElementTree as ET

defloadRSS():
url = 'https://www.w3schools.com/xml/simple.xml'

resp = requests.get(url)

with open('topnewsfeed.xml' , 'wb') as f:
f.write(resp.content)

defparseXML(xmlfile):

tree = ET.parse(xmlfile)

root = tree.getroot()

newsitems = []

for item in root.findall('./food'):

news = {}

for child in item:
news[child.tag] = child.text.encode('utf8')

newsitems.append(news)

returnnewsitems

defsavetoCSV(newsitems, filename):

fields = ['name' , 'price' , 'description' , 'calories']

with open(filename, 'w') as csvfile:

writer = csv.DictWriter(csvfile, fieldnames = fields)

writer.writeheader()

writer.writerows(newsitems)

def main():
loadRSS()

newsitems = parseXML('topnewsfeed.xml')

print(newsitems)

savetoCSV(newsitems, 'topnews.csv')

if __name__ == "__main__":

main()

    
    
    """)