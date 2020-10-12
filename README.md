# StockPrice

* Create directories under root  

git clone https://github.com/ehullander/StockPrice 

data  
model  

From a terminal

$ cd StockPrice   
$ pip install dvc  
$ pip install -r requirements.txt  
$ dvc remote add -d myremote ../../../datasets  
$ dvc pull

Navigate to StockPrice and run Stocks.ipynb  

$ dvc add model  
$ dvc add data  
$ git add .  
