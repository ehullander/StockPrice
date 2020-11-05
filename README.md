# StockPrice
# dvc demo
* Create directories under root  

git clone https://github.com/ehullander/StockPrice 


From a terminal

$ cd StockPrice   
$ pip install dvc  
$ pip install -r requirements.txt  
$ dvc remote add -d myremote <absolute path to remote>
$ dvc pull

Navigate to StockPrice and run Stocks.ipynb  

```
$ dvc add model  
$ dvc add data  
$ git add .  
$ dvc run -n evaluate -d getMASE.py -M metrics.json python getMASE.py  
```
