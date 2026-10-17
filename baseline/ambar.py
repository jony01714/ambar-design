"""Ambar prototype v0: everything lives in a single class (original design)."""
import json
import sqlite3
import time
import urllib.request

CO2_LIMIT = 1000


class AmbarAssistant:
    def __init__(self, broker="localhost", db_path="ambar.db",
                 llm_url="http://localhost:11434/api/generate", model="llama3.2"):
        import paho.mqtt.client as mqtt  # hard dependency, needs a live broker

        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS readings (ts REAL, node TEXT, kind TEXT, value REAL)"
        )
        self.llm_url = llm_url
        self.model = model
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(broker, 1883)
        self.client.subscribe("ambar/+/+")
        self.client.loop_start()

    # 1-4: MQTT message parsing, persistence and threshold rules
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        node = msg.topic.split("/")[1]
        kind = msg.topic.split("/")[2]
        value = float(data["value"])
        self.db.execute(
            "INSERT INTO readings VALUES (?, ?, ?, ?)", (time.time(), node, kind, value)
        )
        self.db.commit()
        if kind == "co2" and value > CO2_LIMIT:
            print(f"[ALERT] CO2 {value} ppm, open a window")

    # 5-6: prompt building and local LLM inference
    def ask_llm(self, text):
        rows = self.db.execute(
            "SELECT kind, value FROM readings ORDER BY ts DESC LIMIT 10"
        ).fetchall()
        prompt = "You are Ambar. Readings: " + ", ".join(f"{k}={v}" for k, v in rows)
        prompt += f"\nUser: {text}"
        body = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(self.llm_url, body, {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())["response"]

    # 7-8: intent detection and actuator control
    def handle_text(self, text):
        t = text.lower()
        if "motor" in t and ("enciende" in t or "mueve" in t):
            self.client.publish("ambar/motor1/cmd", json.dumps({"action": "on"}))
            return "Moving the motor."
        elif "motor" in t and "apaga" in t:
            self.client.publish("ambar/motor1/cmd", json.dumps({"action": "off"}))
            return "Motor stopped."
        elif "co2" in t or "aire" in t:
            row = self.db.execute(
                "SELECT value FROM readings WHERE kind = 'co2' ORDER BY ts DESC LIMIT 1"
            ).fetchone()
            if row is None:
                return "No CO2 readings yet."
            if row[0] > CO2_LIMIT:
                return f"CO2 is {row[0]} ppm, above the limit."
            return f"CO2 is {row[0]} ppm."
        else:
            return self.ask_llm(text)

    # 9-10: console I/O, configuration and logging
    def run(self):
        while True:
            text = input("> ")
            print(self.handle_text(text))


if __name__ == "__main__":
    AmbarAssistant().run()
