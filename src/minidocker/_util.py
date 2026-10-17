import subprocess
import sys


class CommandError(RuntimeError):
    def __init__(self, cmd, err, *args, **kwargs):
        super().__init__(cmd, err, *args, **kwargs)
        self.cmd = cmd
        self.err = err


def run_command(args, **kwargs):
    subprocess.run(args, check=True, **kwargs)


def run_command_for_output(args):
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
    except FileNotFoundError as e:
        print(
            "\nError running command:  %s\nLikely the command is not installed or not in the PATH.\n"
            % " ".join(args),
            file=sys.stderr,
        )
        raise e
    except subprocess.CalledProcessError as e:
        # print("\nError running command:  %s" % " ".join(args), file=sys.stderr)
        # print(e.stderr, file=sys.stderr)
        # raise e
        raise CommandError(" ".join(args), e.stderr) from None
    return result.stdout.rstrip("\n")


