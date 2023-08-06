import time
from pathlib import Path
from subprocess import PIPE, run

from lamin_logger import logger

# in root of lnhub-rest repository
SUPABASE_LOCAL_ANON_KEY_FILE = Path(__file__).parent.parent / ".supabase_local_anon_key"


def start_local_supabase():
    process = run(
        f"""supabase start | grep 'anon key'|cut -f2 -d ":" | sed -e 's/^[[:space:]]*//'""",  # noqa
        shell=True,
        stdout=PIPE,
    )
    logging_output = process.stdout.decode("UTF-8").replace("\n", "")
    if len(logging_output) > 0:
        logger.info(f"Writing anon key to {SUPABASE_LOCAL_ANON_KEY_FILE}")
        anon_key = logging_output
        open(SUPABASE_LOCAL_ANON_KEY_FILE, "w").write(anon_key)
    if process.returncode == 0:
        logger.success("Started supabase dockers! Stop them with `supabase stop`")
    else:
        raise RuntimeError("Failed to set up Supabase test instance. Is it running?")
    time.sleep(2)
    return "postgresql://postgres:postgres@localhost:54322/postgres"
