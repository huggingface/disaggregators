import nox

python_versions = ["3.8", "3.9", "3.10"]


@nox.session(python=python_versions)
def tests(session):
    session.install(".[tests]")
    session.run("spacy", "download", "en_core_web_lg")
    session.run("make", "test")
