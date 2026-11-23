from typing import Dict

class SmartSignageDisplay:
    def __init__(self, sign_id: str):
        self.sign_id = sign_id
        self.current_message = "WELCOME TO OPENPARK"

    def update_display(self, free_spots: int) -> Dict:
        self.current_message = f"PARKING: {free_spots} SPOTS OPEN" if free_spots > 0 else "PARKING FULL"
        return {"sign_id": self.sign_id, "display_text": self.current_message}
