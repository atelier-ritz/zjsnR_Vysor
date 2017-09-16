
class MotorManager(object):
    def __init__(self,client):
        self.client = client
        self.rpm = [20, 20]
        self.stepperrev = [100, 100]
        self.origin = [0, 0]
        self.corner = [0, 0]
        self.position = [0, 0]

    def setOrigin(self,x,y):
        self.origin = [x, y]
    def setCorner(self,x,y):
        self.corner = [x, y]

    def _sendCommand(self,command):
        client = self.client
        client.send_data(command)

    def motorgo(self,motorId,val):
        if val == 0 :
            return
        step = abs(val)
        direction = int(val/step)
        self.position[motorId] += val
        command = 'motorgo{},{},{}'.format(motorId+1,step,direction)
        self._sendCommand(command)
    def touch(self,period):
        command = 'touch,{}'.format(period)
        self._sendCommand(command)
    def setParam(self,rpm1,rpm2,stepperrev1,stepperrev2):
        command = 'setparam,{},{},{},{}'.format(rpm1,rpm2,stepperrev1,stepperrev2)
        self._sendCommand(command)

    def motorGoTo(self,motorId,goal_steps):
        current = self.position[motorId]
        val = goal_steps - current
        self.motorgo(motorId, val)
    def motorGoToX(self,goal_pixel):
        goal_steps = int((self.corner[0] - self.origin[0]) / 1920 * goal_pixel + self.origin[0])
        val = goal_steps - self.position[0]
        self.motorgo(0, val)
    def motorGoToY(self,goal_pixel):
        goal_steps = int((self.corner[1] - self.origin[1]) / 1080 * goal_pixel + self.origin[1])
        val = goal_steps - self.position[1]
        self.motorgo(1, val)
