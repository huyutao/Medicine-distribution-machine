# -*- coding: utf-8 -*-
"""
Created on Sun Nov 06 03:37:11 2016

@author: Max
"""

import kivy
kivy.require('1.9.1')
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from subprocess import check_call

class Patient():
    pat_id = 0
    first_name = ""
    last_name = ""
    dob = ""
    gender = ""
    height = ""
    weight = ""
    number = ""
    blood_type = ""
    photo_addr = ""
    has_med = False
    med1 = 0
    med2 = 0
    med3 = 0

patient_data = []

"""
def inputPatients():
    pass

def outputPatients():
    target = open("patients.txt", 'w')
    target.truncate()
    for pat in patient_data:
        print("writing")
        target.write(pat.first_name+"\n")
        print("writing")
        target.write(pat.last_name+"\n")
        target.write(pat.dob+"\n")
        target.write(pat.gender+"\n")
        target.write(pat.weight+"\n")
        target.write(pat.height+"\n")
        target.write(pat.number+"\n")
        target.write(pat.blood_type+"\n")
        target.write(str(pat.has_med)+"\n")
        target.write(str(pat.med0)+"\n")
        target.write(str(pat.med1)+"\n")
        target.write(str(pat.med2)+"\n\n")
        print("done")
    target.close()
"""
root_dir = "/home/yutao/PycharmProjects/archhack/doctor"

def createNewProfile(pat):
    if not os.path.exists(root_dir+"/Data"):
        os.makedirs(root_dir+"/Data")
    ctr = 1
    while os.path.exists(root_dir+"/Data/"+str(ctr)):
        ctr = ctr + 1
    os.makedirs(root_dir+"/Data/"+str(ctr))
    if(os.path.exists(root_dir+"/face.jpg")):
        check_call(("mv face.jpg Data/" + str(ctr)).split(" "))
    if not os.path.exists(root_dir+"/Temp"):
        os.makedirs(root_dir+"/Temp")
    return ctr

def createPrescribe(pat):
    if not os.path.exists(root_dir+"/Data/"+str(pat.pat_id)):
        print("path 1 missing: "+root_dir+"/Data/"+str(pat.pat_id))
        return
    if not os.path.exists(root_dir+"/Temp"):
        print("path 2 missing")
        return
    target = open(root_dir+"/Data/"+str(pat.pat_id)+"/medicines", 'w')
    while pat.med1:
        target.write("1\n")
        pat.med1 = pat.med1 - 1
    while pat.med2:
        target.write("2\n")
        pat.med2 = pat.med2 - 1
    while pat.med3:
        target.write("3\n")
        pat.med3 = pat.med3 - 1
    target.close()
    target = open(root_dir+"/Temp/request", 'a')
    target.write(str(pat.pat_id)+"\n")
    target.close()
    pat.has_med = False

Builder.load_file("doctor.kv")

screen_manager = ScreenManager()

class PatientListButton(ListItemButton):
    pass

class ScreenLogin(Screen):
    login_fail_text = ObjectProperty()
    
    # function that handles a login request
    def login(self, username, password):
        
        if ((username == str("admin")) & (password == str("admin"))):
            self.login_fail_text.text = ""
            screen_manager.transition.direction = "up"
            screen_manager.transition.duration = 1
            screen_manager.current = "screen_list"
        else:
            self.login_fail_text.text = "Incorrect username and/or password!"
        """
        self.login_fail_text.text = ""
        screen_manager.transition.direction = "up"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_list"
        """
            
