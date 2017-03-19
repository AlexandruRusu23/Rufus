import Surveillance
import DataManager
import time

def main():
    surveillance = Surveillance.Surveillance(640, 480, 30)
    dataManager = DataManager.DataManager('/dev/ttyACM0', 9600, 'test1.db')

    surveillance.start()
    dataManager.start()

    time.sleep(20)

    surveillance.Stop()
    dataManager.Stop()

if __name__ == '__main__':
    main()
