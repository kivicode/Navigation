import urllib.request as urllib


def makeLink(mode, a='0', b='0'):
    out = 'http://192.168.5.1/web/script.php?mode=' + str(mode) + '&r1=' + str(a).replace(" ", "") + '&r2=' + str(
        b).replace(' ', '')
    return out


def sendRequest(link):
    f = urllib.urlopen(link)
    out = f.read()
    return out


def getCoord(r):
    link = makeLink(r)
    return sendRequest(link)


def setCoord(ca, cb):
    link = makeLink(3, a=str(ca), b=str(cb))
    sendRequest(link)
