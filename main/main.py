import pickledb
import sqlite3,json,os

def genunit():
    global unitdb
    unitdb=pickledb.load(unitfn,False)
    dat=json.loads('{"usd":["$",["dollar","dollars"],"¢",[100,"cent","cents"]],"eur":["€",["euro","euros"],"¢",[100,"cent","cents"]],"gbp":["£",["pound","pounds"],"p",[100,"pence",null]],"jpy":["¥",["yen",null],null,null],"rub":["₽",["ruble","rubles"],"коп.",[100,"kopek","kopeks"]],"inr":["₹",["rupee","rupees"],"p",[100,"paisa","paise"]],"cny":["¥",["yuan",null],"角",[10,"jiao",null],"分",[100,"fen",null]],"btc":["฿",["bitcoin",null],null,null],"doge":["Ɖ",["dogecoin","dogecoins"]],"mxn":["Mex$",["peso","pesos"],"¢",[100,"centavo","centavos"]],"cad":["CAD$",["canadian dollar","canadian dollars"],"¢",[100,"cent","cents"]],"aud":["AUD$",["australian dollar","australian dollars"],"¢",[100,"cent","cents"]],"ltc":["Ł",["litecoin",null],null,null]}')
    for k in dat:
        v=dat[k]
        unitdb.set(k,v)
    unitdb.dump()
    return None

def gendb():
    try:
        c=conn.cursor()
        c.execute("CREATE TABLE money (user text, usd int, eur int, gbp int, jpy int, rub int, inr int, cny int, mxn int, cad int,aud int)")
        c.execute("CREATE TABLE crypto (user text, btc real, doge int,ltc real)")
        conn.commit()
    except:
        pass
    genunit()
    return None

def newbal(usr,*,zero=False):
    def qm(l,*,char="?"):
        char+=","
        s=char*len(l)
        s=s[:len(s)-1]
        return f"({s})"
    c=conn.cursor()
    l=(usr,100000,82696,71586,10673750,7379850,7325270,647060,2061050,126360,128427)
    ll=(usr,0.021,1942481,5.33)
    if zero:
        l=dozero(l)
        ll=dozero(ll)
    c.execute(f"INSERT INTO money VALUES {qm(l)}",l)
    c.execute(f"INSERT INTO crypto VALUES {qm(ll)}",ll)
    conn.commit()
    return None

def getbal(usr,cur="usd",*,text=False):
    cur=cur.lower()
    c=conn.cursor()
    try:
        if not cur in cryptl:
            res=list(c.execute(f'SELECT {cur} FROM money WHERE user=?',(usr,)))[0][0]
        else:
            res=list(c.execute(f"SELECT {cur} FROM crypto WHERE user=?",(usr,)))[0][0]
        if not cur in reall:
            res=res/100
        if text:
            res=totxt(res,cur)
        return res
    except IndexError:
        newbal(usr)
        return getbal(usr,cur,text=text)

def setbal(usr,v,cur="usd"):
    c=conn.cursor()
    if not (usr,) in list(c.execute("SELECT user FROM money")):
        newbal(usr)
    cur=cur.lower()
    if not cur in reall:
        v=int(v*100)
    if not cur in cryptl:
        c.execute(f"UPDATE money SET {cur}=? WHERE user=?",(v,usr))
    else:
        c.execute(f"UPDATE crypto SET {cur}=? WHERE user=?",(v,usr))
    conn.commit()
    return v

def minusbal(usr,v,cur="usd"):
    cur=cur.lower()
    if not cur in reall:
        v=int(v*100)
        bal=int(getbal(usr,cur)*100)
    else:
        bal=getbal(usr,cur)
    bal=bal-v
    if not cur in reall:
        bal=bal/100
    setbal(usr,bal)
    return bal

def addbal(usr,v,cur="usd"):
    cur=cur.lower()
    if not cur in reall:
        v=int(v*100)
        bal=int(getbal(usr,cur)*100)
    else:
        bal=getbal(usr,cur)
    bal=bal+v
    if not cur in reall:
        bal=bal/100
    setbal(usr,bal)
    return bal

def totxt(n,cur="usd"):
    cur=cur.lower()
    if not cur in reall:
        n=str(round(float(n),2)).split(".")
        x=n[1]
        while len(x)<2:
            x+=str(0)
        n[1]=x
        n=".".join(n)
    else:
        n=str(float(n))
    s=unitdb.get(cur)[0]
    return s+n

def dozero(l):
    tl=[]
    for i in l:
        if type(i)==int:
            tl.append(0)
        elif type(i)==float:
            tl.append(float(0))
        else:
            tl.append(i)
    return tuple(tl)

def baldict(usr,*,json_out=False,indent=None,text=False):
    if text:
        c=conn.cursor()
        l=list(c.execute("SELECT * FROM money WHERE user=?",(usr,)))[0][1:]
        ll=list(c.execute("SELECT * FROM crypto WHERE user=?",(usr,)))[0][1:]
        res={"money":{"usd":totxt(l[0]/100,"usd"),"eur":totxt(l[1]/100,"eur"),"gbp":totxt(l[2]/100,"gbp"),"jpy":totxt(l[3]/100,"jpy"),"rub":totxt(l[4]/100,"rub"),"inr":totxt(l[5]/100,"inr"),"cny":totxt(l[6]/100,"cny"),"mxn":totxt(l[7]/100,"mxn"),"cad":totxt(l[8]/100,"cad"),"aud":totxt(l[9]/100,"aud")},"crypto":{"btc":totxt(ll[0],"btc"),"doge":totxt(ll[1]/100,"doge"),"ltc":totxt(ll[2],"ltc")}}
    else:
        c=conn.cursor()
        l=list(c.execute("SELECT * FROM money WHERE user=?",(usr,)))[0][1:]
        ll=list(c.execute("SELECT * FROM crypto WHERE user=?",(usr,)))[0][1:]
        res={"money":{"usd":l[0]/100,"eur":l[1]/100,"gbp":l[2]/100,"jpy":l[3]/100,"rub":l[4]/100,"inr":l[5]/100,"cny":l[6]/100,"mxn":l[7]/100,"cad":l[8]/100,"aud":l[9]/100},"crypto":{"btc":ll[0],"doge":ll[1]/100,"ltc":ll[2]}}
    if not json_out:
        return res
    else:
        if indent!=None:
            return json.dumps(res,indent=indent,ensure_ascii=False)
        else:
            return json.dumps(res)

def main(*,new=False):
    global conn
    if new:
        for f in [bankfn,unitfn]:
            try:
                os.remove(os.path.join(".",f))
            except FileNotFoundError:
                pass
    conn=sqlite3.connect(bankfn)
    c=conn.cursor()
    gendb()
    newbal("blank")
    newbal("zero",zero=True)
    print(baldict("blank",json_out=True,indent=2,text=True))
    print(getbal("blank","btc",text=True))
    print(getbal("blank","rub",text=True))
    conn.close()
    print("Done!!!")

#constants
bankfn="bank.sqlite3"
unitfn="money.pickledb"
cryptl=["btc","doge","ltc"]
reall=["btc","ltc"]

debug=True

if __name__=="__main__":
    main(new=debug)