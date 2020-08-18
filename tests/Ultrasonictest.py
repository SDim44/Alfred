import Alf_Ultraschall as distance
import time

while True:
    DistanceOut = distance.get(1)
    print("Rueckgabewert Sensor {0} : {1}".format("1",DistanceOut))

    DistanceOut = distance.get(2)
    print("Rueckgabewert Sensor {0} : {1}".format("2",DistanceOut))

    time.sleep(1)