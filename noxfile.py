import nox

python_versions = ["3.8", "3.9", "3.10"]


@nox.session(python=python_versions)
def tests(session):
    session.install(".[tests]")
    session.run("make", "load_spacy_model", external=True)
    session.run("make", "test", external=True)
