import toml
import sqlalchemy as db

with open("dal/settings/secrets.toml", "r") as fp:
    resource = toml.load(fp)
    config = resource.get("mysqldb")
    user = config.get("user")
    password = config.get("password")
    port = config.get("port")
    host = config.get("host")
    database = config.get("database")


def get_conn():
    return db.create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )


if __name__ == "__main__":
    conn = get_conn()
