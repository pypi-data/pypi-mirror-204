'''
Created on 2022-11-24

@author: wf
'''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from yprinciple.version import Version
from yprinciple.ypgenapp import YPGenApp
from yprinciple.genapi import GeneratorAPI
import os
import sys
import traceback
import webbrowser
# import after app!
from jpcore.justpy_app import JustpyServer

class YPGen:
    """
    Y-Principle Generator
    """

    @classmethod
    def getArgParser(cls,description:str,version_msg)->ArgumentParser:
        """
        Setup command line argument parser
        
        Args:
            description(str): the description
            version_msg(str): the version message
            
        Returns:
            ArgumentParser: the argument parser
        """
        parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--about",help="show about info [default: %(default)s]",action="store_true")
        parser.add_argument('--context', default="MetaModel",help='context to generate from [default: %(default)s]')
        parser.add_argument("--topics",nargs="*",help="list of topic names\n[default: %(default)s]")
        parser.add_argument("--targets",nargs="*",help="list of target names\n[default: %(default)s]")
        parser.add_argument("-ga","--genViaMwApi",action="store_true",help="generate elements via Api")
        parser.add_argument("-gf","--genToFile",action="store_true",help="generate elements to files")
        parser.add_argument("--targetPath", dest="targetPath", help="path for the files to be generated - uses wikibackup default path for wikiId if not specified", required=False)
        parser.add_argument("--sidif", help="path to SiDIF input file")
        parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="show debug info [default: %(default)s]")
        parser.add_argument("-nd","--noDry", action="store_true", help="switch off dry run [default: %(default)s]")   
        parser.add_argument("--editor", action="store_true", help="open editor for results [default: %(default)s]")       
        parser.add_argument('--host',default=JustpyServer.getDefaultHost(),help="the host to serve / listen from [default: %(default)s]")
        parser.add_argument('--port',type=int,default=8778,help="the port to serve from [default: %(default)s]")
        parser.add_argument("--push", action="store_true", help="push from source to target [default: %(default)s]")       
        parser.add_argument("--serve",help="start webserver",action="store_true")
        parser.add_argument('--wikiId',"-t","--target", default="wiki",help='id of the wiki to generate for [default: %(default)s]')
        parser.add_argument('--source',"-s", default="profiwiki",help='id of the wiki to get concept and contexts (schemas) from [default: %(default)s]')
        parser.add_argument("-l", "--login", dest="login", action='store_true', help="login to source wiki for access permission")
        parser.add_argument("-f", "--force", dest="force", action='store_true', help="force to overwrite existing pages")
        parser.add_argument('-q', '--quiet', help="not verbose [default: %(default)s]" )
        parser.add_argument('-V', '--version', action='version', version=version_msg)
        return parser
    
__version__ = Version.version
__date__ = Version.date
__updated__ = Version.updated

def main(argv=None): # IGNORE:C0111
    '''main program.'''

    if argv is None:
        argv=sys.argv[1:]
    
    program_name = os.path.basename(__file__)
    program_shortdesc = Version.description
    
    program_version =f"v{__version__}" 
    program_build_date = str(__updated__)
    program_version_message = f'{program_name} ({program_version},{program_build_date})'

    user_name="Wolfgang Fahl"
    program_license = '''%s

  Created by %s on %s.
  Copyright 2022-2023 Wolfgang Fahl. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, user_name,str(__date__))
    try:
        parser=YPGen.getArgParser(description=program_license,version_msg=program_version_message)
        args = parser.parse_args(argv)
        if len(argv) < 1:
            parser.print_usage()
            sys.exit(1)
        #ypgen=YPGen(args)
        if args.about:
            print(program_version_message)
            print(f"see {Version.doc_url}")
            webbrowser.open(Version.doc_url)
        elif args.serve:
            ypGenApp=YPGenApp(version=Version, title="Y-Principle generator",args=args)
            url=f"http://{args.host}:{args.port}"
            webbrowser.open(url)
            ypGenApp.start(host=args.host, port=args.port,debug=args.debug)
            pass
        elif args.genToFile or args.genViaMwApi or args.push:
            gen=GeneratorAPI.fromArgs(args)
            if gen.error:
                print(f"{gen.errmsg}", file=sys.stderr)
                return 3
            dryRun=not args.noDry
            if args.genViaMwApi:
                gen.generateViaMwApi(target_names=args.targets,topic_names=args.topics, dryRun=dryRun, withEditor=args.editor)
            if args.genToFile:
                gen.generateToFile(target_dir=args.targetPath,target_names=args.targets,topic_names=args.topics, dryRun=dryRun, withEditor=args.editor) 
            if args.push:
                gen.push()       
        pass
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 1
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2       
        
DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())