import os, shutil, json, webbrowser, threading, glob, time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

if not os.path.exists('settings.json'):
    data = {"beclean":[], "filehome":[]}
    with open("settings.json", "w", encoding="utf8") as f: json.dump(data, f, ensure_ascii=False)

def selectdir_beclean():
    file_path = filedialog.askdirectory()
    if file_path != "":
        with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)
        data['beclean'].append(file_path)
        with open("settings.json", "w", encoding="utf8") as f: json.dump(data, f, ensure_ascii=False)
        messagebox.showinfo('資訊', f'路徑已添加\n絕對路徑: {file_path}')
        main()
def selectdir_combobox(event, combox, selectxt):
    selectxt.set("目前已選定: "+combox.get())
def selectdir_del(selected):
    file_path = selected.get().replace("目前已選定: ", "")
    if file_path != "":
        with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)
        clean2 = []
        for i in data['beclean']:
            if i != file_path: clean2.append(i)
        data['beclean'] = clean2
        with open("settings.json", "w", encoding="utf8") as f: json.dump(data, f, ensure_ascii=False)
        messagebox.showinfo('資訊', f'路徑已刪除\n絕對路徑: {file_path}')
        main()
def main():
    global win, frame
    frame.destroy()
    with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)

    frame = tk.LabelFrame(win, text = "需被整理的資料夾")
    frame.grid(row = 0, column=1, padx = 10, pady = 10, sticky="n")

    button1 = ttk.Button(frame, text = "瀏覽並添加", command=selectdir_beclean)
    button1.grid(row = 1, column = 1, sticky="w", padx = 10)

    selected = tk.StringVar()
    label2 = tk.Label(frame, textvariable=selected, fg = "blue")
    selected.set("目前已選定: ")
    label2.grid(row = 2, column=0, sticky="w", padx = 10, pady=10)

    combobox = ttk.Combobox(frame, values = data['beclean'], state="readonly", width=50)
    combobox.grid(row = 1, column = 0, sticky="w", padx = 10, pady=10)
    combobox.bind('<<ComboboxSelected>>', lambda event: selectdir_combobox(event, combobox, selected))

    button2 = ttk.Button(frame, text = "刪除選取項", command=lambda: selectdir_del(selected))
    button2.grid(row = 2, column = 1, sticky="w", padx = 10)

def cleanto_path(folderpath):
    file_path = filedialog.askdirectory()
    if file_path != "": folderpath.set("的檔案歸類到資料夾路徑: "+file_path)
def cleanto_add(folderpath, exten):
    with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)
    fp2 = folderpath.get().replace("的檔案歸類到資料夾路徑: ", "")
    errmsg, con = "", False
    if fp2 != "" and exten.get() != "": con = True
    if fp2 == "": errmsg += "缺少資料夾路徑|"
    if exten.get() == "": errmsg += "缺少副檔名|"

    if con == True: 
        data['filehome'].append(fp2+"/*."+exten.get())
        with open("settings.json", "w", encoding="utf8") as f: json.dump(data, f, ensure_ascii=False)
        messagebox.showinfo('資訊', f'資料歸類區添加成功!\n路徑:{fp2+"/*."+exten.get()}')
        cleanto()
    else: messagebox.showerror("錯誤", f"無法添加檔案歸類區\n{errmsg}")
def cleanto_del(combobox):
    if combobox.get() != "":
        with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)
        clean2 = []
        for i in data['filehome']:
            if i != combobox.get(): clean2.append(i)
        data['filehome'] = clean2
        with open("settings.json", "w", encoding="utf8") as f: json.dump(data, f, ensure_ascii=False)
        messagebox.showinfo('資訊', f'路徑已刪除\n絕對路徑: {combobox.get()}')
        cleanto()
    else: messagebox.showerror("錯誤!", "無法刪除項目!\n未選取任何項目!")
def cleanto():
    global frame, win
    frame.destroy()
    with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)

    frame = tk.LabelFrame(win, text = "檔案歸類區")
    frame.grid(row = 0, column=1, padx = 10, pady = 10, sticky = "n")

    frame2 = tk.Frame(frame)
    frame2.grid(row = 0, column=0, padx = 10, pady = 10, sticky = "w")
    label1 = tk.Label(frame2, text="將副檔名為")
    label1.grid(row = 0, column = 0,sticky="w")
    label3 = tk.Label(frame2, text="(例如:jpg)")
    label3.grid(row = 1, column = 0,sticky="w")
    exten = tk.StringVar()
    entry1 = ttk.Entry(frame2, width=10, textvariable=exten)
    entry1.grid(row = 0, column = 1, sticky="w")
    folderpath = tk.StringVar()
    folderpath.set("的檔案歸類到資料夾路徑: ")
    label2 = tk.Label(frame2, textvariable=folderpath)
    label2.grid(row = 0, column = 2,sticky="w")
    button1 = ttk.Button(frame2, text = "瀏覽", command=lambda:cleanto_path(folderpath))
    button1.grid(row = 0, column = 3, sticky = "w")
    button2 = ttk.Button(frame2, text = "添加", command=lambda: cleanto_add(folderpath, exten))
    button2.grid(row = 1, column = 3, sticky = "w")

    frame3 = tk.Frame(frame)
    frame3.grid(row = 1, column=0, padx = 10, pady = 10, sticky = "w")
    combobox = ttk.Combobox(frame3, values = data['filehome'], state="readonly", width=50)
    combobox.grid(row = 0, column = 0, sticky="w")
    button4 = ttk.Button(frame3, text = "刪除選取項", command=lambda: cleanto_del(combobox))
    button4.grid(row = 0, column = 1, sticky="w", padx = 10)

