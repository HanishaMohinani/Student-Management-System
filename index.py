from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import numpy as np
import matplotlib.pyplot as plt
import requests
import bs4
from sqlite3 import *

#---------------------------------user defined exception classes-------------------

class DataException(Exception):
	def __init__(self,msg):
		self.msg=msg

#---------------------------------------functions--------------------------------

def f1():     					#from main window to add window
	add_window.deiconify()
	main_window.withdraw()

def f2():              				#from main window to view
	view_window.deiconify()
	main_window.withdraw()
	view_st_data.delete(1.0,END)
	info=''
	con=None
	try:
		con=connect('student_db')
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		data.sort()
		for d in data:
			info=info+"rno = "+str(d[0])+ " name = " +str(d[1]) +" marks = "+str(d[2])+"\n\n"
		view_st_data.insert(INSERT,info)
	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def f3():					#from main window to update 
	update_window.deiconify()
	main_window.withdraw()

def f4():					#from main window to delete
	delete_window.deiconify()
	main_window.withdraw()

def f5():					#from main window to charts
	con=None
	try:
		con=connect('student_db')
		cursor=con.cursor()
		sql='select * from student'					
		cursor.execute(sql)
		data=cursor.fetchall()
		student_names=[]
		student_marks=[]
		for d in data:
			student_names.append(str(d[1]))
			student_marks.append(int(d[2]))
		plt.bar(student_names,student_marks,linewidth=2.5)
		plt.xlabel("Student Names")
		plt.ylabel("Marks")
		plt.title("Batch Information")
		plt.show()
	except Exception as e:
		showerror('Failure',e)
	finally:
		if con is not None:
			con.close()	

def f6():					#from add window to main window (back btn)
	main_window.deiconify()
	add_window.withdraw()	

def f7():					#from view window to main window  (back btn)
	main_window.deiconify()
	view_window.withdraw()

def f8():
	main_window.deiconify()			#from update window to main window  (back btn)
	update_window.withdraw()

def f9():					#from delete window to main window  (back btn)
	main_window.deiconify()
	delete_window.withdraw()

def f10():					#add window save buttton
	con=None
	try:
		con=connect('student_db')
		cursor=con.cursor()
		sql="insert into student values('%d','%s','%d')"
		if add_ent_rno.get().isalpha():
			raise DataException("Roll no should be a number")
		if add_ent_rno.get() == '':
			raise DataException("Roll no shouldn't be empty")
		rno=int(add_ent_rno.get())
		if rno<0:
			add_ent_rno.delete(0,'end')
			add_ent_name.delete(0,'end')
			add_ent_marks.delete(0,'end')
			add_ent_rno.focus()
			raise DataException('Roll no should be positive')
		elif rno==0:
			add_ent_rno.delete(0,'end')
			add_ent_name.delete(0,'end')
			add_ent_marks.delete(0,'end')
			add_ent_rno.focus()
			raise DataException("Roll no shouldn't be 0")
		name=add_ent_name.get()
		if name == '':
			raise DataException("Name shouldn't be empty")
		if len(name)<2 or all(chr.isalpha() or chr.isspace() for chr in name)==False:
			add_ent_rno.delete(0,'end')
			add_ent_name.delete(0,'end')
			add_ent_marks.delete(0,'end')
			add_ent_rno.focus()
			raise DataException('Invalid Name')
		if add_ent_marks.get().isalpha():
			raise DataException("Marks should be a number")
		if add_ent_marks.get() == '':
			raise DataException("Marks shouldn't be empty")
		marks=int(add_ent_marks.get())
		if marks<0 or marks>100:
			add_ent_rno.delete(0,'end')
			add_ent_name.delete(0,'end')
			add_ent_marks.delete(0,'end')
			add_ent_rno.focus()
			raise DataException("Marks should be between 0 to 100")
		cursor.execute(sql % (rno,name,marks))
		con.commit()
		showinfo('Success','Student added')
		add_ent_rno.delete(0,'end')
		add_ent_name.delete(0,'end')
		add_ent_marks.delete(0,'end')
		add_ent_rno.focus()

	except DataException as e:
		showerror('Improper',e.msg)

	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def f11():					#save button in update window
	con=None
	try:
		con=connect('student_db')
		cursor=con.cursor()
		sql="update student set name='%s',marks='%d' where rno='%d' "
		if update_ent_rno.get().isalpha():
			raise DataException("Roll no should be a number")
		if update_ent_rno.get() == '':
			raise DataException("Roll no shouldn't be empty")
		rno=int(update_ent_rno.get())
		if rno<0:
			update_ent_rno.delete(0,'end')
			update_ent_name.delete(0,'end')
			update_ent_marks.delete(0,'end')
			update_ent_rno.focus()
			raise DataException('Roll no should be positive')
		name=update_ent_name.get()
		if name == '':
			raise DataException("Name shouldn't be empty")
		if len(name)<2 or all(chr.isalpha() or chr.isspace() for chr in name)==False:
			update_ent_rno.delete(0,'end')
			update_ent_name.delete(0,'end')
			update_ent_marks.delete(0,'end')
			update_ent_rno.focus()
			raise DataException('Invalid Name')
		if update_ent_marks.get().isalpha():
			raise DataException("Marks should be a number")
		if update_ent_marks.get() == '':
			raise DataException("Marks shouldn't be empty")
		marks=int(update_ent_marks.get())
		if marks<0 or marks>100:
			update_ent_rno.delete(0,'end')
			update_ent_name.delete(0,'end')
			update_ent_marks.delete(0,'end')
			update_ent_rno.focus()
			raise DataException("Marks should be between 0 to 100")
		cursor.execute(sql % (name,marks,rno))
		if cursor.rowcount>0:
			con.commit()
			showinfo('Success','Student Updated')
		else:
			showerror('Failure',"Record doesn't exists")
		update_ent_rno.delete(0,'end')
		update_ent_name.delete(0,'end')
		update_ent_marks.delete(0,'end')
		update_ent_rno.focus()

	except DataException as e:
		showerror('Improper',e.msg)

	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:
		if con is not None:
			con.close()
			
