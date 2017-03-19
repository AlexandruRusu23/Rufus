import Surveillance
import DataManager
import time

def main():
    """surveillance = Surveillance.Surveillance(640, 480, 30)"""
    dataManager = DataManager.DataManager('/dev/ttyUSB0', 9600, 'test_create_DB')

    """surveillance.start()"""
    dataManager.start()

    time.sleep(10)

    """surveillance.Stop()"""
    dataManager.Stop()

if __name__ == '__main__':
    main()