def info():
    global frame, win
    frame.destroy()
    with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)

    frame = tk.LabelFrame(win, text = "資訊")
    frame.grid(row = 0, column=1, padx = 10, pady = 10, sticky = "n")
    label1 = tk.Label(frame, text = """版本: 0.1

作者: pour33142GX
Discord: pour33142gx""")
    label1.grid(row = 0, column = 0, padx = 10, pady = 10)
    link = tk.Label(frame, text = "Github: 點我", fg = "blue")
    link.grid(row = 1, column = 0)
    link.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/pictures2333", new=0))

def startclean():
    global frame, framebar, win
    frame.destroy()
    framebar.destroy()

    with open("settings.json", "r", encoding="utf8") as f: data = json.load(f)

    frame = tk.Frame(win, padx = 10, pady = 10)
    frame.grid(row = 0, column=0, sticky="w")
    label1 = tk.Label(frame, text="正在整理中...")
    label1.grid(row = 0, column = 0, sticky = "w")
    pb = ttk.Progressbar(frame,length=500, mode="determinate", orient='horizontal')
    pb["maximum"] = int(len(data['beclean']))
    pb["value"] = 0
    pb.grid(row = 1, column=0, sticky="w")
    
    frame3 = tk.Frame(frame)
    frame3.grid(row = 2, column=0, sticky="w")
    txt1 = tk.StringVar()
    txt1.set(f"已偵測到資料夾: {str(int(len(data['beclean'])))}")
    label2 = tk.Label(frame3, textvariable=txt1)
    label2.grid(row = 0, column = 0, sticky="w")
    txt2 = tk.StringVar()
    txt2.set(f"進度: 0/{str(int(len(data['beclean'])))}")
    label3 = tk.Label(frame3, textvariable=txt2)
    label3.grid(row = 1, column = 0, sticky="w")
    txt3 = tk.StringVar()
    txt3.set(f"目前整理資料夾: ")
    label4 = tk.Label(frame3, textvariable=txt3)
    label4.grid(row = 0, column = 1, sticky="w", padx = 20)
    txt4 = tk.StringVar()
    txt4.set(f"已偵測檔案: ")
    label5 = tk.Label(frame3, textvariable=txt4)
    label5.grid(row = 1, column = 1, sticky="w", padx = 20)
    txt5 = tk.StringVar()
    txt5.set(f"資料夾檔案整理進度: 0/0")
    label6 = tk.Label(frame3, textvariable=txt5)
    label6.grid(row = 2, column = 1, sticky="w", padx = 20)

    pb2 = ttk.Progressbar(frame,length=500, mode="determinate", orient='horizontal')
    pb2["maximum"] = 100
    pb2["value"] = 0
    pb2.grid(row = 3, column=0, sticky="w")

    label7 = tk.Label(frame, text = "警告:整理時關閉程式可能導致檔案毀損!")
    label7.grid(row = 4, column = 0, sticky="w")

    done = 0
    susfn, allfn = 0, 0
    pb['value'] = 0
    for foln, fol in enumerate(data['beclean']):
        txt3.set(f"目前整理資料夾: {str(fol)}")
        con = False
        try: 
            files = glob.glob(fol+"/*")
            con = True
        except: pass
        if con == True:
            allf = []
            for ext in data['filehome']:
                files2 = glob.glob(fol+"/*"+os.path.splitext(ext)[1])
                for f in files2: allf.append(f)
            txt4.set(f"已偵測檔案: {str(int(len(allf)))}")
            txt5.set(f"資料夾檔案整理進度: 0/{str(int(len(allf)))}")
            allfn += len(allf)
            pb2['maximum'] = int(len(allf))
            pb2['value'] = 0

            for fin, fi in enumerate(allf):
                try: 
                    for text in data['filehome']:
                        fe, be = os.path.split(text)
                        fe2, be2 = os.path.splitext(fi)
                        fe3, be3 = os.path.splitext(be)
                        fe4, be4 = os.path.split(fi)
                        if be3 == be2:
                            shutil.move(fi, fe+"/"+be4)
                            break
                    txt5.set(f"資料夾檔案整理進度: {str(fin+1)}/{str(int(len(allf)))}")
                    susfn += 1
                    pb2['value'] = fin+1
                except: pass
            done += 1
        pb['value'] = foln+1
    messagebox.showinfo("資訊", f"整理完成!\n成功整理資料夾: {str(done)}/{str(int(len(data['beclean'])))}\n成功整理檔案: {str(susfn)}/{str(allfn)}")
    main()
    framebars()

win = tk.Tk()
win.title("file classification")

frame = tk.LabelFrame(win, text = "", padx = 10, pady = 10)
frame.grid(row = 0, column=1)

def framebars():
    global framebar
    framebar = tk.LabelFrame(win, text = "選單")
    framebar.grid(row = 0, column=0, sticky="n", padx = 10, pady = 10)
    buttonb1 = ttk.Button(framebar, text="被整理資料夾", command=main)
    buttonb1.grid(row = 0, column = 0, padx = 5, pady=5)
    buttonb2 = ttk.Button(framebar, text="檔案歸類設定", command=cleanto)
    buttonb2.grid(row = 1, column = 0, padx = 5, pady=5)
    buttonb3 = ttk.Button(framebar, text="資訊", command=info)
    buttonb3.grid(row = 2, column=0, padx=5, pady=5)
    buttonb4 = ttk.Button(framebar, text="開始整理", command=lambda: threading.Thread(target=startclean).start())
    buttonb4.grid(row = 3, column=0, padx=5, pady=5)

framebars()

main()

win.mainloop()