import os
#work around for pygame error
os.add_dll_directory('C:/Users/USER/PycharmProjects/musicPlayer/venv/Lib/site-packages/pygame')
from pygame import mixer
import pygame
from tkinter import*
import tkinter.font as font
import mysql.connector
from mysql.connector import Error
from tkinter import filedialog
from tkinter import ttk

#first connect to mysql server
try:
    conn = mysql.connector.connect(host='localhost', password='@Mosemuthoni57', user='Mosenje', db='musicplayer')
    if conn.is_connected():
        print("connection established....\n")
except Error as e:
    print("could not make a connection")

def add_songs():
    temp_song = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song",
                                          filetypes=(("mp3 Files", "*.mp3"),))
    for s in temp_song:
        s = s.replace("C:/Users/USER/Music/Music/Mp3 songs/", "")
        song_list.insert(END, s)

def delete_song():
    curr_song = song_list.curselection()
    song_list.delete(curr_song[0])

def volume(x):
    pygame.mixer.music.set_volume(slider.get())



def Play():
    song=song_list.get(ACTIVE)
    song = f"C:/Users/USER/Music/Music\Mp3 songs/{song}"
    mixer.music.load(song)
    mixer.music.play()

def Pause():
    mixer.music.pause()

def Stop():
    mixer.music.stop()
    song_list.selection_clear(ACTIVE)

def Resume():
    mixer.music.unpause()

def Previous():
    previous_one =song_list.curselection()
    previous_one = previous_one[0]-1
    temp2 = song_list.get(previous_one)
    temp2 = f"C:/Users/USER/Music/Music\Mp3 songs/{temp2}"
    mixer.music.load(temp2)
    mixer.music.play()
    song_list.selection_clear(0, END)
    song_list.activate(previous_one)
    song_list.selection_set(previous_one)

def Next():
    next_one = song_list.curselection()
    next_one = next_one[0]+1
    temp =song_list.get(next_one)
    temp = f"C:/Users/USER/Music/Music\Mp3 songs/{temp}"
    mixer.music.load(temp)
    mixer.music.play()
    song_list.selection_clear(0, END)
    song_list.activate(next_one)
    song_list.selection_set(next_one)

#creating a function that adds selected music to a database
def playlist():
    cursor = conn.cursor()
    add1 = song_list.curselection()
    add = song_list.get(add1)
    adds = f"C:/Users/USER/Music/Music/Mp3 songs/{add}"
    insert_stmnt =(
        " insert into music (name, num) value(%s,%s);"
    )
    data = (adds,1)
    try:
        cursor.execute(insert_stmnt, data)
        print("success...")
    except Error as err:
        print(f"Error: '{err}'")
#create a function that adds the playlist to the listbox
def newlistbox():
    song_list.delete(0,END)
    cursor = conn.cursor()
    result = None
    query = "select name from music"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for m in result:
            m = str(m)
            m = m.replace("('C:/Users/USER/Music/Music/Mp3 songs/", "")
            m = m.replace("',)", "")
            song_list.insert(END, m)


    except Error as err:
        print(f"Error: '{err}'")





root =Tk()
root.title('Resly Music player')

#initialize mixer
mixer.init()
#List box for songs
song_list = Listbox(root, selectmode=SINGLE,relief=FLAT, activestyle=DOTBOX , cursor='hand2',bg='purple', highlightcolor= 'orange', fg='white', font= ('Georgia', 15), height=17, width=47, selectbackground='gray', selectforeground='black')
song_list.grid(columnspan=20)

defined_font = font.Font(family='Helvetica')
#play button
photo = PhotoImage(file = "C:/Users/USER/PycharmProjects/musicPlayer/play2.png")
play_buttton = Button(root, image=photo, width =20,command=Play)
play_buttton.grid(row=1, column=0)

#pause Button
pause_button = Button(root, text='║║', width=7, command=Pause)
pause_button['font'] = defined_font
pause_button.grid(row=1, column=1)

#Volume
v = DoubleVar()
slider = ttk.Scale(root,variable=v,value=0, from_=0, to=1, orient=HORIZONTAL, length=60, command=volume)
slider.grid(row=1, column=6)

label = Label(root)
sel = "Value = " + str(v.get())
label.config(text = sel)
label.grid(row=1, column=7)

#stop button
stop_button = Button(root, text='■', width=7, command=Stop)
stop_button['font'] = defined_font
stop_button.grid(row=1, column=2)

#resume button
resume_button = Button(root, text='►', width=7, command=Resume)
resume_button['font'] = defined_font
resume_button.grid(row=1, column=3)

#Previous button
previous_button = Button(root, text='⏮', width=7, fg='green', command=Previous)
previous_button['font'] = defined_font
previous_button.grid(row=1, column=4)

#Next button
next_button = Button(root, text='⏭', width=7, fg='red', command=Next)
next_button['font'] = defined_font
next_button.grid(row=1, column=5)

#Menu
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="♫ Menu",menu=add_song_menu)
add_song_menu.add_command(label="Add songs", command = add_songs)
add_song_menu.add_command(label="show playlist", command= newlistbox)
add_song_menu.add_command(label='Delete song', command = delete_song)
add_song_menu.add_command(label="add playlist", command= playlist)

mainloop()
