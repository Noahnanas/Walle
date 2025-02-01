import serial
import time

class Walle:
    def __init__(self, port: str):
        self.serial_available = True
        try:
            self.serial = serial.Serial(port, baudrate=9600, timeout=1)
            print(f"✅ Connexion au port {port} réussie.")
        except serial.SerialException as e:
            print(f"❌ Erreur : Impossible d'ouvrir le port {port}.\nDétail : {e}")
            self.serial_available = False
            
        self.coef = {
            "lid_L":1.0,
            "lid_L":1.0,
            "eyebrow_L": 0.0,
            "eyebrow_R": 0.0,
            "UD_L": 0.55,
            "UD_R": 0.6,
            "eye_angle": 0.0,
            "eye_sad": 0.0
        }
        #self.update(self.coef.keys())

    def update(self, tab):
        res = ""
        for key in tab:
            res += f"{key}%{self.coef[key]}\n"
            print(f"🔄 {key} = {self.coef[key]}")

        if self.serial_available:
            self.serial.write(res.encode())
            print("➡️ Envoyé à l'Arduino:\n")

    def blink(self):
        self.coef['lid_L']=0
        self.coef['lid_R']=0
        self.update(['lid_L','lid_R'])
        print("WALL-E cligne des yeux. 1")
        time.sleep(0.15)
        self.coef['lid_L']=1
        self.coef['lid_R']=1
        self.update(['lid_L','lid_R'])
        print("WALL-E cligne des yeux. 2")

    def headAngle(self, angle=None):
        if angle is None:
            angle = self.coef["eye_angle"]
        else:
            self.coef["eye_angle"] = angle

        base_position = 0.6

        UD_L_temp = base_position-0.05 - angle * 0.5
        UD_R_temp = base_position + angle * 0.5

        # Prise en compte de la tristesse
        self.coef["UD_L"] = (1 - self.coef["eye_sad"]) * UD_L_temp
        self.coef["UD_R"] = (1 - self.coef["eye_sad"]) * UD_R_temp

        # Clamping entre 0 et 1
        self.coef["UD_L"] = max(0, min(1, self.coef["UD_L"]))
        self.coef["UD_R"] = max(0, min(1, self.coef["UD_R"]))

        self.update(["UD_L", "UD_R"])

    def eyebrow(self, angle):
        self.coef["eyebrow_L"] = angle
        self.coef["eyebrow_R"] = angle
        self.update(["eyebrow_L", "eyebrow_R"])

    def sadness(self, angle: float):
        self.coef["eye_sad"] = angle
        self.headAngle()
        print(f"Niveau de tristesse réglé à {angle}")
        
    def auto_adjust(self):
        self.headAngle(0)
        self.coef['UD_R']=0
        self.update(['UD_R'])
        time.sleep(1.5)
        self.coef['UD_L']=0
        self.update(['UD_L'])
        time.sleep(1.5)
        self.sadness(0)
        time.sleep(1)
        self.blink()
        time.sleep(1)
        self.sadness(0.7)
        time.sleep(1.5)
        self.sadness(0)
        
    def neutral(self):
        self.coef = {
            "lid_L":0.0,
            "lid_L":0.0,
            "eyebrow_L": 0.0,
            "eyebrow_R": 0.0,
            "UD_L": 0.55,
            "UD_R": 0.6,
            "eye_angle": 0.0,
            "eye_sad": 0.0
        }
        self.update(self.coef.keys())
        

    def close(self):
        if self.serial_available:
            self.serial.close()
        print("Port série fermé.")
