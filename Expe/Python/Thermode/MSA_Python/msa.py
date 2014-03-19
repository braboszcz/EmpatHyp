# msa.py : A Python wrapper for the msatemp library

import ctypes as ct, sys, os,pdb

try:
	lib = ct.CDLL('msatemp.dll')
except:
	print 'msatemp.dll not found'
	sys.exit(-1)

# Creating shortcuts to msatemp.dll's functions

MsaSleep = lib['MsaSleep']
MsaSetTimeRef = lib['MsaSetTimeRef']
StartLog = lib['StartLog']
WriteLog = lib['WriteLog']
logString = lib['logString']

MsaGetLastError = lib['MsaGetLastError']
MsaSetIniPathName = lib['MsaSetIniPathName']
MsaOpen = lib['MsaOpen']
MsaOpenWithIniPName = lib['MsaOpenWithIniPName']
MsaClose = lib['MsaClose']
MsaSetPollInterval = lib['MsaSetPollInterval']
MsaGetCurrTemp = lib['MsaGetCurrTemp']
MsaSetTemp = lib['MsaSetTemp']
MsaGetCurrTemp = lib['MsaGetCurrTemp']
MsaSetCriticalTemp = lib['MsaSetCriticalTemp']
MsaSetCriticalMaxTime = lib['MsaSetCriticalMaxTime']
MsaSetBaseTemp = lib['MsaSetBaseTemp']
MsaSetSlopeToBase = lib['MsaSetSlopeToBase']
MsaSetStimTemp = lib['MsaSetStimTemp']
MsaSetSlopeToStim = lib['MsaSetSlopeToStim']
MsaGetCriticalTemp = lib['MsaGetCriticalTemp']
MsaGetCriticalMaxTime = lib['MsaGetCriticalMaxTime']
MsaGetBaseTemp = lib['MsaGetBaseTemp']
MsaGetSlopeToBase = lib['MsaGetSlopeToBase']
MsaGetStimTemp = lib['MsaGetStimTemp']
MsaGetSlopeToStim = lib['MsaGetSlopeToStim']
MsaReachBaseTemp = lib['MsaReachBaseTemp']
MsaReachStimTemp = lib['MsaReachStimTemp']
MsaStim = lib['MsaStim']
MsaSetLogPathName = lib['MsaSetLogPathName']
MsaTest = lib['MsaTest']
MsaNotifyMriSequenceStart = lib['MsaNotifyMriSequenceStart']
checkPortPresent = lib['checkPortPresent']
checkMsaPresent = lib['checkMsaPresent']

# Specifiying functions argument type

logString.argtypes = [ct.c_char_p]
MsaSleep.argtypes = [ct.c_uint]
WriteLog.argtypes = [ct.c_int,ct.c_long]
MsaSetPollInterval.argtypes = [ct.c_double]
MsaSetLogPathName.argtypes = [ct.c_char_p]
MsaSetIniPathName.argtypes = [ct.c_char_p]
MsaOpen.argtypes = [ct.c_int]
MsaOpenWithIniPName.argtypes = [ct.c_int,ct.c_char_p]
MsaSetTemp.argtypes = [ct.c_double,ct.c_double]
MsaSetCriticalTemp.argtypes = [ct.c_double]
MsaSetCriticalMaxTime.argtypes = [ct.c_double]
MsaSetBaseTemp.argtypes = [ct.c_double]
MsaSetSlopeToBase.argtypes = [ct.c_double]
MsaSetStimTemp.argtypes = [ct.c_double]
MsaSetSlopeToStim.argtypes = [ct.c_double]
MsaStim.argtypes = [ct.c_double,ct.c_double,ct.c_double,ct.c_double]
MsaTest.argtypes = [ct.c_int]
checkPortPresent.argtypes = [ct.c_int]
checkMsaPresent.argtypes = [ct.c_int]

# Specifiying functions return value type

MsaGetLastError.restype = ct.c_int
MsaSetIniPathName.restype = ct.c_int
MsaOpen.restype = ct.c_int
MsaOpenWithIniPName.restype = ct.c_int
MsaSetTemp.restype = ct.c_int
MsaSetCriticalTemp.restype = ct.c_int
MsaSetCriticalMaxTime.restype = ct.c_int
MsaSetBaseTemp.restype = ct.c_int
MsaSetSlopeToBase.restype = ct.c_int
MsaSetStimTemp.restype = ct.c_int
MsaSetSlopeToStim.restype = ct.c_int
MsaStim.restype = ct.c_int
MsaGetCurrTemp.restype = ct.c_double
MsaGetCurrTemp.restype = ct.c_double
MsaGetCriticalTemp.restype = ct.c_double
MsaGetCriticalMaxTime.restype = ct.c_double
MsaGetBaseTemp.restype = ct.c_double
MsaGetSlopeToBase.restype = ct.c_double
MsaGetStimTemp.restype = ct.c_double
MsaGetSlopeToStim.restype = ct.c_double
MsaTest.restype = ct.c_char_p
checkPortPresent.restype = ct.c_int
checkMsaPresent.restype = ct.c_int

