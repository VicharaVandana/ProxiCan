from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
from service19_base import Ui_Form_SID_19
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service19_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
import configure as conf
import os



class Ui_Service19(Ui_Form_SID_19):
    def redesign_ui(self):
        pass    
        
    def connectFunctions(self):
        self.pushButton_Send19Req.clicked.connect(self.send19service)
        self.pushButton_reset.clicked.connect(self.clearform)
        self.pushButton_appendLog.clicked.connect(self.addlog)
        self.pushButton_clearLog.clicked.connect(self.clearlog)
        return
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return
    
    def clearform(self):
        #Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType.setText("No Response")
        self.textBrowser_Resp.clear()
        self.Subfunction.setCurrentIndex(0)        
        self.checkBox_suppressposmsg.setChecked(False)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 19 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 19 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 28 window clicked.")
        return
    
    def send19service(self):
        index_subfunction_type = self.Subfunction.currentIndex()
        subfun_type = fun.get_subfunction(index_subfunction_type)
        subfun_type_name=fun.getsubfunction_name(subfun_type)
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()

        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 

        ###############################################################
        if(index_subfunction_type==0 or index_subfunction_type==1):
        
            DTCStatusMask_string = self.lineEdit_DTCStatusMask.text().strip().replace(" ","").replace(" ","").replace(" ","")
        #gen.log_action("Button Click", f"Send 19 request button clicked with DTC[{DTCStatusMask_string}].")


            if(False == gen.check_1Bytehexadecimal(DTCStatusMask_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Status Mask. It must be 1 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Status Mask format")
                return 

            self.update_status("DTC Status Mask is validated.")
            service_request = fun.form_reqmsg4srv19_subfun_1_2_0F_11_12_13(subfun_type,DTCStatusMask_string,sprmib_flg)
            print(f"the service request is : {service_request}")


            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):


                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Subfunction Type: Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name} </I></p>
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p>       

    '''

            elif(response.type == "Negative Response"):
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
    '''
                
            elif(response.type == "Unknown Response Type"):
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            elif(response.type == "No Response"):
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            else:
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
            #Update the response data on userform
            self.label_ResType.setText(response.type)
            self.textBrowser_Resp.setHtml(response_html)

            current_user = os.getlogin()
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            soup = BeautifulSoup(response_html, 'html.parser')
            response_text = soup.get_text()

            self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
    UDS Request :   [{" ".join(hex(number) for number in service_request)}]
    Explaination:   Read DTC information service 19 requested for subfunction {subfun_type_name} with DTC Status Mark {DTCStatusMask_string}
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''
            
        if(index_subfunction_type==3):
        
            DTCMaskRecord_string = self.lineEdit_DTCMaskRecord.text().strip().replace(" ","").replace(" ","").replace(" ","")
            DTCSExtDataRecordNumber_string=self.lineEdit_ExtDataRecordNumber.text().strip().replace(" ","").replace(" ","").replace(" ","")
        #gen.log_action("Button Click", f"Send 19 request button clicked with DTC[{DTCStatusMask_string}].")


            if(False == gen.check_3Bytehexadecimal(DTCMaskRecord_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Mask Record. It must be 3 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Mask Record format")
                return 
            self.update_status("DTC Mask Record is validated.")
            
            if(False == gen.check_1Bytehexadecimal(DTCSExtDataRecordNumber_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC External Data Record Number. It must be 1 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Snapshot External Data Number format")
                return 

            self.update_status("DTC External Data Record Number is validated.")
            service_request = fun.form_reqmsg4srv19_subfun_6_10(subfun_type,DTCMaskRecord_string,DTCSExtDataRecordNumber_string,sprmib_flg)
            print(f"the service request is : {service_request}")


            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):


                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Subfunction Type: Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name} with DTC Mask Record {DTCMaskRecord_string} and DTC Exteranal Data Record Number{DTCSExtDataRecordNumber_string}</I></p>
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p>       
    '''

            elif(response.type == "Negative Response"):
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
    '''
                
            elif(response.type == "Unknown Response Type"):
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            elif(response.type == "No Response"):
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            else:
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
            #Update the response data on userform
            self.label_ResType.setText(response.type)
            self.textBrowser_Resp.setHtml(response_html)

            current_user = os.getlogin()
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            soup = BeautifulSoup(response_html, 'html.parser')
            response_text = soup.get_text()

            self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
    UDS Request :   [{" ".join(hex(number) for number in service_request)}]
    Explaination:   Read DTC information service 19 requested for subfunction {subfun_type_name} with DTC Mark Record {DTCMaskRecord_string} and DTC Snapcshot Record Number of {DTCSExtDataRecordNumber_string}
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''

        elif(index_subfunction_type==2):
        
            DTCMaskRecord_string = self.lineEdit_DTCMaskRecord.text().strip().replace(" ","").replace(" ","").replace(" ","")
            DTCSnapshotRecordNumber_string=self.lineEdit_DTCSnapshotRecordNumber.text().strip().replace(" ","").replace(" ","").replace(" ","")
        #gen.log_action("Button Click", f"Send 19 request button clicked with DTC[{DTCStatusMask_string}].")


            if(False == gen.check_3Bytehexadecimal(DTCMaskRecord_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Mask Record. It must be 3 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Mask Record format")
                return 
            self.update_status("DTC Mask Record is validated.")
            
            if(False == gen.check_1Bytehexadecimal(DTCSnapshotRecordNumber_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Snapshot Record Number. It must be 1 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Snapshot Record Number format")
                return 

            self.update_status("DTC Snapshot Record Number is validated.")
            service_request = fun.form_reqmsg4srv19_subfun_3_4(subfun_type,DTCMaskRecord_string,DTCSnapshotRecordNumber_string,sprmib_flg)
            print(f"the service request is : {service_request}")


            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):


                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Subfunction Type: Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name} </I></p>
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p>       
    '''

            elif(response.type == "Negative Response"):
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
    '''
                
            elif(response.type == "Unknown Response Type"):
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            elif(response.type == "No Response"):
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            else:
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
            #Update the response data on userform
            self.label_ResType.setText(response.type)
            self.textBrowser_Resp.setHtml(response_html)

            current_user = os.getlogin()
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            soup = BeautifulSoup(response_html, 'html.parser')
            response_text = soup.get_text()

            self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
    UDS Request :   [{" ".join(hex(number) for number in service_request)}]
    Explaination:   Read DTC information service 19 requested for subfunction {subfun_type_name} with DTC Mark Record {DTCMaskRecord_string} and DTC Snapcshot Record Number of {DTCSnapshotRecordNumber_string}
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''

        elif(index_subfunction_type==4 or index_subfunction_type==5):
        
            DTCSeverityMaskRecord_string = self.lineEdit_SeverityMaskRecord.text().strip().replace(" ","").replace(" ","").replace(" ","")
        #gen.log_action("Button Click", f"Send 19 request button clicked with DTC[{DTCSeverityMaskRecord_string}].")


            if(False == gen.check_2Bytehexadecimal(DTCSeverityMaskRecord_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Severity Mask Record. It must be 2 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Severity Mask Record format")
                return 
            self.update_status("DTC Severity Mask Record is validated.")

            service_request = fun.form_reqmsg4srv19_subfun_7_8(subfun_type,DTCSeverityMaskRecord_string,sprmib_flg)
            print(f"the service request is : {service_request}")


            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):


                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Subfunction Type: Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name} with DTC Severity Mask Record {DTCSeverityMaskRecord_string}</I></p>
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p>       
    '''

            elif(response.type == "Negative Response"):
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
    '''
                
            elif(response.type == "Unknown Response Type"):
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            elif(response.type == "No Response"):
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            else:
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
            #Update the response data on userform
            self.label_ResType.setText(response.type)
            self.textBrowser_Resp.setHtml(response_html)

            current_user = os.getlogin()
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            soup = BeautifulSoup(response_html, 'html.parser')
            response_text = soup.get_text()

            self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
    UDS Request :   [{" ".join(hex(number) for number in service_request)}]
    Explaination:   Read DTC information service 19 requested for subfunction {subfun_type_name} with DTC Severity Mark Record {DTCSeverityMaskRecord_string} 
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''    
        
        elif(index_subfunction_type==6):
        
            DTCMaskRecord_string = self.lineEdit_DTCMaskRecord.text().strip().replace(" ","").replace(" ","").replace(" ","")
        #gen.log_action("Button Click", f"Send 19 request button clicked with DTC[{DTCStatusMask_string}].")


            if(False == gen.check_3Bytehexadecimal(DTCMaskRecord_string)):
                #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Mask Record. It must be 3 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 Request not happened due to invalid DTC Mask Record format")
                return 
            self.update_status("DTC Mask Record is validated.")
            
            service_request = fun.form_reqmsg4srv19_subfun_9(subfun_type,DTCMaskRecord_string,sprmib_flg)
            print(f"the service request is : {service_request}")


            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):


                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Subfunction Type: Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name} and DTC Status mask {DTCMaskRecord_string}</I></p>
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p> 
    '''

            elif(response.type == "Negative Response"):
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
    '''
                
            elif(response.type == "Unknown Response Type"):
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            elif(response.type == "No Response"):
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            else:
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
            #Update the response data on userform
            self.label_ResType.setText(response.type)
            self.textBrowser_Resp.setHtml(response_html)

            current_user = os.getlogin()
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            soup = BeautifulSoup(response_html, 'html.parser')
            response_text = soup.get_text()

            self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
    UDS Request :   [{" ".join(hex(number) for number in service_request)}]
    Explaination:   Read DTC information service 19 requested for subfunction {subfun_type_name} with DTC Mark Record {DTCMaskRecord_string} 
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''
        
        elif(index_subfunction_type==7 or index_subfunction_type==8 or index_subfunction_type==9):
            print("HERE")
            service_request = fun.form_reqmsg4srv19_subfun_A_B_C_D_E_14_15(subfun_type,sprmib_flg)
            print(f"the service request is : {service_request}")

            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 19 request is sent")
            gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):
                

                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Control Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name}</I></p>
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p> 
    '''

            elif(response.type == "Negative Response"):
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
    '''
                
            elif(response.type == "Unknown Response Type"):
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            elif(response.type == "No Response"):
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
    '''
            else:
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
            #Update the response data on userform
            self.label_ResType.setText(response.type)
            self.textBrowser_Resp.setHtml(response_html)

            current_user = os.getlogin()
            currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            soup = BeautifulSoup(response_html, 'html.parser')
            response_text = soup.get_text()

            self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
    UDS Request :   [{" ".join(hex(number) for number in service_request)}]
    Explaination:   Read DTC information Requested for subfunction {subfun_type_name} 
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''
#         elif(index_subfunction_type==10):
#             service_request = fun.form_reqmsg4srv19_subfun_clear(sprmib_flg)
#             print(f"the service request is : {service_request}")

#             #Send the service request        
#             response = uds.sendRequest(service_request, True)
            
#             self.update_status("Service 19 request is sent")
#             gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
#             ##############################################################
                
#             response = uds.sendRequest(service_request, IsPosResExpected)
            
#             self.update_status("Service 19 request is sent")
#             gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

#             if(response.type == "Positive Response"):
                

#                 response_html = f'''<h4><U>Positive Response Recieved</U></h4>
#         <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
#         <p><strong>Control Type:</strong> <I>{hex(response.resp[1])} {subfun_type_name}</I></p>
#         <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
#         <p><strong>Info:</strong> <I>Service 19 is successfully sent with subfunction {subfun_type_name}</I></p> 
#     '''

#             elif(response.type == "Negative Response"):
#                 response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
#         <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
#         <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
#         <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
#         <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
#     '''
                
#             elif(response.type == "Unknown Response Type"):
#                 response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
#         <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
#     '''
#             elif(response.type == "No Response"):
#                 response_html = f'''<h4><U>No Response Recieved</U></h4>    
#         <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
#         <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
#     '''
#             else:
#                 response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

            
#             #Update the response data on userform
#             self.label_ResType.setText(response.type)
#             self.textBrowser_Resp.setHtml(response_html)

#             current_user = os.getlogin()
#             currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             soup = BeautifulSoup(response_html, 'html.parser')
#             response_text = soup.get_text()

#             self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
#     UDS Request :   [{" ".join(hex(number) for number in service_request)}]
#     Explaination:   Read DTC information Requested for subfunction {subfun_type_name} 
#     UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
#     Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->
            
# '''


if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID19 = QtWidgets.QWidget()
    ui = Ui_Service19()
    ui.setupUi(Form_SID19)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    #os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')

    #conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
    #conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID19.show()
    sys.exit(app.exec_())
