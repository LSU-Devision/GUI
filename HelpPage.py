import tkinter as tk
from tkinter import ttk

import Utilities as utils


class HelpPage(tk.Toplevel):

    def __init__(self,master,container):
        super().__init__(master=master)
        self.master = master
        self.container = container
        main_window_width = self.container.winfo_width()
        # set the size of the pop up window
        main_window_height = self.container.winfo_height()
        # variables for the pop up window
        pop_up_window_width = 800
        # variables for the pop up window
        pop_up_window_height = 600
        # set the position of the pop up window
        #x = main_window_width + 75
        # set the position of the pop up window
        #y = main_window_height // 2 - pop_up_window_height // 2  # center the pop-up window vertically
        x=0
        y=0

        # set the title of the pop up window
        self.title('Help page')

        # set the geometry of the pop up window
        self.geometry(f'{pop_up_window_width}x{pop_up_window_height}+{x}+{y}')

        self.notebook = ttk.Notebook(self)
        # add the notebook using the grid method
        self.notebook.grid(row=0, column=0)
        # create the first tab
        self.tab1 = ttk.Frame(self.notebook)
        # create the second tab
        self.tab2 = ttk.Frame(self.notebook)
        # create the third tab
        self.tab3 = ttk.Frame(self.notebook)

        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)

        # adding tabs
        self.notebook.add(self.tab1, text="Simple Run In Steps", )

        self.notebook.add(self.tab2, text="General Navigation")

        self.notebook.add(self.tab3, text='General Notes')

        self.notebook.add(self.tab4, text = 'Special Runs')
        self.notebook.add(self.tab5, text='Credits')

        runInStepsText = open(utils.resource_path("docs/Simple_Run_In_Steps.txt"))
        generalNavigationText = open(utils.resource_path("docs/General_Navigation.txt"))
        generalNotesText = open(utils.resource_path("docs/General_Notes.txt"))
        specialRunsText = open(utils.resource_path("docs/Special_Runs.txt"))
        creditsText = open(utils.resource_path("docs/Credits.txt"))



        self.label_widget = tk.Label(self.tab1, text=runInStepsText.read(), wraplength=800, justify=tk.LEFT)
        #self.label_widget.grid(row=0, column=0, stricky="nsew")
        self.label_widget.pack()

        #self.label_widget.insert(tk.END, runInStepsText.read())
        #self.label_widget = tk.Text(self.tab2)
        self.label_widget = tk.Label(self.tab2, text=generalNavigationText.read(), wraplength=800, justify=tk.LEFT)
        self.label_widget.pack()
        #self.label_widget.insert(tk.END, "This is the text for the Columns tab.")

        self.label_widget = tk.Label(self.tab3, text=generalNotesText.read(), wraplength=800, justify=tk.LEFT)
        self.label_widget.pack()
        self.label_widget = tk.Label(self.tab4, text=specialRunsText.read(), wraplength=800, justify=tk.LEFT)
        self.label_widget.pack()
        self.label_widget = tk.Label(self.tab5, text=creditsText.read(), wraplength=800, justify=tk.LEFT)
        self.label_widget.pack()

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        #self.resize_tab(3)
        self.after(100, self.resize_tab, 5)
        self.run()

    def create_tab1(self):
        """
        :method: create tab 1
        :description: creates the page
        """
        #self.demo_button = ttk.Button(self.tab1, text="Demo", command=self.demo)
        pass

    def create_tab2(self):
        """
        :method: create tab 2
        :description: creates the page
        """
        pass

    def create_tab3(self):
        """
        :method: create tab 3
        :description: creates the page
        """
        pass

    def load_tab1(self):
        """
        :method: load tab 1
        :description: loads the page
        """
        #self.demo_button.grid(row=0, column=0)
        pass

    def load_tab2(self):
        """
        :method: load tab 2
        :description: loads the page
        """
        pass

    def load_tab3(self):
        """
        :method: load tab 3
        :description: loads the page
        """
        pass

    def run(self):
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()
        self.load_tab1()
        self.load_tab2()
        self.load_tab3()

    def on_tab_change(self, event):
        """
        method: on tab change
        description: method to resize the tab
        """
        # get the index of the tab
        tab_index = self.notebook.index(self.notebook.select())
        # resize the tab
        #self.resize_tab(tab_index)
        self.resize_tab(5)

    def resize_tab(self,index):
        """
        method: resize tab
        description: method to resize the tab
        :param index: index of the current tab
        """
        # if the index is 0, resize the tab to 300x200
        if index == 0:
            # resize the tab
            self.geometry('300x200')
        # if the index is 1, resize the tab to 400x400
        elif index == 1:
            # resize the tab
            self.geometry('400x350')
        # if the index is 2, resize the tab to 500x400
        elif index == 2:
            # resize the tab
            self.geometry('500x200')
        elif index == 3:
            self.geometry('1280x720')
        elif index == 4:
            self.geometry('1920x1080')
        elif index == 5:
            self.geometry('900x400')