# enumPorts() : returns available serial ports as a list of port numbers

def enumPorts():
	ports = []
	for i in range(1,11):
		if checkPortPresent(i):
			ports.append(i)
	return ports

# msaSearch(): searches on available serial ports for the MSA unit.
#       returns the port number on which it is connected, zero if it is not connected

def msaSearch():
	ports = enumPorts()
	for port in ports:
		if checkMsaPresent(port):
			return port
	return 0

# Application(tk.Tk) :
# Application(tk.Tk) : A class providing an simple gui for testing the MSA unit.
#       This class will be created if msa.py is invoked directely, i.e. not imported
#       as a Python module

if __name__ == '__main__':
        import Tkinter as tk,tkMessageBox as tkmb
        class Application(tk.Tk):
                def __init__(self,master=None):
                        tk.Tk.__init__(self)
                        self.msaOpened = False
                        self.calibFiles = [x for x in os.listdir('c:\WINDOWS') if 'Thermod' in x and '.ini' in x]
                        if len(self.calibFiles) == 0:
                                tkmb.showerror('MSA test','No calibration INI files found in c:\windows')
                                self.close()
                        self.currCalib = 0
                        self.port = -1
                        self.grid()
                        self.protocol("WM_DELETE_WINDOW", self.close)
                        self.searchDisp = tk.StringVar()
                        self.createWidgets()
                        self.after(100,self.displayCurrTemp)

                def close(self):
                        if self.msaOpened:
                                MsaClose()
                        print('Quit pressed')
                        self.quit()
                        self.destroy()

                def test(self):
                        print self

                def setCalibFile(self,selection):
                        if self.port != -1:
                                #pdb.set_trace()
                                MsaClose()
                                fileName = self.calibFiles[int(selection[0])]
                                MsaSetIniPathName(''.join(('c:\windows\\',fileName)))
                                MsaOpen(self.port)

                def restoreListbox(self,event=None):
                        self.listbox.select_clear(0,tk.END)
                        self.listbox.select_set(self.currCalib)
                        
                def displayCurrTemp(self):
                        if self.port != -1:
                                temp = MsaGetCurrTemp()
                                self.tempLabel.configure(text='%.2f degC' % temp)
                                self.tempLabel.update_idletasks()
                        currSelection = self.listbox.curselection()
                        if len(currSelection) == 0:
                                self.restoreListbox(None)
                                currSelection = self.listbox.curselection()
                        if currSelection != self.currCalib:
                                #pdb.set_trace()
                                self.setCalibFile(currSelection)
                                self.currCalib = currSelection
                        self.after(100,self.displayCurrTemp)
                        
                def portScan(self):
                        ports = enumPorts()
                        retrying = True
                        while retrying:
                                for port in ports:
                                        self.searchLabel.configure(text='Scanning serial ports %d' % port)
                                        self.searchLabel.update_idletasks()
                                        if checkMsaPresent(port):
                                                self.searchLabel.configure(text='MSA connected to port %d' % port)

                                                self.searchLabel.update_idletasks()
                                                MsaOpen(port);
                                                self.msaOpened = True
                                                self.port = port
                                                self.after(100,self.displayCurrTemp)
                                                retrying = False
                                                break
                                if self.port == -1:
                                        self.searchLabel.configure(text='MSA not connected')
                                        retrying = tkmb.askretrycancel('Msa test','Msa device not found\nCheck serial connection',parent=self)
                                        self.searchLabel.update_idletasks()

                def tempValidate(self,event=None):
                        tempStr = self.tempEntry.get()
                        try:
                                temp = float(tempStr)
                        except:
                                pass
                        finally:
                                MsaSetTemp(temp,5.)

                def createWidgets(self):
                        self.font = 'Helvetica 10 bold'

                        self.searchLabel = tk.Label(self,text='',width=20,font=self.font)
                        self.searchLabel.grid(row=1,column=1)

                        self.searchButton = tk.Button(self,text='Port scan',command=self.portScan,font=self.font)
                        self.searchButton.grid(row=1,column=2)

                        lbWidth = max([len(s) for s in self.calibFiles])
                        self.listbox = tk.Listbox(self,height=len(self.calibFiles),width=lbWidth)
                        for file in self.calibFiles:
                                self.listbox.insert(tk.END,file)
                        self.listbox.select_set(0)
                        self.listbox.grid(row=2,column=1,columnspan=2)

                        self.tempValidateButton = tk.Button(self,text='set temp.',command=self.tempValidate,font=self.font);
                        self.tempValidateButton.grid(row=3,column=2)

                        self.tempEntry = tk.Entry(self,font=self.font)
                        self.tempEntry.bind('<Double-Button-1>',self.restoreListbox);
                        self.tempEntry.bind('<Return>',self.tempValidate);
                        self.tempEntry.grid(row=3,column=1)

                        self.tempLabel = tk.Label(self,text='',width=20,font=self.font)
                        self.tempLabel.grid(row=4,column=1,columnspan=2)

        app = Application()
        app.title('MSA tester')
        app.mainloop()

