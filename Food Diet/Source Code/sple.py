from winotify import Notification

toast = Notification(app_id="windows app",
                     title="Winotify Test Toast",
                     msg="New Notification!",
                     icon=r"c:\path\to\icon.png")

toast.show()