import urllib.request as urllib

link = "http://127.0.0.1/script.php?p1=[10,20]&p2=[0,1]"
f = urllib.urlopen(link)
myfile = f.read()
print(myfile)