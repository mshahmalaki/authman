from click import secho
from authman import app_cli, db


@app_cli.command("testdb", help="Check Database Connections.")
def app_cli_testdb():
    secho("Testing database connections...", nl=False)
    (db_status, db_message) = db_check()
    if db_status:
        secho(db_message, fg="green")
    else:
        secho(db_message, fg="red")
        exit(1)

def db_check():
    try:
        result = db.engine.execute("select 1;").first()
        if result[0] == 1:
            return True, "DB, SUCCESS!"
        else:
            return False, "DB, BAD RESULT"
    except:
        return False, "DB, FAILED!"
