from ast import Index
from turtle import pos
from fltk import *
import os
import subprocess as sp
import signal
import pathlib

vlc_player  ="C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"  # keep as is if using linux. otherwise, change to string: "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
global contents
contents = []
global pid
pid = 0
global index
index = -1
 


def main_playing(pos):
    global pid
    global contents
    if pid == 0:
        for x in range(len(contents)):
            play_a_song(contents[int(pos)])
            print(contents[int(pos)])
            if int(pos)+1 == len(contents):
                pos = 0
            else:
                pos += 1
            
            #pid.send_signal(signal.SIGTERM)

def play_a_song(mp3_file):
    global pid
    print("here is the location: "+str(mp3_file))
    pid = sp.Popen([vlc_player,'--intf', 'dummy', 'file:///' + str(mp3_file)])
    
    print('poll value: ' +str(sp.Popen.poll(pid)))
    
    # while True:
    #     print('poll value: ' +str(sp.Popen.poll()))
    #     if sp.Popen.poll() != None:
    #         break
        #current = MP

def remove_cb(wid):
    global location
    os.remove(location)
    fl_message('file has been removed')

def brow_cb(wid):
    global index
    index=brow.value() # position of the line selected
    print("pos:"+str(index))
    name=brow.text(index) # starts at 1
    out.value(name)
    
    location = contents[int(Index)-1]
    print(location)

def play_cb(wid):
   
	#    global location #path
    print(pid)
    if pid ==0:
        main_playing(pos-1)
        ''' # if is playing already
		for x in range(len(contents)):
			print("here is the location: "+str(location))
			pid = sp.Popen([vlc_player,'--intf', 'dummy', 'file:///'+ contents[int(pos)-1]])
			if int(pos)-1 == len(contents):
				pos = 1
			else:
				pos += 1
			current = MP3(str(contents[int(pos)-1]))
			sleep((current.info.length))
			pid.send_signal(signal.SIGTERM)
			pid = 0
			'''
        #pid = sp.Popen(['C:/Program Files (x86)/VideoLAN/VLC/vlc.exe','--intf', 'dummy', 'file:///C:/tools/my_code/musics/TeflonSega_RAIN.mp3'])
        #"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" --intf  dummy C:\tools\my_code\musics\TeflonSega_RAIN.mp3
        #print("pid:"+str(pid))

def skip_cb(wid,which):
    global pid
 
    pid.send_signal(signal.SIGTERM)
    pid = 0
    if which == 'next':
        if index == len(contents) - 1:
           play_a_song(contents[0])
        else:
           play_a_song(contents[index-1])
    else:
        if pos == 0:
           play_a_song(contents[index-1])
        else:
           play_a_song(contents[index-2])

def open_mp3_folder(wid):
    # get a list of mp3 files
    mp3_files= []
    for each in mp3_files:
        play_a_song(each)
        


def signal_cb(wid,sig):
    global pid
    if pid != 0:
        pid.send_signal(sig)
        pid = 0

def navigate_folder(wid):
    global contents
    folder = fl_dir_chooser('List out MP3 files', 'C:', 0)
    print("nav: folder: "+str(folder))
    for x in os.listdir(folder):
        print(x)
        if (str(x)[-4:]) == '.mp3':
            contents.append(os.path.join(folder,x))
            brow.add(x)
    print(contents)
    
    

def find_dir_cb(wid):
# https://www.fltk.org/doc-1.3/classFl__File__Chooser.html#details
    global location
    fname= fl_file_chooser('Open File','*.mp3',None)
    location = pathlib.Path(fname)
    print("find_dir_cb: "+str(location))
    print("find_dir_cb value:"+str(fname ))
	
   
    '''
    dir = str(dir)
    temp = str('\ ')
    for x in range(len(dir)-1,-1,-1):
        if dir[x] in "\\":
            dir = dir[:x]
            '''
'''
def inp_cb(wid):
    name=wid.value() # gets the text from the input widget
    brow.add(name)
    wid.value('') # clear input text
    wid.take_focus()
'''



# def main():
win=Fl_Window(100,100,400,500,'FL_Browser Example')
win.begin()
brow=Fl_Hold_Browser(0,55,win.w(),225)
menu = Fl_Menu_Bar(0,0,win.w(),25)
#fl_chooser = Fl_File_Chooser("C:", "MP3", Fl_File_Chooser.SINGLE, "My File Selector")
menu.add("Open Folder a |",0,navigate_folder)



out=Fl_Output(0,25,win.w(),30) # not working
prev_song = Fl_Button(0,280,65,65) # not working
prev_song.label('@|<') # not working

play = Fl_Button(65,280,65,65)
play.label('@>')

next_song = Fl_Button(130,280,65,65) # not working
next_song.label('@>|') # not working


stop = Fl_Button(195,280,65,65)
stop.label('@square')
remove = Fl_Button(260,280,65,65) # works
remove.label("@menu")
win.end()

play.callback(play_cb)
stop.callback(signal_cb,signal.SIGTERM)
brow.callback(brow_cb)
remove.callback(remove_cb)
next_song.callback(skip_cb,'next')
prev_song.callback(skip_cb,'prev')

win.show()
Fl.run()

# main()