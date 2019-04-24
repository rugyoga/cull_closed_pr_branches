from github import Github, UnknownObjectException, GithubException
import traceback
import sys
import os
import getopt


def cull_closed_pr_branches(options):
    github = Github(login_or_token=options["GIT_AUTH_TOKEN"], per_page=100)
    org_repo = '{}/{}'.format(options["org"], options["repo"])
    repo = github.get_repo(org_repo)
    for pull in repo.get_pulls(state='closed'):
        ref_name = pull.head.ref
        try:
            ref_path = 'heads/{}'.format(ref_name)
            git_ref = repo.get_git_ref(ref_path)
            print('https://github.com/{0}/pull/{1} -- {2}'.format(options["repo"], pull.number, ref_name))
            if options["force"]:
                git_ref.delete()
        except (UnknownObjectException, GithubException):
            print('.')
            pass
        except Exception as e:
            print(e)
            traceback.print_exc(e)
            exit(0)


def help(status):
    print 'GIT_AUTH_TOKEN=<token> python cull_dead_pr_branches.py -r <repo> -o <org>'
    sys.exit(status)


def process_options(argv):
    options = {"force": False, "GIT_AUTH_TOKEN": os.environ['GIT_AUTH_TOKEN']}
    try:
        opts, args = getopt.getopt(argv, "hfr:o:", ["help", "force", "repo=", "org="])
    except getopt.GetoptError:
        help(1)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            help(0)
        elif opt in ("-r", "--repo"):
            process_options["repo"] = arg
        elif opt in ("-f", "--force"):
            options["force"] = True
        elif opt in ("-o", "--org"):
            options["org"] = arg
    for required in ["repo", "org", "GIT_AUTH_TOKEN"]:
        if options[required] is None:
            print("missing <{}>".format(required))
            help(1)
    return options


def main(argv):
    cull_closed_pr_branches(process_options(argv[1:]))
