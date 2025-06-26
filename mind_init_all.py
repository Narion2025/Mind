import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import scrolledtext

processes = {}


def start_process(name, cmd):
    if name in processes and processes[name].poll() is None:
        return
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    processes[name] = proc
    threading.Thread(target=_pipe_output, args=(name, proc), daemon=True).start()


def _pipe_output(name, proc):
    for line in proc.stdout:
        log.insert(tk.END, f"[{name}] {line}")
        log.see(tk.END)
    proc.wait()
    log.insert(tk.END, f"[{name}] exited\n")
    log.see(tk.END)
    processes.pop(name, None)


def start_server():
    start_process("server", ["python3", "mind_bus_api.py"])
    webbrowser.open("http://localhost:8000/dashboard")


def start_agent_gateway():
    start_process("gateway", ["python3", "wirklichkeits-api/gateway.py"])


def start_html():
    start_process("dashboard", ["node", "server.js"])
    webbrowser.open("http://localhost:8001")


root = tk.Tk()
root.title("Mind Init")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="x")

btn1 = tk.Button(frame, text="Start Server", command=start_server)
btn1.pack(fill="x")

btn2 = tk.Button(frame, text="Start Agent Integration", command=start_agent_gateway)
btn2.pack(fill="x", pady=5)

btn3 = tk.Button(frame, text="Start Dashboard", command=start_html)
btn3.pack(fill="x")

log = scrolledtext.ScrolledText(root, height=20)
log.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
