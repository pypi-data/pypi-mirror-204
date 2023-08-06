import os
import sys
import tempfile
import yaml
from argparse import ArgumentParser
from os.path import basename

try:
    from conda.auxlib.path import expand
except ModuleNotFoundError:
    from conda._vendor.auxlib.path import expand

from conda.api import Channel, PrefixData, Solver, SubdirData
from conda.base.context import context
from conda.cli.conda_argparse import add_parser_networking, add_parser_prefix
from conda.gateways.connection.session import CONDA_SESSION_SCHEMES
from conda.models.match_spec import MatchSpec
from conda_env import exceptions, specs
from conda_env.env import from_environment
from conda_env.cli.common import get_prefix

ALL_PLATFORMS = ['linux-64', 'win-64', 'osx-64']
GPU_VARIANTS = {
    "tensorflow": "tensorflow-gpu"
}
GPU_EXTRAS = [
    MatchSpec(name='cudatoolkit', channel='defaults')
]


def get_packages(prefix):
    return list(sorted(PrefixData(prefix).iter_records(), key=lambda x: x.name))


def solve(pkgs, channels, subdir):
    solver = Solver(prefix=tempfile.mkdtemp(),
                    specs_to_add=pkgs,
                    channels=channels,
                    subdirs=[subdir, 'noarch'])
    return solver.solve_final_state()


def match_packages(packages, platform, channels=None,
                   requested_only=False, drop_version=False,
                   keep_build=False, with_gpu=False):
    matched = []
    for package in packages:
        if requested_only and package.requested_spec == 'None':
            continue

        match_args = {}

        if with_gpu:
            match_args['name'] = GPU_VARIANTS.get(package.name, package.name)
        else:
            match_args['name'] = package.name

        if package.version is not None and (not drop_version):
            match_args['version'] = package.version

        if keep_build and not with_gpu:
            match_args['build'] = package.build

        if channels is None:
            channels = []

        # packages gathered from a live environment
        # remember the channel they came from
        channel_attr = hasattr(package, 'channel')
        if channel_attr:
            channel_dump = package.channel.dump()
            del channel_dump['platform']
            match_args['channel'] = Channel(**channel_dump)
            channels.insert(0, match_args['channel'])

        pkg_match_spec = MatchSpec(**match_args)

        match = SubdirData.query_all(pkg_match_spec,
                                     channels=channels,
                                     subdirs=[platform, 'noarch'])
        if match:
            matched.append(pkg_match_spec)
        else:
            print(f'dropped {pkg_match_spec} for {platform}', file=sys.stderr)

    if with_gpu:
        matched.extend(GPU_EXTRAS)

    return matched


def cli():
    parser = ArgumentParser('conda-transfer')
    parser.add_argument('-f', '--file', action='store',  # default='environment.yml',
                        help='environment definition file')
    # parser.add_argument('--platform', help='Platform to create locked environment spec. Default is current platform.')
    parser.add_argument('--requested-only', action='store_true',
                        help='Only pin the requested packages and their current versions.')
    parser.add_argument('--drop-version', action='store_true',
                        help='Drop version numbers for packages.')
    parser.add_argument('--keep-build', action='store_true',
                        help='Keep build string when possible before solving the environment.')
    parser.add_argument('--with-gpu', action='store_true',
                        help='Switch compatible packages to their GPU variants and add cudatoolkit')

    parser.add_argument(
        'remote_definition',
        help='remote environment definition / IPython notebook',
        action='store',
        default=None,
        nargs='?'
    )

    add_parser_prefix(parser)
    add_parser_networking(parser)

    return parser.parse_args()


def main(args):
    if args.file or args.remote_definition:
        name = args.remote_definition or args.name
        try:
            if args.file:
                url_scheme = args.file.split("://", 1)[0]
                if url_scheme in CONDA_SESSION_SCHEMES:
                    filename = args.file
                else:
                    filename = expand(args.file)
            else:
                filename = expand('environment.yml')

            spec = specs.detect(name=name, filename=filename, directory=os.getcwd())
            env = spec.environment
            packages = [MatchSpec(p) for p in env.dependencies['conda']]

            # FIXME conda code currently requires args to have a name or prefix
            # don't overwrite name if it's given. gh-254
            # if args.prefix is None and args.name is None:
            #     args.name = env.name

            # prefix = args.remote_definition or filename

        except exceptions.SpecNotFound:
            raise
    else:
        prefix = get_prefix(args, search=False)
        packages = get_packages(prefix)
        write_env(prefix, args.name)

    by_platform = {}
    for platform in ALL_PLATFORMS:
        channels = list(context.channels)
        if 'win' in platform:
            channels.append('msys2')

        matched = match_packages(packages, platform, channels,
                                 requested_only=args.requested_only,
                                 drop_version=args.drop_version,
                                 keep_build=args.keep_build,
                                 with_gpu=args.with_gpu)

        solved = solve(matched, channels, platform)
        print(yaml.dump({'dependencies':sorted([f'{m.name}={m.version}' for m in solved])}))
        by_platform[platform] = solved

    write_lock(by_platform)


def write_env(prefix, name=None):
    if name is None:
        name = basename(prefix)

    env = from_environment(name, prefix, no_builds=True, from_history=True)
    env.filename = 'environment.yml'
    env.prefix = None
    env.save()


def write_lock(platform_specs, env_spec_hash=None):
    lock_specs = {}
    for platform, spec in platform_specs.items():
        lock_specs[platform] = [str(p) for p in spec]  # .split('::')[-1] for p in spec]

    lock = {
        'locking_enabled': True,
        'env_specs': {
            'default': {
                'locked': True,
                'platforms': list(platform_specs.keys()),
                'packages': lock_specs
            }
        }
    }

    if env_spec_hash is not None:
        lock['env_specs']['default']['env_spec_hash'] = env_spec_hash

    with open('environment-lock.yml', 'wt') as f:
        f.write(yaml.dump(lock))


if __name__ == '__main__':
    context.__init__()
    args = cli()
    main(args)