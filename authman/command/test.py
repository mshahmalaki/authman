from click import secho
from authman import app_cli, db


@app_cli.command("testdb", help="Check Database Connections.")
def app_cli_testdb():
    secho("Testing database connections...", nl=False)
    try:
        result = db.engine.execute("select 1;").first()
        if result[0] == 1:
            secho("SUCCESS", fg="green")
            success = True
        else:
            secho("BAD RESULT", fg="yellow")
            success = False
    except:
        secho("FAILED", fg="red")
        success = False
    if success is False:
        exit(1)
