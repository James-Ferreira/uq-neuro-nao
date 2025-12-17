from src_py2.robot.nao_robot import NAORobot
import urllib2
import json
import time

BRIDGE = "http://127.0.0.1:5055"   # if running on same Mac; otherwise put the Mac mini LAN IP

def post_json(url, payload=None, timeout=10):
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib2.Request(url, data, {"Content-Type": "application/json"})
    resp = urllib2.urlopen(req, timeout=timeout)
    return json.loads(resp.read())

def main():
    clas = NAORobot("clas")

    while True:
        clas.tm.wait_for_left_bumper_press()
        post_json(BRIDGE + "/start")

        clas.tm.wait_for_left_bumper_release()
        result = post_json(BRIDGE + "/stop")

        # Optional: speak the transcript back for debugging only
        # (You don't need this for production)
        txt = result.get("transcript","")
        if txt:
            clas.tts.post.say("You said: {}".format(txt))

        time.sleep(0.05)

if __name__ == "__main__":
    main()
