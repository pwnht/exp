#!/usr/bin/env python
from pwn import *
io=None
__author__ = '3summer'
s       = lambda data            :io.send(str(data)) 
sa      = lambda delim,data      :io.sendafter(str(delim), str(data))
sl      = lambda data            :io.sendline(str(data))
sla     = lambda delim,data      :io.sendlineafter(str(delim), str(data))
r       = lambda numb=4096       :io.recv(numb)
ru      = lambda delims,drop=True:io.recvuntil(delims, drop)
irt     = lambda                  :io.interactive()
uu32    = lambda data            :u32(data.ljust(4, '\0'))
uu64    = lambda data            :u64(data.ljust(8, '\0'))

#context.terminal = ['tmux', 'sp', '-h', '-l', '110']
context.terminal = ['gnome-terminal', '-x', 'sh', '-c']
context.log_level = 'debug'
token = ''
binary='./amazon'
libc=ELF('./libc-2.27.so')
ispow=0
isremote=0
isdebug=1
ip='121.41.38.38'
port=9999
def dbg(breakpoint):
    gdbscript = ''
    elf_base = 0
    gdbscript += 'b *{:#x}\n'.format(int(breakpoint) + elf_base) if isinstance(breakpoint, int) else breakpoint
    gdbscript += 'c\n'
    log.info(gdbscript)
    gdb.attach(io, gdbscript)
    time.sleep(1)
def b(string='####'):
    raw_input(string)
def add(index,conut,size,con):
    sla('Your choice:',1)
    sla('What item do you want to buy:',str(index))
    sla('How many:',str(conut))
    sla('How long is your note',str(size))
    sa('Content:',con)
def rm(index):
    sla("choice",str(3))
    sla('Which item are you going to pay for:',str(index))
def wr(address):
    sla('>>',str(3))
    sa('What do you want?',address)
def add666(size):
    sl(1)
    sl(size)
def exploit(io):

def main(argv=None):
	global io
	if isremote:
		io=remote(ip,port)
	else:
		io=process(binary)
		if isdebug:
			gdb.attach(io)
	return io
if __name__ == '__main__':
	if ispow:
		while True:
			try:
				io= main()
				exploit(io)
			except:
				io.close()
				continue	
			break
	else:
		io=main()
		exploit(io)
 	irt()
