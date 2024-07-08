import nox


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.decode("utf-8")
    session.run("pytest", *session.posargs)


@nox.session
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "--serve" to serve.
    """

    session.install(".[docs]")
    session.chdir("docs")
    session.decode("utf-8")
    session.run("sphinx-build", "-M", "html", ".", "build")


@nox.session
def serve(session: nox.Session) -> None:
    docs(session)
    print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
    session.decode("utf-8")
    session.run("python", "-m", "http.server", "8000", "-d", "_build/html")