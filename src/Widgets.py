import tkinter.ttk as ttk
import tkinter as tk

# This is an object reference to store immutable values, used for carrying variables between callbacks
class MutImmutable():
    def __init__(self, value=None):
        self._val = value

    def __add__(self, value):
        self._val += value
        return self._val
    
    def __radd__(self, value):
        self._val = value + self._val
        return self._val
    
    def __sub__(self, value):
        self._val -= value
        return self._val
    
    def __rsub__(self, value):
        self._value = value - self._value
        return self._val
    
    def __mult__(self, value):
        self._value *= value
        return self._val
    
    def __rmult__(self, value):
        self._value = value * self._value
        return self._val
        
    def __div__(self, value):
        self._value /= value
        return self._val
    
    def __rdiv__(self, value):
        self._value = value / self._value
        return self._val

    def __pow__(self, value):
        self._value **= value
        return self._val
    
    def __floordiv__(self, value):
        self._value //= value
        return self._val
    
    def __repr__(self):
        return repr(self._val)
    
    def __len__(self):
        return len(self._val)
    
    def __setitem__(self, key, val):
        self._val = val
    
    def __getitem__(self, key):
        return self._val
    
    def __str__(self):
        return str(self._val)
    
    def __hash__(self):
        return hash(self._val)
    
class TkIO(ttk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self._value = MutImmutable()
    
    #Abstract method
    def pop(self):
        current_input = self._value['']
        self._value[''] = None
        return current_input
    
    #Abstract method
    def push(self, inp):
        self._value[''] = inp
    
class Inputable(TkIO):
    def __init__(self, *args):
        super().__init__(*args)
        self.ready_flag = False
        
    @property
    def value(self):
        if self.ready_flag:
            return self.value['']
        else:
            return None
    
    @value.setter
    def value(self, inp):
        self._value[''] = inp
    
    def ready(self):
        self.ready_flag = True
        
    def unready(self):
        self.ready_flag = False
    
    
class Outputable(TkIO):
    def __init__(self, *args):
        super().__init__(*args)
        self.outputs = []
        
    def bind_out(self, io_object, transform=lambda x: x):
        assert isinstance(io_object, Outputable)
        self.outputs.append((io_object, transform))
    
    def bind_to(self, io_object, transform=lambda x: x):
        assert isinstance(io_object, Outputable)
        io_object.outputs.append((self, transform))
    
    @property
    def value(self):
        return self._value['']
    
    @value.setter
    def value(self, inp):
        self._value[''] = inp
        self.update()
        
        for (io_obj, transform) in self.outputs:
            out = transform(inp)
            io_obj.value = out
        
    #method to update text, not all widgets will need
    def update(self):
        pass
    
class LabelBox(Inputable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        def text_start(e):
            self.unready()
            
        def text_finish(e):
            self.value = self.box.get()
            self.ready()
                
        text = kwargs.get('text', '')
        self.text = ttk.Label(self, text=text, relief='solid') 
        self.box = ttk.Entry(self, exportselection=0)
        
        self.text.pack(expand=True, fill=tk.BOTH)
        self.box.pack(expand=True, fill=tk.BOTH)
        
        self.box.bind('<FocusIn>', text_start)
        self.box.bind('<FocusOut>', text_finish)

    def pop(self):
        current_text = super().pop()
        self.box.delete(0, tk.END)
        if current_text == None:
            current_text = ''
        return current_text
    
    def push(self, text):
        self.box.delete(0, tk.END)
        self.box.insert(0, text)
        self.value = text

class IOButton(Outputable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        self.command = kwargs.get('command', None)
        if self.command:
            del kwargs['command']
        
        self.button = ttk.Button(self, command=self.run, **kwargs)
        self.button.pack(expand=True, fill=tk.BOTH)

    def run(self):
        if self.command:
            self.value = self.command()
        
class Counter(Outputable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        self.text_label = ttk.Label(self, **kwargs)
        self.counter = ttk.Label(self, text='-')
        self.text_label.pack(expand=True, side=tk.LEFT, fill=tk.BOTH)
        self.counter.pack(expand=False, side=tk.RIGHT, fill=tk.BOTH)
        
    def update(self):
        self.counter.config(text=self.value)
    
    def pop(self):
        old = self.value
        self.value = ''
        return old
        
    def push(self, inp):
        self.value = inp