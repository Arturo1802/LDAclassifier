#Libs
import torch
import pandas as pd
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.nn.functional as F
from LDAtools import getT2DataSQL,getFullDataSQL,getNegativeDataSQL
from torch.autograd import Variable 
from sqlalchemy import create_engine 


class Model(nn.Module):
    def __init__(self, in_features=6,h1=6,h2=8,h3=4,h4=2, out_features=3):
        super().__init__()
        self.fc1=nn.LazyLinear(in_features, h1)
        self.fc2=nn.Linear(h1,h2)
        self.fc3=nn.Linear(h2,h3)
        #self.fc4=nn.Linear(h3,h4) 
        self.out=nn.Linear(h3,out_features)
    def forward(self, x):
        x= F.relu(self.fc1(x))
        x= F.relu(self.fc2(x)) 
        x= F.relu(self.fc3(x))
        #x= F.relu(self.fc4(x))
        x= self.out(x)
        return x 
torch.manual_seed(4)
model= Model()

#to cuda device (ROCM rx580 2048sp)
model= model.cuda()
#
#
df=getNegativeDataSQL()  
X= df.drop('preinf',axis=1).drop('#AUTHID',axis=1).drop('TEXT',axis=1).drop('finalinf',axis=1)#.drop('',axis=1)
y= df['preinf']
df=0
X= X.values
print(X)
y=y.values
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test =train_test_split(X,y,test_size=0.2)
X_train=torch.FloatTensor(X_train)
X_test=torch.FloatTensor(X_test)
y_train=torch.LongTensor(y_train)
y_test=torch.LongTensor(y_test)

#to cuda device (ROCM rx580 2048sp)
X_train=X_train.cuda()
y_train=y_train.cuda()

#cross entropy for classification0
criterion=nn.CrossEntropyLoss()
#adam as optimizer
optimizer = torch.optim.Adam(model.parameters(),lr=0.01) 
losses=[]  
try:
    checkpoint = torch.load(f"checkpoint.pth")
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    i = checkpoint['epoch']
    loss = checkpoint['loss']
except:
    loss=1
    i=-1 

while(loss>.20):
    i+=1
    y_pred=model.forward(X_train)
    loss = criterion(y_pred,y_train)
    losses.append(loss.detach().cpu().numpy())
    if i %10 ==0:
        print(f'Epoch: {i}, Loss: {loss}')
    if i%1000==0: 
        if losses[-1]<=losses[0]*.95:
            print("SAVING MODEL")
            torch.save({
            'epoch': i,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, f"./checkpoint.pth")
        losses=[]
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
     