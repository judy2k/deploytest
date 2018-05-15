import pathlib

from invoke import task, Collection

@task
def install(c):
    c.run("pip install tox")

@task
def test(c):
    # export TOX_SKIP_MISSING_INTERPRETERS="False";
    c.run("tox")

@task
def check_formatting(c):
    print("Using ", end='')
    c.run("black --version")
    c.run("black --check src/")

@task
def publish(c):
    if pathlib.Path(".pypirc").is_file():
        c.run("pip install 'twine>=1.5.0'")
        c.run("python setup.py sdist bdist_wheel")
        c.run("twine upload -r test --config-file .pypirc dist/*")
        c.run("rm -fr build dist .egg requests.egg-info")
    else:
        print("Missing .pypirc file - has it been decrypted?")
        exit(1)


ns = Collection()
ns.add_task(install)
ns.add_task(test)
ns.add_task(check_formatting)

ci = Collection('ci')
ci.add_task(publish)
ns.add_collection(ci)