def f12():					#save button in delete window
	con=None
	try:
		con=connect('student_db')
		cursor=con.cursor()
		sql="delete from student where rno='%d' "
		if delete_ent_rno.get().isalpha():
			raise DataException("Roll no should be a number")
		if delete_ent_rno.get() == '':
			raise DataException("Roll no shouldn't be empty")
		rno=int(delete_ent_rno.get())
		if rno<0:
			delete_ent_rno.delete(0,'end')
			delete_ent_rno.focus()	
			raise DataException('Roll no should be positive')
		cursor.execute(sql % (rno))
		if cursor.rowcount > 0:
			con.commit()
			showinfo('Success','Record deleted')
		else:
			showerror('Failure',"Record doesn't exists")
		delete_ent_rno.delete(0,'end')
		delete_ent_rno.focus()

	except DataException as e:
		showerror('Improper',e.msg)

	except Exception as e:
		showerror('Failure',e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

def f13():					#quote of the day scraping
	web_address='https://www.brainyquote.com/quote_of_the_day'
	result=requests.get(web_address)
	data=bs4.BeautifulSoup(result.text,'html.parser')
	info=data.find('img',{'class':'p-qotd'})
	msg=info['alt']
	format_msg=msg.split('-')
	msg='QOTD:  '+'\n'.join(format_msg)
	return msg

def f14():					#location web scraping
	try:
		wa="https://ipinfo.io/"
		res=requests.get(wa)
		data=res.json()
		city_name=data['city']
		a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
		a2="&q="+city_name
		a3="&appid="+"c6e315d09197cec231495138183954bd"	
		wa2=a1+a2+a3
		res2=requests.get(wa2)
		data2=res2.json()
		tempt=data2['main']['temp']
		tempt=str(tempt)+chr(176)+'C'
		return city_name,tempt
	except Exception as e:
		showerror('Failure',e)
	
#---------------------------------------main window-------------------------------

main_window=Tk()
main_window.title("S.M.S")
main_window.geometry('600x600+400+100')
main_window.config(bg='#d3e0ea')

quote=f13()					#calling function f13
tup=f14()
city_name=tup[0]
temperature=tup[1]

font1=('Arial',20,'bold')
add_btn=Button(main_window,text='Add',font=font1,width=10,command=f1,bg='#1687a7')
view_btn=Button(main_window,text='View',font=font1,width=10,command=f2,bg='#1687a7')
update_btn=Button(main_window,text='Update',font=font1,width=10,command=f3,bg='#1687a7')
delete_btn=Button(main_window,text='Delete',font=font1,width=10,command=f4,bg='#1687a7')
chart_btn=Button(main_window,text='Charts',font=font1,width=10,command=f5,bg='#1687a7')
lt_lb=Label(main_window,text='Location: '+city_name+'\nTemperature: '+temperature ,font=('Arial',13),width=30,bg='#d3e0ea')
quote_label = Label(main_window,text=quote,font=('Arial',13),width=65,bg='#d3e0ea')

add_btn.pack(pady=10)
view_btn.pack(pady=10)
update_btn.pack(pady=10)
delete_btn.pack(pady=10)
chart_btn.pack(pady=10)
quote_label.pack(pady=10)
lt_lb.pack(pady=10)

#--------------------------------------add window---------------------------------

add_window=Toplevel(main_window)
add_window.title('Add Student')
add_window.geometry('600x600+400+100')
add_window.config(bg='#d3e0ea')

add_lb_rno=Label(add_window,text='Enter rno:',font=font1,bg='#d3e0ea')
add_lb_name=Label(add_window,text='Enter name:',font=font1,bg='#d3e0ea')
add_lb_marks=Label(add_window,text='Enter marks:',font=font1,bg='#d3e0ea')
add_ent_rno=Entry(add_window,bd=5,font=font1)
add_ent_name=Entry(add_window,bd=5,font=font1)
add_ent_marks=Entry(add_window,bd=5,font=font1)
add_btn_save=Button(add_window,text='Add',font=font1,width=10,command=f10,bg='#1687a7')
add_btn_back=Button(add_window,text='Back',font=font1,width=10,command=f6,bg='#1687a7')

add_lb_rno.pack(pady=10)
add_ent_rno.pack(pady=10)
add_lb_name.pack(pady=10)
add_ent_name.pack(pady=10)
add_lb_marks.pack(pady=10)
add_ent_marks.pack(pady=10)
add_btn_save.pack(pady=10)
add_btn_back.pack(pady=10)

add_window.withdraw()

#--------------------------------------view window-----------------------------------

view_window=Toplevel(main_window)
view_window.title('View Students')
view_window.geometry('600x600+400+100')
view_window.config(bg='#d3e0ea')

view_st_data=ScrolledText(view_window,width=35,height=15,font=('Arial',18,'bold'))
view_btn_back=Button(view_window,text='Back',font=font1,command=f7,bg='#1687a7')

view_st_data.pack(pady=10)
view_btn_back.pack(pady=10)

view_window.withdraw()

#---------------------------------------update window---------------------------------
update_window=Toplevel(main_window)
update_window.title('Update Student')
update_window.geometry('600x600+400+100')
update_window.config(bg='#d3e0ea')

update_lb_rno=Label(update_window,text='Enter rno:',font=font1,bg='#d3e0ea')
update_lb_name=Label(update_window,text='Enter name:',font=font1,bg='#d3e0ea')
update_lb_marks=Label(update_window,text='Enter marks:',font=font1,bg='#d3e0ea')
update_ent_rno=Entry(update_window,bd=5,font=font1)
update_ent_name=Entry(update_window,bd=5,font=font1)
update_ent_marks=Entry(update_window,bd=5,font=font1)
update_btn_save=Button(update_window,text='Update',font=font1,width=10,command=f11,bg='#1687a7')
update_btn_back=Button(update_window,text='Back',font=font1,width=10,command=f8,bg='#1687a7')

update_lb_rno.pack(pady=10)
update_ent_rno.pack(pady=10)
update_lb_name.pack(pady=10)
update_ent_name.pack(pady=10)
update_lb_marks.pack(pady=10)
update_ent_marks.pack(pady=10)
update_btn_save.pack(pady=10)
update_btn_back.pack(pady=10)

update_window.withdraw()
#------------------------------------delete window---------------------------------
delete_window=Toplevel(main_window)
delete_window.title('Delete Student')
delete_window.geometry('600x600+400+100')
delete_window.config(bg='#d3e0ea')

delete_lb_rno=Label(delete_window,text='Enter rno:',font=font1,bg='#d3e0ea')
delete_ent_rno=Entry(delete_window,bd=5,font=font1)
delete_btn_save=Button(delete_window,text='Delete',font=font1,width=10,bg='#1687a7',command=f12)
delete_btn_back=Button(delete_window,text='Back',font=font1,width=10,bg='#1687a7',command=f9)

delete_lb_rno.pack(pady=10)
delete_ent_rno.pack(pady=10)
delete_btn_save.pack(pady=10)
delete_btn_back.pack(pady=10)

delete_window.withdraw()

main_window.mainloop()