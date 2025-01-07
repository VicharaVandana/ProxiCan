import time
import threading
from service3e_main import Ui_Service3E
import general as gen

class TimerMonitor(threading.Thread):
    def __init__(self, ui):
        threading.Thread.__init__(self)
        self.ui = ui
        self.daemon = True  # This ensures the thread ends when the main program ends

    def run(self):
        while True:
            time.sleep(1)  # Check every second
            self.monitor_timer()

    def monitor_timer(self):
        # Monitor IsAnyServiceActive and reset the timer if necessary
        if gen.IsAnyServiceActive is False:  # Transition to True, reset the timer
            if self.ui.get_timer() and not self.ui.get_timer().isActive():
                print("IsAnyServiceActive is False, resetting the timer.")
                self.ui.reset_timer(3)  # Reset the timer with the desired interval (e.g., 3 seconds)
        elif gen.IsAnyServiceActive is True:  # Transition to False, stop the timer
            if self.ui.get_timer() and self.ui.get_timer().isActive():
                print("IsAnyServiceActive is True, stopping the timer.")
                self.ui.stop_timer()

def start_monitoring(ui):
    monitor = TimerMonitor(ui)
    monitor.start()

if __name__ == "__main__":
    from service3e_main import Ui_Service3E

    # Initialize the Ui_Service3E object
    ui_service3e = Ui_Service3E()

    # Start monitoring the timer in a separate thread
    start_monitoring(ui_service3e)
    
    # Main program continues running
    print("Monitoring started.")
    while True:
        time.sleep(1)  # Keep the main program running
