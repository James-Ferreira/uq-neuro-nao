from naoqi import ALProxy


def dismiss_arm_warning(robot_ip, port=9559):
    """Dismiss arm-related warnings from the robot notification manager."""
    nm = ALProxy("ALNotificationManager", robot_ip, port)
    notes = nm.notifications()

    print("Found {} notification(s).".format(len(notes)))

    removed = []
    for note in notes:
        try:
            data = dict(note)
        except Exception:
            data = note if isinstance(note, dict) else {}
        nid = data.get("id")
        msg = data.get("message", "")
        sev = data.get("severity", "")

        print("id={} severity={} message={}".format(nid, sev, msg))

        if nid is not None and ("Warning 714" in msg or "right arm" in msg):
            nm.remove(nid)
            removed.append(nid)
            print("Removed notification id {}".format(nid))

    if not removed:
        print("No matching arm warning notification found.")
    else:
        print("Done. Removed ids: {}".format(removed))