class ScreenList(Screen):
    # function that creates a popup window with two button when logout is pressed
    def open_logout_popup(self):
        self.box=FloatLayout()
        self.label_text = (Label(text="Are you sure to logout?",font_size=15,
        	size_hint=(None,None),pos_hint={'x':.25,'y':.6}))
        self.box.add_widget(self.label_text)
        self.button_yes = (Button(text="Yes",size_hint=(None,None),
        	width=200,height=50,pos_hint={'x':0,'y':0}))
        self.box.add_widget(self.button_yes)
        self.button_no = (Button(text="No",size_hint=(None,None),
        	width=200,height=50,pos_hint={'x':.5,'y':0}))
        self.box.add_widget(self.button_no)
        self.popup = Popup(title="Logout",content=self.box,
        	size_hint=(None,None),size=(450,300),auto_dismiss=False,title_size=15)
        self.button_yes.bind(on_release=self.logout)
        self.button_no.bind(on_release=self.popup.dismiss)
        self.popup.open()
    
    # do the actual logout after the user confirms
    def logout(self, button):
        screen_manager.transition.direction = "down"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_login"
        self.popup.dismiss()
    
    # go to edit the selected patient
    def edit(self):
        if self.patient_list.adapter.selection:
            # set up selected patient
            selection = self.patient_list.adapter.selection[0].text
            ind = self.patient_list.adapter.data.index(selection)
            selected_patient = patient_data[ind]
            screenedit = self.manager.get_screen("screen_edit_patient")
            screenedit.first_name_text_input.text = selected_patient.first_name
            screenedit.last_name_text_input.insert_text(selected_patient.last_name)
            screenedit.dob_text_input.insert_text(selected_patient.dob)
            screenedit.weight_text_input.insert_text(selected_patient.weight)
            screenedit.height_text_input.insert_text(selected_patient.height)
            screenedit.number_text_input.insert_text(selected_patient.number)
            screenedit.male_checkbox.active = (selected_patient.gender == "Male")
            screenedit.female_checkbox.active = (selected_patient.gender == "Female")
            screenedit.other_gender_checkbox.active = (selected_patient.gender == "Other")
            screenedit.a_type_checkbox.active = (selected_patient.blood_type == "A")
            screenedit.b_type_checkbox.active = (selected_patient.blood_type == "B")
            screenedit.o_type_checkbox.active = (selected_patient.blood_type == "O")
            screenedit.ab_type_checkbox.active = (selected_patient.blood_type == "AB")
            screenedit.has_med_switch.active = selected_patient.has_med
            screenedit.med_1_text_input.text = str(selected_patient.med1)
            screenedit.med_2_text_input.text = str(selected_patient.med2)
            screenedit.med_3_text_input.text = str(selected_patient.med3)
            screenedit.ind = ind
            # move to screen
            screen_manager.transition.direction = "left"
            screen_manager.transition.duration = 1
            screen_manager.current = "screen_edit_patient"
    
class BaseEditScreen(Screen):
    first_name_text_input = ObjectProperty()
    last_name_text_input = ObjectProperty()
    dob_text_input = ObjectProperty()
    weight_text_input = ObjectProperty()
    height_text_input = ObjectProperty()
    number_text_input = ObjectProperty()
    
    male_checkbox = ObjectProperty()
    female_checkbox = ObjectProperty()
    other_gender_checkbox = ObjectProperty()
    a_type_checkbox = ObjectProperty()
    b_type_checkbox = ObjectProperty()
    o_type_checkbox = ObjectProperty()
    ab_type_checkbox = ObjectProperty()
    
    def takePhoto(self):
        check_call("fswebcam -r 640x480 --jpeg 85 -D 1 face.jpg".split(' '))

    def save(self):
        if ((self.first_name_text_input.text == "") |
            (self.last_name_text_input.text == "") #|
            #(self.dob_text_input.text == "") |
            #(self.weight_text_input.text == "") |
            #(self.height_text_input.text == "") |
            #(self.number_text_input.text == "") |
            #(self.photo_addr == "") |
            #(((self.male_checkbox.active) | (self.female_checkbox.active) | 
            #  (self.other_gender_checkbox.active)) is False) |
            #(((self.a_type_checkbox.active) | (self.b_type_checkbox.active) |
            #  (self.o_type_checkbox.active) | (self.ab_type_checkbox.active)) is False)
            ):
            #print(((self.male.value) | (self.female.value) | (self.other_gender.value)) is False)
            #print(((self.a_type) | (self.b_type) | (self.o_type) | (self.ab_type)) is False)
            self.reportError()
        else:
            ind = self.overwritePat()
            if ind is -1:
                pat = Patient()
            else:
                pat = patient_data[ind]
            pat.first_name = self.first_name_text_input.text
            pat.last_name = self.last_name_text_input.text
            pat.dob = self.dob_text_input.text
            pat.gender = "Male" if self.male_checkbox.active else ("Female" if self.female_checkbox.active else ("Other" if self.other_gender_checkbox.active else ""))
            pat.height = self.height_text_input.text
            pat.weight = self.weight_text_input.text
            pat.number = self.number_text_input.text
            pat.blood_type = "A" if self.a_type_checkbox.active else ("B" if self.b_type_checkbox.active else ("O" if self.o_type_checkbox.active else ("AB" if self.ab_type_checkbox.active else "")))
            #pat.photo_addr = ""
            self.otherSave(ind)
            self.submitPatient(pat)
            self.clean()
    
    def overwritePat(self):
        return -1
            
    def otherSave(self, ind):
        pass
    
    def reportError(self):
        pass
        
    def submitPatient(self, ind):
        pass
            
    def clean(self):
        self.first_name_text_input.text = ""
        self.last_name_text_input.text = ""
        self.dob_text_input.text = ""
        self.weight_text_input.text = ""
        self.height_text_input.text = ""
        self.number_text_input.text = ""
        #self.photo_addr = ""
        self.male_checkbox.active = False
        self.female_checkbox.active = False
        self.other_gender_checkbox.active = False
        self.a_type_checkbox.active = False
        self.b_type_checkbox.active = False
        self.o_type_checkbox.active = False
        self.ab_type_checkbox.active = False
        self.otherClean()
        self.goBack()
        
    def otherClean(self):
        pass
    
    def goBack(self):
        pass
    
