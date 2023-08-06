'''
Author: Elidas               |   Python Version: 3.9.9
Date: 24/4/2023, 20:01:50    |   version: 0.0.1
'''

# __LIBRARIES__ #
from tkinter import *

# __MAIN CODE__ #
class Add_Delete(Button):
    '''
    Creates a button pair to add or delete a copy of the row
    in which they are placed.
    ONLY WITH GRID!!
    '''
    def __init__(self, master, scale=1, min_row=1, max_row=-1, textFont='Bell MT', textSize=10):
        Button.__init__(self, master)
        self.__min = min_row
        self.__max = max_row
        self.__row = self.master.grid_size()[1]
        self.__dic = self.master.__dict__['children'].values()
        self.add = Button(
            master, text='+',
            font=(textFont, int(textSize*scale)),
            command=self.__add_row
        )
        self.add.grid(row=master.grid_size()[1]-1, column=master.grid_size()[0], padx=10)
        self.delete = Button(
            master, text='-',
            font=(textFont, int((textSize)*scale)),
            state=DISABLED, width=self.add['width'],
            command=self.__del_row
        )
        self.delete.grid(row=master.grid_size()[1]-1, column=master.grid_size()[0]+1)
    
    def __add_row(self):
        '''
        Adds a new row with the same items in the row below
        '''
        to_copy = [i for i in self.__dic if not isinstance(i, Button) and i.grid_info()['row']==self.__row-1]
        for item in to_copy:
            new = type(item)(self.master)
            for key in list(item.keys())[:-1]:
                try:
                    new.config({key: item[key]})
                    try:
                        new.current(0)
                    except:
                        pass
                except Exception:
                    pass
            for info in list(item.grid_info()):
                try:
                    new.grid({info: item.grid_info()[info]})
                    new.grid(row=self.__row)
                except:
                    pass
        self.add.grid(row=self.__row)
        self.delete.grid(row=self.__row)
        self.__row = self.master.grid_size()[1]
        if self.__row >= self.__min:
            self.delete.config(state=NORMAL)
        if self.__row == self.__max and self.__max != -1:
            self.add.config(state=DISABLED)
        
    def __del_row(self):
        '''
        Deletes the current row of items.
        '''
        to_delete = [i for i in self.__dic if not isinstance(i, Button) and i.grid_info()['row']==self.__row-1]
        for item in to_delete:
            item.destroy()
        self.add.grid(row=self.__row-2)
        self.delete.grid(row=self.__row-2)
        self.__row = self.master.grid_size()[1]
        if self.__row <= self.__min:
            self.delete.config(state=DISABLED)
        if self.__row < self.__max:
            self.add.config(state=NORMAL)

class Checkbox(Checkbutton):
    '''
    A simplified CheckBox with a simply usage to set active or
    inactive some features.
    '''
    
    def __init__(self, master, **kwargs):
        Checkbutton.__init__(self, master)
        self.__control_var = BooleanVar()
        self.__dependencies = list()
        self.config(text = kwargs['text'])
        try:
            self.config(font = kwargs['font'])
        except:
            pass
        self.config(offvalue=False, onvalue=True)
        self.config(variable = self.__control_var)
        self.bind('<ButtonRelease-1>', self.__bind)
        
        self.binded = [self.apply_codependencyes]
        self.bind('<ButtonRelease-1>', self.__apply_codependencyes)

    def set_text(self, text):
        '''
        Configres only the text shown with the box
        '''
        self.config(text = text)

    def configure(self, **conf):
        '''
        Configures everything that's configurable in a CheckButton
        '''
        for key in list(conf.keys()):
            value = conf[key]
            self.config({key: value})

    def set_dependencies(self, *args):
        '''
        Sets the codependency of this CheckBox with other Checkboxes.
        '''
        for item in args:
            if not isinstance(item, Checkbox) and not isinstance(item, Entry):
                raise TypeError(f'Not supported codependency between Checkbox and {type(item)}')
        else:
            self.__dependencies = list(args)

    def __apply_codependencyes(self, event):
        '''
        Applyes the dependencies set.
        If CheckBox, deactivates.
        If Entry applies changes its state
        '''
        self.__apply_dependencies()
        for item in self.__dependencies:
            if isinstance(item, Checkbox):
                if item.is_active():
                    item.__apply_dependencies()
                item.deselect()
    
    def __apply_dependencies(self):
        '''
        Toggels the state of the entry depending state of the codependent checkbox
        '''
        for item in self.__dependencies:
            if isinstance(item, Entry):
                if item['state'] == NORMAL:
                    item['state'] = DISABLED
                elif item['state'] == DISABLED:
                    item['state'] = NORMAL
                
    def show_dependencies(self):
        '''
        Shows th dependencies between THIS CheckBox and the other CheckBoxes
        '''
        items = list()
        for item in self.__dependencies:
            obj = dict()
            if isinstance(item, Checkbox):
                obj = (item['text'], item.is_active(), item)
            if isinstance(item, Entry):
                obj = ('Entry', item['state'], item)
            items.append(obj)
        items.append((self['text'], self.is_active(), self))
        return items

    def delete_dependencies(self, *args):
        '''
        Deletes the given dependencies
        '''
        for item in args:
            self.__dependencies.remove(item)

    def is_active(self):
        '''
        Returns Either is active or not.
        '''
        return self.__control_var.get()
    
    def add_func_to_bind(self, func):
        '''
        Adds a function to queue to run when the checkbox is clicked.
        functions run every time the checkbox is checked
        '''
        self.binded.append(func)
        
    def __bind(self, event):
        '''
        runs every function in the queue when the checkbox is clicked
        '''
        for func in self.binded:
            func(event)

