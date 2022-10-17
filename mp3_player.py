from fltk import *
import os
import subprocess as sp
import signal
import pathlib

vlc_player  ="vlc" # keep as is if using linux. otherwise, change to string: "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
global contents
contents = []
global pid
pid = 0
global index
index = -1
global current_song
current_song = 0

def main_playing(pos,action):
    global pid
    global contents
    global current_song
    if action == 'skip':
        if current_song+1 == len(contents):
            play_a_song(contents[0])
            current_song = 0
            out.value(brow.text(1))
        else:
            play_a_song(contents[current_song+1])
            current_song += 1
            out.value(brow.text(current_song+1))
    elif action == 'back':
        if current_song == 0:
            play_a_song(contents[-1])
            current_song = len(contents)-1
            out.value(brow.text(len(contents)))
        else:
            play_a_song(contents[current_song-1])
            current_song -= 1
            out.value(brow.text(current_song+1))
    elif action == 'play':
        play_a_song(contents[int(pos)])
        current_song = pos
        out.value(brow.text(current_song+1))
        
def play_a_song(mp3_file):
    global pid
    print("here is the location: "+str(mp3_file))
    if pid != 0:
        pid.send_signal(signal.SIGTERM)
    pid = sp.Popen([vlc_player,'--intf', 'dummy', 'file:///' + str(mp3_file)])
    
    print('poll value: ' +str(sp.Popen.poll(pid)))
    
def remove_cb(wid):
    global location
    os.remove(location)
    fl_message('file has been removed')

def brow_cb(wid):
    global index
    index=brow.value() # position of the line selected
    print("pos:"+str(index))
    name=brow.text(index) # starts at 1
    
    location = contents[int(index)-1]
    print(location)            
def play_cb(wid):
   
    #    global location #path
    print(pid)
    if pid ==0:
        main_playing(index-1,'play')
 
        #pid = sp.Popen(['C:/Program Files (x86)/VideoLAN/VLC/vlc.exe','--intf', 'dummy', 'file:///C:/tools/my_code/musics/TeflonSega_RAIN.mp3'])
        #"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" --intf  dummy C:\tools\my_code\musics\TeflonSega_RAIN.mp3
        #print("pid:"+str(pid))

def go_to(wid,action):
	if action == 'playing':
		if pid == 0:
			fl_message('nothing is playing')
		else:
			brow.select(current_song+1)
	elif action == 'last':
		brow.select(len(contents))
	elif action == 'first':
		brow.select(1)

def skip_cb(wid,act):
    global pid
    main_playing(index-1,act)


def signal_cb(wid,sig):
    global pid
    if pid != 0:
        pid.send_signal(sig)
        pid = 0
    if wid == win:
        win.hide()

def navigate_folder(wid):
    global contents
    contents = []
    brow.clear()
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
menu.add("Skip to.../Playing",0,go_to,'playing')
menu.add("Skip to.../First",0,go_to,'first')
menu.add("Skip to.../Last",0,go_to,'last')

out=Fl_Output(0,25,win.w(),30) # working
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

win.callback(signal_cb,signal.SIGTERM)
play.callback(play_cb)
stop.callback(signal_cb,signal.SIGTERM)
brow.callback(brow_cb)
remove.callback(remove_cb)
next_song.callback(skip_cb,'skip')
prev_song.callback(skip_cb,'back')

win.show()
Fl.run()

# main()
