class Juiy :
	"""
	คลาส จุ้ย คือ
	เป็นข้อมูลเกี่ยวกับจุ้ย เประกอบด้วย ชื่อเฟส
	ชื่อ ig

	EX.
	juiy = Juiy()
	juiy.show_name()
	juiy.show_IG()
	juiy.about()
	juiy.show_Art()
	juiy.show_page()
	"""

	def __init__(self) :
		self.name = 'จุ้ย'
		self.facebook = 'https://www.facebook.com/pakkapon.lertpanyawut'

	def show_name(self):
		print('สวัสดีฉันชื่อ {}'.format(self.name,self.facebook))

	def show_IG(self):
		print('https://www.instagram.com/_2missu/')

	def about(self):
		text = """
		สวัสดี ชื่อจุ้ย เป็นผู้ชาย อายุ 25 ปี กำลังทำงาน"""
		print(text)
	def show_Art(self):
		text = '''
		("`-''-/").___..--''"`-._ 
		 `6_ 6  )   `-.  (     ).`-.__.`) 
		 (_Y_.)'  ._   )  `._ `. ``-..-' 
		   _..`--'_..-_/  /--'_.'
		  ((((.-''  ((((.'  (((.-' 
		'''
		print(text)

	def show_page(self):
		print('fb ฉัน : {}'.format(self.facebook))

if __name__ == '__main__':
	juiy = Juiy()
	juiy.show_name()
	juiy.show_IG()
	juiy.about()
	juiy.show_Art()
	juiy.show_page()