import json
from database import Database


class Lift:
    def __init__(self):
        self.data = self.load_lift_data()

    def load_lift_data(self) -> object:
        db = Database()
        db.connect()
        return db

    def add_data(self, lift_name: str, user: str, data: dict[str, str]) -> None:
        self.data.execute("INSERT INTO lifts (blockid, userid, liftname, date, weight, sets, reps, rpe, topset) "
                          "VALUES ((SELECT blockid FROM blocks WHERE "
                          "name = %s),(SELECT userid FROM users WHERE username = %s) , %s, %s, %s, %s, %s, %s, %s)",
                          (data["block"], user, lift_name, data["date"], data["weight"], data["sets"], data["reps"],
                           data["rpe"], data["top set"]))

    def add_lift(self, lift: str) -> None:
        self.data.execute("INSERT INTO lifttype (name) VALUES (%s) ", (lift,))

    def create_block(self, block_type, block_name, username):
        result = self.get_blocks(username)
        for row in result:
            if row["name"] == block_name:
                return False
        self.data.execute("INSERT INTO blocks (blocktype, userid, name) VALUES (%s, (SELECT userid FROM users WHERE "
                          "username = %s), %s)", (block_type, username, block_name))
        return True

    def get_lifts(self) -> list:
        lifts = self.data.fetchall("SELECT name FROM lifttype")
        existing_lifts = []
        for i in lifts:
            existing_lifts.append(i["name"])
        return existing_lifts

    def get_blocks(self, username) -> list:
        blocks = self.data.fetchall("SELECT name FROM blocks WHERE userid = (SELECT userid FROM users "
                                    "WHERE username = %s)", (username,))
        return blocks

    def get_history(self, lift: str, block: str, user: str):
        block_row = self.data.fetchone("SELECT blockid, blocktype FROM blocks WHERE name = %s", (block,))
        if lift == "All lifts" and block == "All blocks":
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe, liftid FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.userid = (SELECT users.userid FROM users WHERE users.username = "
                                         "%s) ORDER BY date", (user,))
            output = (history, "All")
        elif lift == "All lifts":
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe, liftid FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.blockid = %s ORDER BY date",
                                         (block_row["blockid"],))
            output = (history, "All lifts")
        elif block == "All blocks":
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe, liftid FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.userid = (SELECT users.userid FROM users WHERE users.username = "
                                         "%s) AND lifts.liftname = %s ORDER BY date", (user, lift))
            output = (history, "All blocks")
        else:
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe, liftid FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.blockid = %s AND lifts.userid = (SELECT users.userid FROM users "
                                         "WHERE users.username = %s) AND lifts.liftname = %s ORDER BY date",
                                         (block_row["blockid"], user, lift))
            output = (history, "")
        return output
