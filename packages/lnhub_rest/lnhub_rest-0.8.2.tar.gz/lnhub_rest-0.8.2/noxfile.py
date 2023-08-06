import os

import nox
from lamin_logger import logger
from laminci.nox import login_testuser1, login_testuser2

nox.options.reuse_existing_virtualenvs = True


if "BRANCH_NAME" in os.environ:
    branch_name = os.environ["BRANCH_NAME"]
    logger.info(f"Using BRANCH_NAME {branch_name}")
else:
    logger.info("Env variable BRANCH_NAME not found")


# lamin_env = "local"
# if branch_name is not None:
#     if branch_name == "main":
#         lamin_env = "prod"
#     elif branch_name == "staging":
#         lamin_env = "staging"
#     else:
#         lamin_env = "local"
# elif "LAMIN_ENV" in os.environ:
#     lamin_env = os.environ["LAMIN_ENV"]

# logger.info(f"Setting LAMIN_ENV to {lamin_env}")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session
@nox.parametrize("package", ["lnhub-rest", "lndb"])
@nox.parametrize("lamin_env", ["local", "staging"])
def build(session: nox.Session, package: str, lamin_env: str):
    session.install("./lndb[dev,test]")
    session.install(".[dev,test]")
    session.run(
        "pytest",
        "-s",
        "--cov=lnhub_rest",
        "--cov-append",
        "--cov-report=term-missing",
        env={"LN_SERVER_DEPLOY": "1", "LAMIN_ENV": lamin_env},
    )
    if package == "lndb":
        login_testuser1(session)
        login_testuser2(session)
        os.chdir(f"./{package}")
        session.run(
            "pytest",
            "-s",
            "./tests",
            env={"LAMIN_ENV": lamin_env},
        )


@nox.session
def supabase_stop(session: nox.Session) -> None:
    session.run("supabase", "db", "reset", external=True)
    session.run("supabase", "stop", external=True)
