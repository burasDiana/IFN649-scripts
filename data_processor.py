import serial
import time
import string
import paho.mqtt.publish as publish
# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different

msg_ok = "Plant is doing all right :)"
msg_hot = "Temperature too high!"
msg_little_hot = "Warning, temperature getting hot!"
msg_cold = "Temperature too low!"
msg_light_low = "Light level too low!"
msg_light_little_low = "Plant could use more light!"
msg_light_high = "Light level too high!"
msg_hum_high = "Humidity level high!"
msg_hum_low = "Humidity level low!"
msg_water = "Moisture getting low, water plant soon!"

TOD = 2
currtime = time.localtime()
if currtime.tm_hour < 6 or currtime.tm_hour > 18:
    TOD = 1 # night
    print("Time period is night")
else:
    TOD = 0 # day
    print("Time period is day")


raw_temp = ""
EC2_IP = "13.127.250.10"
HUM_NORMAL = range(50,90)
HUM_LOW = range(0,50)

HID_MAX = 34
HID_MED = 29

T_HIGH_DAY = 26
T_MED_DAY = 20
T_LOW_NIGHT = 10

L_HIGH = 500
L_NORMAL_DAY = range(200,450)
L_NORMAL_NIGHT = range(60,240)

ser = serial.Serial("/dev/rfcomm0", 9600)
ser.write(str.encode('Start\r\n'))

#based on status we send 0 = green, 1 = red, or 2 = yellow representing the statuses
while True:
    if ser.in_waiting > 0:
        rawserial = ser.readline()
        cookedserial = rawserial.decode('utf-8').strip('\r\n')
        print(cookedserial)
        #x = len(cookedserial)
        #print("length is: " + str(x))

        
        if (len(cookedserial)> 15):
            raw_humidity = cookedserial[11:15]
            raw_temp = cookedserial[32:36]
            raw_hid = cookedserial[52:56]
            ldr = cookedserial[64:67]
            
            h = int(float(raw_humidity))
            t = round(float(raw_temp))
            hid = round(float(raw_hid))
            ldr = int(float(ldr))
            #print(h,t,hid,ldr)
            
            if TOD == 0:
                if t < T_MED_DAY or t > T_HIGH_DAY or hid > HID_MAX or ldr > L_HIGH or h not in HUM_NORMAL:
                    print("status_bad, send red")
                    publish.single("status",1,hostname=EC2_IP)
                    if(t> T_HIGH_DAY):
                        publish.single("notify",msg_hot,hostname=EC2_IP)
                    if(ldr > L_HIGH):
                        publish.single("notify",msg_light_high,hostname=EC2_IP)
                    # publish values or message regarding what to do on phone
                elif t >= T_MED_DAY and t < T_HIGH_DAY and ldr in L_NORMAL_DAY and h in HUM_NORMAL and hid <= HID_MED:
                    print("status_ok, send green")
                    publish.single("status",0,hostname=EC2_IP)
                    publish.single("notify",msg_ok,hostname=EC2_IP)
                else:
                    print("status_ok, but warnings, send yellow")
                    publish.single("status",2,hostname=EC2_IP)
                    if t > (T_HIGH_DAY -2):
                        publish.single("notify",msg_little_hot,hostname=EC2_IP)
                    else:
                        publish.single("notify",msg_water,hostname=EC2_IP)
                        publish.single("notify",msg_light_little_low,hostname=EC2_IP)
            if TOD == 1:
                if t < T_LOW_NIGHT or t > T_HIGH_DAY or hid > HID_MAX or ldr not in L_NORMAL_NIGHT or h not in HUM_NORMAL:
                    print("status_bad, send red, night")
                    publish.single("status",1,hostname=EC2_IP)
                    publish.single("notify",msg_hot,hostname=EC2_IP)
                    publish.single("notify",msg_light_low,hostname=EC2_IP)
                    publish.single("notify",msg_hum_high,hostname=EC2_IP)
                elif t >= T_LOW_NIGHT and t < T_MED_DAY or t < T_HIGH_DAY and ldr in L_NORMAL_DAY and h in HUM_NORMAL and hid <= HID_MED:
                    print("status_ok, send green, night")
                    publish.single("status",0,hostname=EC2_IP)
                    publish.single("notify",msg_ok,hostname=EC2_IP)
                else:
                    print("status_ok, but warnings, send yellow, night")
                    publish.single("status",2,hostname=EC2_IP)
                    publish.single("notify",msg_water,hostname=EC2_IP)
                    publish.single("notify",msg_hum_high,hostname=EC2_IP)