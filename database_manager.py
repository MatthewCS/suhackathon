import sqlite3


class DatabaseManager(object):

    def __init__(self, path):

        self.path = path


    def connect(self):

        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        return connection, cursor


    def read_database(self, table_name="scoreboard"):

        connection, cursor = self.connect()
        command = "SELECT * FROM {}".format(table_name)
        return cursor.execute(command)


    def upload_new_ips(self, ip_list):

        connection, cursor = self.connect()
        command = """
        INSERT OR IGNORE INTO scoreboard
        (
            ip, ftp_up, ssh_up, smtp_up, http_up, rdp_up, points
        )
        VALUES
        (
            \"{}\", 0, 0, 0, 0, 0, 0
        );"""

        for ip in ip_list:

            cursor.execute(command.format(ip))

        connection.commit()


    def update_scoreboard(self, port_dict):

        self.update_ports(port_dict)
        self.update_scores(port_dict)


    def update_ports(self, ports):

        connection, cursor = self.connect()
        command = """
        UPDATE scoreboard
        SET ftp_up=?,
            ssh_up=?,
            smtp_up=?,
            http_up=?,
            rdp_up=?
        WHERE ip=?
        """

        for ip in ports:

            params = list(ports[ip].values())
            params.append(ip)
            cursor.execute(command, params)

        connection.commit()


    def update_scores(self, ports):

        connection, cursor = self.connect()
        command = """
        UPDATE scoreboard
        SET points=points+{0}
        WHERE ip=\"{1}\"
        """

        for ip in ports:

            points = sum(list(ports[ip].values()))
            cursor.execute(command.format(points, ip))

        connection.commit()


def create_database():

    db = DatabaseManager("./info.db")
    command = """
    CREATE TABLE scoreboard
    (
        ip TEXT PRIMARY KEY,
        ftp_up BOOLEAN,
        ssh_up BOOLEAN,
        smtp_up BOOLEAN,
        http_up BOOLEAN,
        rdp_up BOOLEAN,
        points INT
    );
    """
    cursor, connection = db.connect()
    cursor.execute(command)
    connection.commit()


if __name__ == "__main__":

    try:
        create_database()
    except:
        pass

    print("Scoreboard:")
    for row in DatabaseManager("./info.db").read_database("scoreboard"):

        print("  ", row)
