# to be run within scripts tab of mission planner
import clr
clr.AddReference("MAVLink")
import MAVLink
from MAVLink import mavlink_command_long_t
import MAVLink
import MissionPlanner
import socket
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

try:
  print 'starting socket'
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print 'binding socket'
  s.bind((HOST, PORT))
  print 'listening socket'
  s.listen(5)
  print 'outside while loop'
  while True:
    # print 'inside while loop'
    (conn, addr) = s.accept()
    # print 'receive data'
    data = conn.recv(1024)
    print 'Relay high - sprayer on'
    MAV.doCommand(MAVLink.MAV_CMD.DO_SET_RELAY, 0, 1, 0, 0, 0, 0, 0);
    Script.Sleep(700)
    # print 'Relay low - sprayer off'
    MAV.doCommand(MAVLink.MAV_CMD.DO_SET_RELAY, 0, 0, 0, 0, 0, 0, 0);
    # print 'echo back data'
    conn.sendall(data) # this is just an echo of what we received. No need but let it be
except:
  print 'got to except - pass'
  pass
finally:
  print 'got to finally - closing'
  s.close()


s.close()

# ORIGINAL TEST CODE:
# lots of iron python script examples in C:\Program Files (x86)\Mission Planner\Scripts
# this is copied from there - just sets aux5 (relay 0) to 3.3V or 0V and sleeps 5 seconds
#print 'Start Script'
#print 'Relay high - sprayer on'
#MAV.doCommand(MAVLink.MAV_CMD.DO_SET_RELAY, 0, 1, 0, 0, 0, 0, 0);
#Script.Sleep(1000)
#print 'Relay low - sprayer off'
#MAV.doCommand(MAVLink.MAV_CMD.DO_SET_RELAY, 0, 0, 0, 0, 0, 0, 0);
#Script.Sleep(1000)
#print 'Relay high'
#MAV.doCommand(MAVLink.MAV_CMD.DO_SET_RELAY, 0, 1, 0, 0, 0, 0, 0);
#Script.Sleep(1000)
#print 'Relay low'
#MAV.doCommand(MAVLink.MAV_CMD.DO_SET_RELAY, 0, 0, 0, 0, 0, 0, 0);
#Script.Sleep(1000)
#My forum question: https://discuss.ardupilot.org/t/is-it-possible-to-turn-on-off-a-gpio-pin-on-cube-orange-quadcopter-programatically/82387