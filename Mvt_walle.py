import serial
import time

class Walle:
    def __init__(self, port: str):
        self.serial_available = True
        try:
            self.serial = serial.Serial(port, baudrate=9600, timeout=1)
            print(f"[Mvt_Walle] ✅ Connexion au port {port} réussie.")
        except serial.SerialException as e:
            print(f"[Mvt_Walle] ❌ Erreur : Impossible d'ouvrir le port {port}.\n")
            self.serial_available = False
        
            
        self.coef_init = {
            "lid_L":1.0,
            "lid_R":1.0,
            "eyebrow_L": 0.0,
            "eyebrow_R": 0.0,
            "UD_L": 0.55,
            "UD_R": 0.6,
            "eye_angle": 0.0,
            "eye_sad": 0.0,
            "neck_U":0.0,
            "neck_L":0.0,
            "neck_LR":0.0,
            "neck_level":0.5,
            "neck_angle":0.0,
            "arm_L":0.5,
            "arm_R":0.5,
            "hand_L":1.0,
            "hand_R":1.0
        }
        self.coef = self.coef_init.copy()
        #self.update(self.coef.keys())

    def update(self, tab):
        res = ""
        for key in tab:
            res += f"{key}%{self.coef[key]}\n"
            print(f"[Mvt_Walle] 🔄 {key} = {self.coef[key]}")

        if self.serial_available:
            self.serial.write(res.encode())
            print("[Mvt_Walle] ➡️ Envoyé à l'Arduino:\n")
        else:
            print("[Mvt_Walle] Erreur envoie arduino\n")

    def blink(self):
        self.coef['lid_L']=0
        self.coef['lid_R']=0
        self.update(['lid_L','lid_R'])
        print("[Mvt_Walle] WALL-E cligne des yeux. 1")
        time.sleep(0.15)
        self.coef['lid_L']=1
        self.coef['lid_R']=1
        self.update(['lid_L','lid_R'])
        
    def manual(self,name,angle):
        self.coef[name]=angle
        print(f"[Mvt_Walle] {self.coef}")
        self.update([name])

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

        self.coef["UD_L"] = max(0, min(1, self.coef["UD_L"]))
        self.coef["UD_R"] = max(0, min(1, self.coef["UD_R"]))

        self.update(["UD_L", "UD_R"])
        
    def neckLR(self, angle):
        self.coef["neck_LR"]=angle
        self.update(["neck_LR"])

    def eyebrow(self, angle):
        self.coef["eyebrow_L"] = angle
        self.coef["eyebrow_R"] = angle
        self.update(["eyebrow_L", "eyebrow_R"])

    def sadness(self, angle):
        self.coef["eye_sad"] = angle
        self.headAngle()
        print(f"[Mvt_Walle] Niveau de tristesse réglé à {angle}")
        
    def neckLevel(self, headLevel=None):
        neckAngle = self.coef["neck_angle"]

        if headLevel is None:
            headLevel = self.coef["neck_level"]
        else:
            self.coef["neck_level"] = headLevel

        neck_L_temp = (1 - neckAngle) * headLevel
        neck_U_temp = neckAngle + (1 - neckAngle) * headLevel

        self.coef["neck_L"] = max(0, min(1, neck_L_temp))
        self.coef["neck_U"] = max(0, min(1, neck_U_temp))

        self.update(["neck_L", "neck_U"])
        
    def neckAngle(self, neckAngle=None):
        self.coef["neck_angle"] = neckAngle
        self.neckLevel()
        
    def auto_adjust(self):
        self.headAngle(0)
        self.coef['UD_R']=0
        self.update(['UD_R'])
        time.sleep(1)
        self.coef['UD_L']=0
        self.update(['UD_L'])
        time.sleep(1)
        self.sadness(0)
        time.sleep(1)
        self.blink()
        time.sleep(0.7)
        self.sadness(0.7)
        time.sleep(1)
        self.sadness(0)
        
    def sleep(self):
        self.coef = self.coef_init.copy()
        self.update(self.coef.keys())
        

    def close(self):
        if self.serial_available:
            self.serial.close()
        print("[Mvt_Walle] Port série fermé.")