class ScreenAddPatient(BaseEditScreen):
    add_fail_text = ObjectProperty()
    
    def submitPatient(self, pat):
        screenlist = self.manager.get_screen("screen_list")
        screenlist.patient_list.adapter.data.extend([pat.first_name + " " + pat.last_name])
        screenlist.patient_list._trigger_reset_populate()
        pat.pat_id = createNewProfile(pat)
        patient_data.append(pat)
        #print(patient_data[-1].pat_id)

    def reportError(self):
        self.add_fail_text.text = "Please fill in name information"
        
    def otherClean(self):
        self.add_fail_text.text = ""
        #super(ScreenAddPatient, self).clean()
        
    def goBack(self):
        screen_manager.transition.direction = "left"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_list"

class ScreenEditPatient(BaseEditScreen):
    #selected_patient = None;
    edit_fail_text = ObjectProperty()
    med_1_text_input = ObjectProperty()
    med_2_text_input = ObjectProperty()
    med_3_text_input = ObjectProperty()
    has_med_switch = ObjectProperty()
    
    ind = -1
    
    def overwritePat(self):
        return self.ind
    
    def otherSave(self, ind):
        if ind is -1:
            return
        if self.has_med_switch.active is True:
            pat = patient_data[ind]
            pat.has_med = self.has_med_switch.active
            try:
                pat.med1 = eval(self.med_1_text_input.text)
                pat.med2 = eval(self.med_2_text_input.text)
                pat.med3 = eval(self.med_3_text_input.text)
            except Exception:
                pass
            patient_data[ind] = pat
        
    def submitPatient(self, pat):
        if self.ind >= 0:
            #pat = patient_data[ind]
            screenlist = self.manager.get_screen("screen_list")
            screenlist.patient_list.adapter.data[self.ind] = pat.first_name + " " + pat.last_name
            screenlist.patient_list._trigger_reset_populate()
            patient_data[self.ind] = pat
            self.ind = -1
            if pat.has_med & (pat.med1 + pat.med2 + pat.med3 > 0):
                #print("prescribe" + str(pat.pat_id))
                createPrescribe(pat)
        
    def reportError(self):
        self.edit_fail_text.text = "Please fill in name information"

    def otherClean(self):
        self.ind = -1
        self.edit_fail_text.text = ""
        self.has_med_switch.active = False
        #super(ScreenEditPatient, self).clean()

    def goBack(self):
        screen_manager.transition.direction = "right"
        screen_manager.transition.duration = 1
        #Clock.schedule_once(self.shift_screen, .3)
        screen_manager.current = "screen_list"
    

screen_manager.add_widget(ScreenLogin(name="screen_login"))
screen_manager.add_widget(ScreenList(name="screen_list"))
screen_manager.add_widget(ScreenAddPatient(name="screen_add_patient"))
screen_manager.add_widget(ScreenEditPatient(name="screen_edit_patient"))

class DoctorApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return screen_manager

doctor_app = DoctorApp()
doctor_app.run()