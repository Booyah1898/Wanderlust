from flask import Flask,render_template,url_for,flash,redirect,request
from forms import Register,Enquiry, Feedback, Admin_login, Add_pack
from flask_login import login_required
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f1324e414f9dcd52971f749021a21ddd'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sanjkrao'
app.config['MYSQL_PASSWORD'] = 'sanjana'
app.config['MYSQL_DB'] = 'wanderlustv2'

mysql = MySQL(app)

@app.route('/')
@app.route('/home')
@app.route('/destination')
def welcome():
	return render_template('index.html')

@app.route('/about')
def home():
	return render_template('about.html')

@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
	form = Register(request.form)
	if request.method=='POST' and form.validate():
		name = str(form.name.data)
		email = str(form.email.data)
		phone = str(form.phone.data)
		password = str(form.password.data)
		seat_num = str(form.seat_num.data)
		packageID = str(form.packageID.data)
		cur = mysql.connection.cursor()
		row = cur.execute("SELECT * FROM CUSTOMER WHERE (CUST_EMAIL,CUST_NAME) = (%s,%s)",(email,name))
		if row==0:
			cur.execute('INSERT INTO CUSTOMER(CUST_NAME,CUST_EMAIL,CUST_PHONE,DEPEND_NUM,PASSWORD) VALUES(%s,%s,%s,%s,%s)',(name,email,phone,seat_num,password))
			mysql.connection.commit()
		else:
			cur.execute("SELECT PASSWORD FROM CUSTOMER WHERE (CUST_NAME,CUST_EMAIL) = (%s,%s)",(name,email))
			if password!=cur.fetchone()[0]:
				flash(f'Wrong password!','danger')
				return redirect(url_for('register'))
			#flash(f'Account created successfully for {form.name.data}','success')
		cur.execute('SELECT * FROM CUSTOMER WHERE (CUST_EMAIL,CUST_NAME) = (%s,%s)',(email,name))
		custID= str(cur.fetchall()[0][0])
		print(custID)
		cur.execute('INSERT INTO BOOKING(CUST_ID,PACK_ID) VALUES(%s,%s)',(custID,packageID))
		mysql.connection.commit()
		cur.execute('SELECT * FROM BOOKING WHERE (CUST_ID,PACK_ID) = (%s,%s)',(custID,packageID))
		bookID = cur.fetchall()
		print(bookID[0][0])
		if bookID:
			flash(f'Booked package successfully for {form.name.data}.\nBooking ID ={bookID[0][0]} ','success')
		else:
			flash(f'ERROR','danger')
	return render_template('register.html',form = form)



@app.route('/enquiry',methods=['GET','POST'])
def enquiry():
	form = Enquiry(request.form)
	if request.method=='POST' and form.validate():
		email = str(form.email.data)
		password = str(form.password.data)
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM CUSTOMER WHERE (CUST_EMAIL,PASSWORD) = (%s,%s)',(email,password))
		row = cur.fetchone()
		if row==None:
			flash(f'No packages!','danger')
			return redirect(url_for('enquiry'))

		cur.execute("""SELECT P.PACK_ID,CP.COMP_NAME, P.START_LOC, P.DEST_LOC, P.START_DATE, C.DEPEND_NUM,CP.COMP_ID
					FROM BOOKING B, CUSTOMER C, COMPANY CP, PACKAGE P 
					WHERE B.CUST_ID = C.CUST_ID AND B.PACK_ID = P.PACK_ID AND P.COMP_ID = CP.COMP_ID AND (C.CUST_EMAIL,C.PASSWORD) = (%s,%s)""",(email,password))
		packages = cur.fetchall()
		return render_template('booking_enquiry.html',package=packages,cust_email=email)
	return render_template('enquiry.html',form=form) 


@app.route('/packages',methods=['GET'])
def packages():
	cur = mysql.connection.cursor()
	row = cur.execute('SELECT P.PACK_ID, C.COMP_NAME, P.START_LOC, P.DEST_LOC, P.START_DATE, P.DEST_DATE, P.PRICE FROM PACKAGE P, COMPANY C WHERE P.COMP_ID = C.COMP_ID')
	if row==0:
		flash(f'No packages!','danger')
	else:
		#packages = cur.fetchall()
		cur.callproc('find_all')
		packages = cur.fetchall()
		return render_template('packages.html',package=packages)


