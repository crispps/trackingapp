import json
from database import Database


class Lift:
    def __init__(self, path: str):
        self.path = path
        self.data = self.load_lift_data()

    def load_lift_data(self) -> object:
        db = Database(self.path)
        db.connect()
        return db

    def add_data(self, lift_name: str, user: str, data: dict[str, str]) -> None:
        self.data.execute("INSERT INTO lifts (blockid, userid, liftname, date, weight, sets, reps, rpe, topset) "
                          "VALUES ((SELECT blockid FROM blocks WHERE "
                          "name = ?),(SELECT userid FROM users WHERE username = ?) , ?, ?, ?, ?, ?, ?, ?)",
                          (data["block"], user, lift_name, data["date"], data["weight"], data["sets"], data["reps"],
                           data["rpe"], data["top set"]))

    def dump_data(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f)
            f.close()

    def add_lift(self, lift: str) -> None:
        self.data.execute("INSERT INTO lifttype (name) VALUES (?) ", (lift,))

    def create_block(self, block_type, block_name, username):
        result = self.get_blocks(username)
        for row in result:
            if row["name"] == block_name:
                return False
        self.data.execute("INSERT INTO blocks (blocktype, userid, name) VALUES (?, (SELECT userid FROM users WHERE "
                          "username = ?), ?)", (block_type, username, block_name))
        return True

    def get_lifts(self) -> list:
        lifts = self.data.fetchall("SELECT name FROM lifttype")
        existing_lifts = []
        for i in lifts:
            existing_lifts.append(i["name"])
        return existing_lifts

    def get_blocks(self, username) -> list:
        blocks = self.data.fetchall("SELECT name FROM blocks WHERE userid = (SELECT userid FROM users "
                                    "WHERE username = ?)", (username,))
        return blocks

    def get_history(self, lift: str, block: str, user: str):
        block_row = self.data.fetchone("SELECT blockid, blocktype FROM blocks WHERE name = ?", (block,))
        if lift == "All lifts" and block == "All blocks":
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.userid = (SELECT users.userid FROM users WHERE users.username = "
                                         "?) ORDER BY date", (user,))
            output = (history, "All")
        elif lift == "All lifts":
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.blockid = ? ORDER BY date",
                                         (block_row["blockid"],))
            output = (history, "All lifts")
        elif block == "All blocks":
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.userid = (SELECT users.userid FROM users WHERE users.username = "
                                         "?) AND lifts.liftname = ? ORDER BY date", (user, lift))
            output = (history, "All blocks")
        else:
            history = self.data.fetchall("SELECT liftname, blocks.name, date, weight, sets, reps, rpe FROM lifts "
                                         "INNER JOIN blocks ON lifts.blockid = blocks.blockid "
                                         "WHERE lifts.blockid = ? AND lifts.userid = (SELECT users.userid FROM users "
                                         "WHERE users.username = ?) AND lifts.liftname = ? ORDER BY date",
                                         (block_row["blockid"], user, lift))
            output = (history, "")
        return output
