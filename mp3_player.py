from fltk import *
import os
import subprocess as sp
import signal
import pathlib

vlc_player  ="vlc" # keep as is if using linux. otherwise, change to string: "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
global contents
contents = [] # list of songs in directory selected with full path
global pid
pid = 0
global index
index = 0
global current_song
current_song = 0

def main_playing(pos,action):
	# deciding what to do
    global pid
    global contents
    global current_song
    pos -= 1
    if pos+1 == 0: # pos+1 because index is subtracted by 1 when passed into func
        fl_message('please select a song first')
        return None
    if action == 'skip':
        if current_song+1 == len(contents):
            play_a_song(contents[0])
            current_song = 0
            out.value(brow.text(1)) # brow index is 1 based
        else:
            current_song += 1
            play_a_song(contents[current_song])
            out.value(brow.text(current_song+1)) # current_song+1 because browser index is 1 based
        
    elif action == 'back':
        if current_song == 0:
            play_a_song(contents[-1])
            current_song = len(contents)-1
            out.value(brow.text(len(contents)))
        else:
            current_song -= 1
            play_a_song(contents[current_song])
            out.value(brow.text(current_song+1))
            
    elif action == 'play':
        play_a_song(contents[int(pos)])
        current_song = pos
        out.value(brow.text(current_song+1)) 


def play_a_song(mp3_file):
	# playing of the son
    global pid
    if pid != 0:
       pid.send_signal(signal.SIGTERM)
    pid = sp.Popen([vlc_player,'--intf', 'dummy', 'file:///' + str(mp3_file)])
    
    
def remove_cb(wid):
	# removes selected song
    global current_song
    os.remove(contents[index-1])
    brow.remove(index)
    contents.pop(index-1)
    if pid !=0:
        pid.send_signal(signal.SIGTERM)
        out.value('')
    fl_message('file has been removed')

def brow_cb(wid):
	# selection menu gui
	# function does not execute if no mp3 files are displayed
    if contents == []:
        return None
    global index
    index=brow.value() # position of the line selected
    name=brow.text(index) # brow index starts at 1
    location = contents[int(index)-1]   
           
def play_cb(wid):
    # playing of selected song
    if contents == []:
	    fl_message('please select a directory of songs first')
	    return None 
    main_playing(index,'play')


def clear_all(wid):
	# cleans up all items inside browser
    brow.clear()
    if pid != 0:	
	    pid.send_signal(signal.SIGTERM)
    out.value('')
	
	
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

def skip_cb(wid,act):# act for main_playing to understand to go back or forward 1 song
    global pid
    if contents == []:
        fl_message('please select a directory of songs first')
    main_playing(index,act)


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
    # creates gui for user to select directory with mp3 files
    folder = fl_dir_chooser('Choose directory with MP3 files', 'C:', 0)
    for x in os.listdir(folder):
        print(x)
        # sanitization to prevent non mp3 files to be displayed
        if (str(x)[-4:]) == '.mp3':
			# adds song with full path to it
            contents.append(os.path.join(folder,x))
            # adds song name to browser
            brow.add(x)
    print(contents)
    


win=Fl_Window(100,100,400,500,'FL_Browser Example')
win.begin()
# widget creation
brow=Fl_Hold_Browser(0,55,win.w(),225)
menu = Fl_Menu_Bar(0,0,win.w(),25)
# adding buttons to menubar
menu.add("Open Folder   |",0,navigate_folder)
menu.add("&Skip to...    |/Playing",FL_F+1,go_to,'playing')
menu.add("&Skip to...    |/First",FL_F+2,go_to,'first')
menu.add("&Skip to...    |/Last",FL_F+3,go_to,'last')
menu.add("Clear All",FL_F+4,clear_all)
# output bar created to displaying playing song
out=Fl_Output(0,25,win.w(),30) # working
out.color(FL_YELLOW)
# buttons created with labels to help user comprehension
prev_song = Fl_Button(0,280,65,65)
prev_song.label('@|<')
prev_song.tooltip('Stop the current song and play the song before it')
play = Fl_Button(65,280,65,65)
play.label('@>')
play.tooltip('Plays Selected song')
next_song = Fl_Button(130,280,65,65)
next_song.label('@>|')
next_song.tooltip('Skip the current song and play the next')
stop = Fl_Button(195,280,65,65)	
stop.label('@square')
stop.tooltip('Stop playing the song that is playing')
remove = Fl_Button(260,280,65,65)
remove.label("@menu")
remove.tooltip('Delete the song selected from your computer')
# makes window resizeable
win.resizable(win)
Fl.scheme('gtk+')
win.end()
# callbacks
win.callback(signal_cb,signal.SIGTERM)
play.callback(play_cb)
stop.callback(signal_cb,signal.SIGTERM)
brow.callback(brow_cb)
remove.callback(remove_cb)
next_song.callback(skip_cb,'skip')
prev_song.callback(skip_cb,'back')

win.show()
Fl.run()
