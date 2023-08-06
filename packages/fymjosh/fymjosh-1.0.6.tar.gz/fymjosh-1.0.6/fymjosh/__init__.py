
import os, time, sys, websocket, requests, json, logging, datetime

class Colwrite:
    def __init__(self):
        self.red = 40
        self.cycle = 0 
    
    def purplepink(self,text):
        os.system("");faded = ""
        
        
        faded += (f"\033[38;2;{self.red};0;220m{text}")
            
        
        return faded
        
        
    def _write(self,datefmt=' %H:%M:%S.%f - ', text):
        
        print(self.purplepink(f"{datetime.utcnow().strftime(datefmt)}\033[37m{text}"))
        if not self.red == 255 and self.cycle == 0:
            self.red += 15
            
        
            
        if self.red > 255:
            self.cycle += 1
            #self.red -= 15
            
                
        if self.cycle > 0:    
            if self.red > 40:
                self.red -= 15
                       
            if self.red == 40:
                self.cycle = 0



class Status:
    

    def streaming(stream_name:str, atream_url:str):
        return {
            "name": stream_name,
            "type": 1,
            "url": atream_url
        }

    def playing(game_name:str):
        return {
            "name": game_name,
            "type": 0,
        
        }       
    def watching(movie_name:str):
        return {
            "name": movie_name,
            "type": 3,
            
        }
        
    def listening(song_name:str):
        return {
            "name": song_name,
            "type": 2,
           
        }
        
        
class ImproperTokenError(Exception):
    def __init__(self, message="Improper Token has Been Passed"):
        self.message = message
        super().__init__(self.message)
    
        
class Client:
    def __init__(self, status):
        self.token = ""
        self.jsrp = status
        self.ws = websocket.WebSocket()
     
    
     
    def run(self, token:str):
        self.token = token
        r = requests.get(f"https://discord.com/api/v10/users/@me", headers={"Authorization": self.token})
        if r.status_code == 200:
            print(f"token : {self.token}")
            
        elif r.status_code == 401:
            raise ImproperTokenError
            
        
        self.ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
        res = self.ws.recv()
        h = json.loads(res)
        heartbeat = int(h["d"]["heartbeat_interval"])
        
        self.ws.send(json.dumps({"op": 2, "d": {"token": self.token, "properties": {"$os": sys.platform, "$browser": "Discord", "$device": "desktop"}, "presence": {"game": self.jsrp, "status": "online", "since": 0, "afk": False}}, "s": None, "t": None}))
        
        beats = {"op": 1, "d": None}
        while True:
            self.ws.send(json.dumps(beats))
            time.sleep(heartbeat / 1000)
            
    
 