class ScrollWindow(Canvas):
    '''
    A simplified way to create a scrollable window
    '''
    def __init__(self, master):
        Canvas.__init__(self, master)
                
        #Creamos lo necesario
        self.frame = Frame(self)
        self.vbar = Scrollbar(self.master, orient=VERTICAL, command=self.yview)
        
        #Configuramos
        self.config(yscrollcommand=self.vbar.set)
        self.frame.bind('<Configure>', self.__updateScrollRegion)
        self.bind_all('<MouseWheel>', self.__on_mousewheel)
        self.vbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.create_window(0, 0, window=self.frame, anchor=NW)
        
    def __updateScrollRegion(self, event):
        self.update_idletasks()
        self.config(scrollregion=self.frame.bbox())
        
    def __on_mousewheel(self, event):
        self.yview_scroll(-1*int(event.delta/120), "units")
        
class TerminalWindow(Frame):
    '''
    A simplified way to create a scrollable window
    '''
    def __init__(self, master, max_width):
        Frame.__init__(self, master)
                
        self._master = master
        self.__width, self.__max_width = 40, max_width
        #Creamos lo necesario
        self.__terminal = Listbox(
            self, width=self.__width, 
            background='black', fg='light green', 
            font=('Consolas', 10)
        )
        self.__vbar = Scrollbar(self, orient=VERTICAL, command=self.__terminal.yview)
        self.__hbar = Scrollbar(self, orient=HORIZONTAL, command=self.__terminal.xview)
        
        #Configuramos
        self.__terminal.config(yscrollcommand=self.__vbar.set, xscrollcommand=self.__hbar.set)
        self.__vbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.__hbar.pack(fill=X, side=BOTTOM, expand=FALSE)
        self.__terminal.pack(fill=BOTH, expand=0, side=TOP)
        
        self.__set_width()
        
    def add(self, place, text):
        self.__terminal.insert(place, text)
    
    def __set_width(self):
        self.__terminal.update()
        if self.__terminal.winfo_reqwidth() >= self.__max_width:
            while self.__terminal.winfo_reqwidth() >= self.__max_width-20:
                self.__width -= 1
                self.__terminal.config(width=self.__width)
                #! print(self.__terminal.winfo_reqwidth(), self.__max_width)
        elif self.__terminal.winfo_reqwidth() < self.__max_width:
            while self.__terminal.winfo_reqwidth() <= self.__max_width-20:
                self.__width += 1
                self.__terminal.config(width=self.__width)
                #! print(self.__terminal.winfo_reqwidth(), self.__max_width)
#__AUXILIARY__#


# __NOTES__ #
'''
'''

# __BIBLIOGRAPHY__ #
'''
'''