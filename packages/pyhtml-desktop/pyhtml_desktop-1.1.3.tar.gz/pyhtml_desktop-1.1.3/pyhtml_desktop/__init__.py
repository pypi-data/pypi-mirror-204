import tkinter as tk
import tkinter.font
from bs4 import BeautifulSoup as bs4
import re,sys




global _funcs
_funcs = {}

def load(fname):
	global soup,data,gsty,p_elm
	with open(fname) as f:
		data = f.read().replace('<br>','::br')
	soup = bs4(data,'html.parser')

	gsty = pcss(soup.find('style').text)
	p_elm = get_p()
def get_p():
	xs = soup.find('body').findChildren(recursive=True)
	res = []
	for x in xs:
		csty = x['style'].split(';') if 'style' in x.attrs.keys() else []
		ccl = x['onclick'] if 'onclick' in x.attrs.keys() else ""
		cid = x['id'] if 'id' in x.attrs.keys() else None

		res.append({'text':x.text,'elm':x.name,'style':csty,'id':cid,'onclick':ccl})
	return res


iso = lambda d: [x.replace('\n','') for x in re.findall(r'\S+{[\S\s]*?}',d)]

def clear_all():
	for el in ce:
		el.tk.destroy()
def delm(ind):
	for eli in range(0,len(ce)): 
		ce[eli].tk.destroy()

def update(ind,atr,val):
	delm(ind)
	p_elm[ind][atr]= val

def get(ind):
	return p_elm[ind]
def pcss(c):
  y = iso(c)
  res = []
  for r in y:
    res.append([
      re.search(r'\S+?{',r).group(0)[:-1],
      re.search(r'{[\S\s]*?}',r).group(0),
    ])
  res2 = {}
  for r2 in res:
    res2[r2[0]]=\
      [n.replace('}','').replace('{','').strip() \
                                    for n in r2[1].split(';')]
    if '' in res2[r2[0]]: 
      res2[r2[0]].remove('')
  return res2

fsz = {"h1":32,'h2':24,'h3':21,'h4':16,'p':16,'button':16}
def up(_):
	#global wheight, wwidth
    sys.modules[__name__].wwidth = main.winfo_width()
    sys.modules[__name__].wheight = main.winfo_height()


def init():
	global main
	main = tk.Tk()
	main.configure(background='white')
	main.option_add('*font','lucida 11')

	main.bind("<Configure>",up)

	main.minsize(500,500)
	main.title(soup.find('title').text)

	
class elm:
	def __init__(self,text,x,y,fsi=11,at={},pt={},typ=tk.Label):
		self.sty_attrs = {'text':text,'bg':'white','fg':'black','font':('lucida',fsi),**at}
		self.pos_attrs = {'x':x,'y':y,**pt}
		self.tk = typ(**self.sty_attrs)
		self.fsize = tk.font.Font(font=f'lucida {fsi}').metrics('linespace')

	def render(self):
		self.tk.place(**self.pos_attrs)





global ce
ce = []
def parse_style(s):
	catr = {}
	patr = {}
	mgn = 0
	display = True
	for sty in s:

		pr = sty.split(':')
		if pr[0] == 'color':
			catr['fg'] = pr[1]
		if pr[0] == 'background-color':
			catr['bg'] = pr[1]
		if pr[0] == 'margin':
			mgn = int(pr[1].replace('px',''))
		if pr[0] == 'left':
			patr['x'] = int(pr[1])
		if pr[0] == 'top':
			patr['y'] = int(pr[1])
		if pr[0] == 'display' and pr[1] == 'none':
			display = False
	return catr,mgn,patr,display

	
global y


y = 0
mgn = 0
def render():
	global y,mgn
	for el in p_elm:
		print('--')
		y+=mgn if len(ce) > 0 else 0
		print(el['text'].split('::br'))
		

		for tx2 in el['text'].split('::br'):
			tx = tx2.replace('\n','')
			catr1,mgn1,patr1,disp1 = parse_style(el['style'])
			if el['id'] != None and "#"+el['id'] in gsty:

				catr2,mgn2,patr2,disp2 = parse_style(gsty["#"+el['id']])

				catr = {**catr1,**catr2}
				patr = {**patr1, **patr2}
				mgn = mgn1 or mgn2
				disp = disp2 or disp1
			else:
				mgn = mgn1
				catr = catr1
				patr = patr1
				disp = disp1
			if el['elm'] == "button":
				onclck = el['onclick']
				print(';',_funcs[onclck])
				catr['command'] = lambda:_funcs[onclck]()
			print('!!!!!',catr)
			celm = elm(tx,0,y,fsz[el['elm']],catr,patr,(tk.Label if el['elm'] != "button" else tk.Button))
			ce.append(celm)
			if disp:
				ce[-1].render()
				y+=ce[-1].fsize
		y += mgn
		print('-')

		if type(ce[-1].tk) == tk.Button:

			y += 10


	main.mainloop()




	
def _bind(func,name):
	_funcs[name]=func


def find_by_id(id_):
	for i in range(len(p_elm)):
		if p_elm[i]['id'] == id_:
			return i

def find_by_tag(tag):
	r = []
	for i in range(len(p_elm)):
		if p_elm[i]['elm'] == tag:
			r.append(i)
	return r
def bind(nm):
	def _func(f):
		def intr():
			global y
			y= 0
			f()
			render()	
		_bind(intr,nm)
		return intr

	return _func




