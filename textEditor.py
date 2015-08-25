#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import Tkinter
import sys
import tkFileDialog
import tkMessageBox
import os
import imp
import subprocess
import fileinput


#define class
class editor_tk(Tkinter.Tk):
    def __init__(self,parent,textToOpen = None):
        Tkinter.Tk.__init__(self,parent)
        #keep track of parent class
        self.parent = parent
        #call initialize function, which is seperate from main logic
        self.initialize()
        
        if len(sys.argv) == 2:
            self.openText(sys.argv[1])
        elif textToOpen:
            self.openText(textToOpen)
            
            
        
    #initialization function
    def initialize(self):
        #create grid layout manager
        self.grid()

        #create global counter for number of times file_save has been completed, local passing to function failed
        global countOfSaves
        countOfSaves = 0

        #create a toplevel menu
        self.menubar = Tkinter.Menu(self)
        self.filemenu = Tkinter.Menu(self.menubar,tearoff=0)

        #create file menu
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save As...", command=self.file_save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Plugin Manager", command = self.plugin_manager)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.close)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # display the menu
        self.config(menu=self.menubar)
        
        
        #construct the toolbars
        global counterForPlugins
        self.import_toolbars()

        #seperate main toolbar for imported buttons
        self.defaultToolbar = Tkinter.Frame(self,bd=1, relief = "raised")
        self.defaultToolbar.grid(column = 1, row = 0,sticky = "nsew")

        self.import_buttons()

        #create text box
        self.text = Tkinter.Text(self)
        self.text.grid(column=1,row=counterForPlugins, sticky ="nesw")

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(counterForPlugins,weight=1)

        #create shortcuts
        self.shortcuts()


    def openText(self,text):       
        #newContent=sys.argv[1].read()
        #self.text.delete(0.0,Tkinter.END)
        file = open(text)
        openContent = file.read()
        self.text.insert(Tkinter.END, openContent)

    def import_buttons(self):
        counterForButtonPlugins = 0
        #../aadijoshi/Desktop/textEditor/plugins
        testFilePath = os.path.abspath("plugins")
        
        #get list of files in directory
        listOfFilesInPluginDirectory = os.listdir(testFilePath)

        #get list of python files in directory and remove extension
        listOfButtonPlugins = []
        for everyFile in listOfFilesInPluginDirectory:
            if everyFile[-3::1] == ".py" and everyFile[0:6] == "button":
                listOfButtonPlugins.append(everyFile[0:-3])

        #remove plugins to skip
        if "toSkip.txt" in listOfFilesInPluginDirectory:
            fp = open("plugins/toSkip.txt")
            for plugin in fp:
                if plugin[0:-1] in listOfButtonPlugins:
                    plugin = plugin[0:-1]
                    listOfButtonPlugins.remove(plugin)
                    
        #import plugin
        for plugins in listOfButtonPlugins:
            returnedPlugin = imp.find_module(plugins, [testFilePath])
            moduleObject = imp.load_module(plugins,returnedPlugin[0],returnedPlugin[1],returnedPlugin[2])
            moduleObject.create_button(self)
            self.defaultButton.grid(column = counterForButtonPlugins, row = 0)
            counterForButtonPlugins+=1

    def import_toolbars(self):
        global counterForPlugins
        
        testFilePath = os.path.abspath("plugins")
       
        #get list of files in directory
        listOfFilesInPluginDirectory = os.listdir(testFilePath)

        #get list of python files in directory and remove extension
        listOfToolbarPlugins = []
        for everyFile in listOfFilesInPluginDirectory:
            if everyFile[-3::1] == ".py" and everyFile[0:7] == "toolbar":
                listOfToolbarPlugins.append(everyFile[0:-3])

        counterForPlugins = 1

        #remove plugins to skip
        if "toSkip.txt" in listOfFilesInPluginDirectory:
            fp = open("plugins/toSkip.txt")
            for plugin in fp:
                if plugin[0:-1] in listOfToolbarPlugins:
                    plugin = plugin[0:-1]
                    listOfToolbarPlugins.remove(plugin)
        
        #import plugin
        for plugins in listOfToolbarPlugins:
            returnedPlugin = imp.find_module(plugins, [testFilePath])
            moduleObject = imp.load_module(plugins,returnedPlugin[0],returnedPlugin[1],returnedPlugin[2])
            moduleObject.create_toolbar(self)
            self.defaultToolbar.grid(column = 1, row = counterForPlugins,sticky ="nsew")
            counterForPlugins+=1

    def file_open(self):  
        #continueWithOpen = tkMessageBox.askyesno(message="Any unsaved progress will be lost. Would you like to continue?")
        continueWithOpen = True
        if continueWithOpen:
            fileToOpen = tkFileDialog.askopenfilename()
            if fileToOpen is None: #Check if user cancelled
                return
            else:
                #os.system("start"+"first.py")
                #subprocess.call(tkFileDialog.askopenfilename(),shell=True) #ask for file and then open it
                #subprocess.Popen(os.path.dirname(os.path.realpath(fileToOpen)))

                #p = subprocess.Popen(["echo", "hello world"], stdout=subprocess.PIPE)
                #print(p.communicate())

                #subprocess.Popen(["../Texteditor2.app"], shell=True)
                #subprocess.call("open ../Texteditor2.app", shell = True)
                
                #p = subprocess.Popen(["ls ../"], stdout=subprocess.PIPE)
                #print(p.communicate())

                #seems the count starts at 1, i.e. one character means count of 2
                if len(self.text.get(0.0,Tkinter.END)) == 1:
                    self.openText(fileToOpen)
                else:
                    newEditor = editor_tk(None,fileToOpen)
                    newEditor.title("Versatile: The Flexible Text Editor")
                    newEditor.mainloop()

                #os.system(tkFileDialog.askopenfilename())
                #window = Tkinter.Tk.TopLevel(self)
                #print(fileToOpen)
                #os.system("open "+fileToOpen)
                #newEditor = editor_tk(None)
                #newEditor.title = fileToOpen
                #newEditor.mainloop()
                
                #subprocess.Popen(fileToOpen, shell= True)
                #print("hello")
                #toplevel = Tkinter.Toplevel()
                #toplevel.focus_set()
                
                #newContent=fileToOpen.read()
                #self.text.delete(0.0,Tkinter.END)
                #self.text.insert(Tkinter.END, newContent)
        else:
            return

    def close(self):
        continueWithClose = tkMessageBox.askyesno(message="Any unsaved progress will be lost. Would you like to continue?")
        if continueWithClose:
            self.destroy()

    def file_save(self):
        global countOfSaves
        saveSettings = tkFileDialog.asksaveasfile(mode="w")
        if saveSettings is None: #Check if user cancelled
            return
        fileToSave = str(self.text.get(0.0, Tkinter.END))
        saveSettings.write(fileToSave)
        print(saveSettings)
        saveSettings.close()
        countOfSaves+=1
        print(countOfSaves)

    def shortcuts(self):
        self.text.bind("<Control-q>",lambda x: self.close())
        self.text.bind("<Command-q>",lambda x: self.close())
        self.text.bind("<Control-s>",lambda x: self.file_save())
        return

    def plugin_manager(self):
        #create new window for plugin manager
        self.pluginManager = Tkinter.Toplevel(padx = 20, pady = 20)
        self.pluginManager.title("Plugin Manager")
        self.pluginManager.grid()

        testFilePath = os.path.abspath("plugins")
        #get list of files in directory
        listOfFilesInPluginDirectory = os.listdir(testFilePath)

        #get list of python files in directory and remove extension
        self.listOfPlugins = []
        for everyFile in listOfFilesInPluginDirectory:
            if everyFile[-3::1] == ".py" and (everyFile[0:7] == "toolbar" or everyFile[0:6] == "button"):
                self.listOfPlugins.append(everyFile[0:-3])

        self.listOfCheckboxes = []

        #list all plugins as checkbuttons, link checkbutton state to listOfCheckboxes
        for pluginIndex in range(0, len(self.listOfPlugins)):
            self.listOfCheckboxes.append("placeholder")
            self.listOfCheckboxes[pluginIndex] = Tkinter.IntVar()
            pluginText = self.listOfPlugins[pluginIndex]
            self.pluginManager.textBox = Tkinter.Checkbutton(self.pluginManager, text = pluginText,variable = self.listOfCheckboxes[pluginIndex])                        
            self.pluginManager.textBox.select()
            
            if "toSkip.txt" in listOfFilesInPluginDirectory:
                fp = open("plugins/toSkip.txt")
                for plugin in fp:
                    if plugin[0:-1] in self.listOfPlugins:
                        plugin = plugin[0:-1]
                        if plugin == pluginText:
                            self.pluginManager.textBox.deselect()
                        
            self.pluginManager.textBox.grid(column = 0, row = pluginIndex, sticky = "nsew")

        self.pluginManager.saveButton = Tkinter.Button(self.pluginManager, command = self.saveStates, text = "Save")
        self.pluginManager.saveButton.grid(column = 0, row = len(self.listOfPlugins), sticky = "nsew")
            
    def saveStates(self):
        fp = open("plugins/toSkip.txt","w")
        for checkButtonIndex in range(0,len(self.listOfCheckboxes)):
            checkButtonValue = self.listOfCheckboxes[checkButtonIndex].get()
            if checkButtonValue == 0:
                fp.write(self.listOfPlugins[checkButtonIndex]+"\n")
        
            

if __name__ == "__main__":
    #create instance of editor_tk class. No parent defined.
    editor = editor_tk(None)
    editor.title("Versatile: The Flexible Text Editor")
    #loop indefinitely, waiting for events
    editor.mainloop()
