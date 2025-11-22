from app_window import AppWindow

from classes.queue import Queue

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()

    q = Queue()
    # q.add(10)
    for i in range(10):
        q.add(i)

    q.print()
