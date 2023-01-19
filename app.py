from flask import Flask, render_template,request
import sqlite3 as sql


app = Flask(__name__)

l=[]
@app.route("/")
def display():
    conn=sql.connect("shop.db")
    cur=conn.cursor()
    cur.execute("select * from buyer")
    a=cur.fetchall()
    for i in a:
        dic={"name":i[0],"mobile":i[1],"amount":i[2]}
        l.append(dic)
    return render_template("display.html",data=l)


lis=[]
@app.route("/product")
def product():
    conn=sql.connect("shop.db")
    cur=conn.cursor()
    cur.execute("select*from product")
    a=cur.fetchall()
    for i in a:
        d={"product_name":i[0],"price":i[1]}
        lis.append(d)
    return render_template("display.html",data=lis)


@app.route("/home",methods=['POST','GET'])
def show():
    if request.form.get("user_name")!=None:
        name=request.form.get("user_name")
        mobile=request.form.get("mobile_number")
        product=request.form.get("product_name")
        quantity=request.form.get("quantity")
        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("insert into purchase(user_name,mobile_number,product_name,quantity) values(?,?,?,?)",(name,mobile,product,quantity))
        conn.commit()

        cur.execute("select price from product where product_name=?",(product,))
        minus=cur.fetchall()
        minus=minus[0][0]
        quantity=int(quantity)
        minus=minus*quantity

        cur.execute("update buyer set amount=amount-? where mobile=?",(minus,mobile))
        conn.commit()

        le=[]
        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("select * from buyer")
        a=cur.fetchall()
        for i in a:
            di={"name":i[0],"mobile":i[1],"amount":i[2]}
            le.append(di)
        return render_template("display.html",data=le)
    return render_template("index.html")


    

if __name__=="__main__":
    app.run(debug=True)