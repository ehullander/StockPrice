# StockPrice
# dvc demo
* Create directories under root  

git clone https://github.com/ehullander/StockPrice 


From a terminal

```
$ cd StockPrice   
$ pip install dvc  
$ pip install -r requirements.txt  
$ dvc remote add -d myremote <absolute path to remote>
$ dvc pull 
$ dvc run -n evaluate -d getMASE.py -M metrics.json python getMASE.py  
$ git add dvc.lock dvc.yaml
$ dvc add model  
$ dvc add data  
$ git add . 
```