@app.route('/review',methods=['GET','POST'])
def review():
	form = Feedback(request.form)
	if request.method=='POST' and form.validate():
		booking_id = str(form.booking_id.data)
		rating= str(form.rating.data)
		review = str(form.review.data)
		cur = mysql.connection.cursor()
		row = cur.execute("SELECT * FROM REVIEW R WHERE (R.BID,R.RATING)=(%s,%s)",(booking_id,rating))
		print(row)
		if row!=0:
			flash(f'Package has already been rated!','danger')
		else:
			cur.execute("INSERT INTO REVIEW VALUES(%s,%s,%s)",(booking_id,rating,review))
			mysql.connection.commit()
			cur.close()
			flash(f'Thank you for the feedback!','success')
			return render_template('review.html',form=form)
	return render_template('review.html',form=form)

"""@app.route('/admin_login')
def admin_login():
	form = Admin_login(request.form)
	return render_template('admin_login.html',form=form)"""



@app.route('/rajasthan')
def rajasthan():
	return render_template('rajasthan.html')

@app.route('/kerala')
def kerala():
	return render_template('kerala.html')

@app.route('/goa')
def goa():
	return render_template('goa.html')

@app.route('/karnataka')
def karnataka():
	return render_template('karnataka.html')

@app.route('/mumbai')
def mumbai():
	return render_template('mumbai.html')

@app.route('/ladakh')
def ladakh():
	return render_template('ladakh.html')

@app.route('/kasol')
def kasol():
	return render_template('kasol.html')

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
	form=Admin_login(request.form)
	if request.method=='POST' and form.validate():
		ad_name = str(form.name.data)
		ad_email= str(form.email.data)
		ad_password = str(form.password.data)
		if ad_name=='sanjana' and ad_password=='sanjana':
			return redirect(url_for('admin_option'))
		else:
			flash(f'Wrong credentials try again','danger')
	return render_template('admin_login.html',form=form)

@app.route('/add_Pack',methods=['GET','POST'])
def admin_addPack():
	form = Add_pack(request.form)
	comp_name = str(form.comp_name.data)
	comp_email= str(form.comp_email.data)
	comp_phone = str(form.phone.data)
	comp_phone=str(comp_phone)
	start_loc= str(form.start_loc.data)
	dest_loc= str(form.dest_loc.data)
	start_date= (form.start_date.data)
	end_date= str(form.end_date.data)
	mode = str(form.mode.data)
	seat_num=str(form.mode.data)
	price=str(form.mode.data)
	cur = mysql.connection.cursor()
	if comp_name!='':
		cur.execute('INSERT INTO COMPANY(COMP_NAME,COMP_EMAIL,PHONE) VALUES(%s,%s,%s)',(comp_name,comp_email,comp_phone))
		mysql.connection.commit()
		cur.execute('SELECT COUNT(*) FROM COMPANY')
		comp_id=cur.fetchone()
		print(comp_id)
		cur.execute('INSERT INTO PACKAGE(COMP_ID,START_LOC,START_DATE,DEST_LOC,DEST_DATE,PRICE) VALUES(%s,%s,%s,%s,%s,%s)',(comp_id,start_loc,start_date,dest_loc,end_date,price))
		mysql.connection.commit()
		cur.execute('INSERT INTO ADVERTISEMENT(ADV_NAME,ADV_RATING) VALUES(%s,%s)',(dest_loc,'4'))
		mysql.connection.commit()
		cur.execute('SELECT COUNT(*) FROM ADVERTISEMENT')
		ad_id=cur.fetchone()
		cur.execute('INSERT INTO AD_COMP(ADV_ID,COMP_ID,MODE,SEAT_NUM) VALUES(%s,%s,%s,%s)',(ad_id,comp_id,mode,seat_num))
		mysql.connection.commit()
		flash(f'Updation successful','success')
	return render_template('admin_addPack.html',form=form)

@app.route('/site_stats')
def stats():
	cur = mysql.connection.cursor()
	cur.execute('SELECT CUST_ID,CUST_NAME,CUST_EMAIL,CUST_PHONE FROM CUSTOMER')
	cust = cur.fetchall();
	print(cust)
	cur.execute('SELECT ADV_ID,ADV_NAME,ADV_RATING FROM ADVERTISEMENT')
	ads = cur.fetchall()
	print(ads)
	cur.execute('SELECT COMP_ID,COMP_NAME,COMP_EMAIL,PHONE,COMP_RATING FROM COMPANY')
	comp = cur.fetchall()
	print(comp)
	cur.execute('SELECT C.COMP_NAME, COUNT(*) FROM AD_COMP AC,COMPANY C WHERE C.COMP_ID=AC.COMP_ID GROUP BY(C.COMP_ID)')
	comp_ads = cur.fetchall()
	print(comp_ads)
	return render_template('stats.html',cust=cust,ads=ads,comp=comp,comp_ads=comp_ads)

@app.route('/admin_option')
def admin_option():
	return render_template('admin_option.html')


if __name__=="__main__":
	app.run(debug=True)
