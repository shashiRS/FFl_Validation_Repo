Search.setIndex({"docnames": ["howto", "howto/assessment_sync_tool", "howto/building_a_wheel", "howto/debugging", "howto/expected_result_interval", "howto/external_link", "howto/hpc", "howto/overview_page", "howto/report", "howto/uri", "howto/user_registration", "howto/user_webui_registration", "index", "quickstart/quickstart", "setup/setup", "tutorial/cli_commands/database", "tutorial/cli_commands/report", "tutorial/cli_commands/runner", "tutorial/run_spec", "tutorial/understanding_tsf", "tutorials"], "filenames": ["howto.rst", "howto\\assessment_sync_tool.rst", "howto\\building_a_wheel.rst", "howto\\debugging.rst", "howto\\expected_result_interval.rst", "howto\\external_link.rst", "howto\\hpc.rst", "howto\\overview_page.rst", "howto\\report.rst", "howto\\uri.rst", "howto\\user_registration.rst", "howto\\user_webui_registration.rst", "index.rst", "quickstart\\quickstart.rst", "setup\\setup.rst", "tutorial\\cli_commands\\database.rst", "tutorial\\cli_commands\\report.rst", "tutorial\\cli_commands\\runner.rst", "tutorial\\run_spec.rst", "tutorial\\understanding_tsf.rst", "tutorials.rst"], "titles": ["How To", "TSF Assessment sync tool", "Build a Wheel", "Debugging", "Expected Result Interval", "TSF Report - External Links", "Submit to HPC", "Overview Page", "TSF Report", "Uniform Resource Identifier (URI)", "TSF User registration", "TSF User WebUI registration", "ADAS TSF Examples", "Quickstart", "Setup Python", "Command line arguments for custom database connection (Optional)", "Command line arguments for report.py", "Command line arguments for runner.py", "Understanding run_spec.json", "Understanding usage of TSF tooling", "Tutorials"], "terms": {"debug": [0, 7, 8, 12, 18, 19, 20], "test": [0, 2, 5, 6, 7, 8, 9, 11, 12, 14, 17, 18], "case": [0, 5, 7, 12, 13, 17, 18], "implement": [0, 12, 18], "process": [0, 1, 5, 7, 12, 13, 16, 17, 18], "two": [0, 4, 5, 7, 8, 12, 18], "bsig": [0, 7, 8, 12, 13, 18], "parallel": [0, 12], "tsf": [0, 2, 6, 7, 9, 14, 15, 16, 17, 18, 20], "user": [0, 1, 5, 7, 8, 12, 15, 16, 17, 18], "registr": [0, 12], "webui": [0, 10, 12], "report": [0, 2, 3, 10, 11, 12, 13, 15, 17, 18, 19, 20], "output": [0, 3, 7, 12, 13, 16, 18], "folder": [0, 2, 12, 16, 18], "structur": [0, 7, 9, 12, 18], "html": [0, 5, 12], "overview": [0, 5, 8, 12, 13, 16, 18], "page": [0, 4, 6, 8, 9, 10, 12, 14, 17], "info": [0, 12, 16, 17], "section": [0, 5, 8, 9, 12, 18], "testcas": [0, 3, 5, 8, 12, 17, 18], "verdict": [0, 12, 13], "tool": [0, 10, 12, 20], "statist": [0, 8, 12, 13, 16, 18], "event": [0, 2, 8, 12, 17], "teststep": [0, 7, 8, 12, 17], "build": [0, 12], "wheel": [0, 6, 12], "expect": [0, 7, 12], "result": [0, 3, 7, 8, 9, 12, 13], "interv": [0, 12], "us": [0, 1, 3, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18], "confid": [0, 7, 12], "To": [2, 3, 6, 12, 13], "creat": [1, 2, 5, 8, 14, 16, 18], "organis": 2, "follow": [2, 4, 5, 6, 7, 8, 9, 10, 16, 18], "step": [2, 8, 9, 10, 13], "repo": [2, 18], "add": [2, 6, 7, 13, 14, 18], "webhook": 2, "set": [0, 2, 3, 4, 7, 9, 12, 16, 17, 18], "hook": 2, "payload": 2, "url": [0, 2, 7, 12, 18], "http": [2, 10, 14, 18], "am": [2, 14, 18], "ada": [2, 13, 14, 18], "aw": 2, "jenkin": [2, 11], "eu1": 2, "agileci": 2, "conti": [2, 10, 14, 18], "de": [2, 10, 14, 18], "github": [2, 14, 18], "content": [2, 16], "type": [2, 7, 9, 15, 16, 17, 18], "applic": [2, 5], "json": [0, 2, 8, 12, 16, 17, 19, 20], "select": [2, 7, 10, 16], "send": 2, "me": 2, "everyth": 2, "under": [2, 7, 18], "which": [2, 5, 7, 8, 13, 16, 17, 18], "would": [2, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18], "you": [2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18], "like": [2, 7, 11, 13, 14, 15, 16, 17, 18], "trigger": 2, "thi": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 17, 18], "file": [2, 3, 7, 8, 13, 16, 17, 18], "need": [2, 3, 6, 13, 14, 16, 17, 18], "creation": 2, "were": [2, 7, 8], "copi": [1, 2, 16, 18], "from": [2, 5, 7, 8, 10, 13, 14, 16, 17, 18], "wa": [2, 7], "extend": [2, 5], "requir": [2, 3, 7, 8, 14, 15, 16, 17, 18], "setup": [2, 7, 8, 12, 13], "py": [2, 3, 6, 12, 15, 19, 20], "packag": [2, 6, 9, 17], "defin": [2, 3, 7, 13, 18], "name": [2, 5, 6, 7, 9, 10, 13, 15, 18], "descript": [2, 7, 9, 13, 15, 16, 17, 18], "long": 2, "package_data": 2, "extens": [2, 18], "entry_point": 2, "function": [2, 3, 9, 13], "execut": [1, 2, 3, 7, 8, 9, 16, 18], "noxfil": 2, "In": [2, 7, 9, 10], "nox": 2, "": [2, 6, 7, 8, 9, 13, 16, 17, 18], "dure": [2, 3, 7, 8, 9, 13], "lint": 2, "must": [2, 6], "run": [2, 13, 14, 16, 17, 18], "pytest": 2, "junitxml": 2, "xml": 2, "cach": 2, "clear": 2, "your": [2, 3, 6, 7, 10, 16, 17, 18], "txt": [2, 14], "requirements_develop": 2, "pyproject": 2, "toml": 2, "pre": [2, 13, 16, 17], "commit": [2, 18], "jenkinsfil": 2, "flake8": 2, "pip": [2, 14], "ini": [2, 14], "c": 2, "programdatapip": 2, "make": [2, 14, 15], "awar": 2, "artifactori": [2, 6, 14], "command": [2, 6, 7, 12, 19, 20], "instal": [2, 13, 14, 17], "vnev": 2, "python": [1, 2, 6, 9, 12, 13, 17], "m": [1, 2, 14, 16, 17], "w": [2, 17], "dist": 2, "ha": [2, 4, 5, 7, 8, 10, 13], "check": [2, 7, 9, 13, 16, 17], "all": [2, 3, 7, 8, 9, 13, 15, 16, 18], "ar": [2, 4, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18], "part": [2, 7, 8, 13, 17], "If": [2, 4, 5, 7, 9, 10, 11, 13, 15, 16, 17], "ani": [2, 13, 14, 18], "miss": 2, "__init__": [2, 13], "those": [2, 7], "local": [0, 2, 8, 12, 16, 17, 18], "after": [2, 13, 18], "success": [2, 10], "push": 2, "chang": [2, 8, 9], "branch": [2, 18], "publishcoverag": 2, "adapt": 2, "archiveartifact": 2, "coverag": 2, "batch": [2, 13, 16], "publish": 2, "demo": [3, 5, 12], "demonstr": [3, 12, 13], "how": [1, 3, 5, 6, 7, 9, 12, 13], "call": [3, 6, 13, 14], "coupl": 3, "produc": 3, "i": [1, 3, 4, 5, 7, 8, 9, 13, 15, 16, 17, 18], "veri": [3, 16], "develop": [3, 7, 9, 12, 13, 14, 18, 19, 20], "sinc": [3, 8], "won": 3, "t": [3, 13, 15], "access": [3, 7, 10], "oracl": [3, 8, 10, 11, 15, 16, 17], "databas": [3, 7, 8, 10, 11, 12, 16, 17, 19, 20], "hpc": [0, 3, 7, 12, 18, 19, 20], "e": [3, 8, 9, 13, 14, 16, 17], "g": [3, 13, 14, 16, 17], "compon": [3, 7, 9], "want": [3, 13], "def": [3, 5, 9, 13], "main": [3, 8, 13], "data_fold": [3, 13], "path": [3, 8, 9, 13, 16, 17, 18], "output_fold": [], "open_explor": [3, 13, 18], "true": [3, 9, 13, 18], "entri": 13, "point": [1, 8, 13, 14, 18], "test_bsig": [3, 13], "f": [3, 9, 13], "test_input_": [3, 13], "k": [3, 13], "rang": [3, 13], "3": [3, 7, 9, 14, 17], "b": [3, 13], "generate_bsig": [3, 13], "exampleusecasetestcas": 13, "temp_dir": [3, 13, 16, 18], "clean_dir": [16, 18], "project_nam": [], "project_2": [], "The": [3, 4, 5, 6, 7, 8, 13, 15, 16, 17, 18], "full": [3, 13, 16, 17], "exampl": [3, 5, 7, 9, 13, 14, 18, 19, 20], "can": [3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18], "found": [3, 7], "single_bsig": 3, "mani": [3, 13], "simul": [3, 7, 13, 18], "more": [3, 5, 7, 8, 9, 13, 16, 18], "than": [3, 7, 9, 13], "one": [3, 6, 10, 13, 16, 17], "multipl": [3, 18], "either": [3, 4, 5, 7, 13, 18], "split": [3, 18], "cycl": [3, 7], "devic": [3, 13], "input": [1, 3, 6, 7, 8, 9, 13, 16, 17, 18], "explain": [4, 6, 7, 8], "usag": [4, 12, 20], "an": [4, 5, 7, 8, 9, 13, 14, 15, 16, 17, 18], "instanti": 4, "directli": [4, 14], "give": 4, "string": [4, 7, 9], "numer": [4, 7, 13], "lower": [4, 16, 17], "limit": [4, 17], "numerator2": 4, "upper": 4, "both": 4, "inclus": 4, "As": [4, 15], "oper": [4, 9, 13], "relationoper": [4, 9, 13], "between": [4, 13], "denomin": 4, "common": 4, "appli": 4, "given": [4, 13, 16], "wai": [3, 4, 9], "There": 4, "valu": [4, 5, 7, 13, 18], "error": [4, 7, 16, 17], "differ": [4, 5, 7], "calcul": 4, "mean": [4, 9], "we": [5, 7, 8, 9, 13, 14, 18], "navig": [7, 10], "through": [0, 7, 12, 14], "whole": 7, "contain": [7, 8, 14, 16, 18], "mainli": [7, 18], "four": 7, "list": [7, 9, 11, 13, 15, 16, 17, 18], "below": [7, 15, 16, 17, 18], "go": 7, "detail": [7, 8, 10, 13, 15, 16], "orang": 7, "continent": 7, "color": 7, "text": [5, 7, 18], "link": [0, 6, 7, 10, 12], "These": [7, 8, 15], "avail": [6, 7, 8, 16, 17, 18], "everi": [7, 8, 16, 17], "around": 7, "explor": 7, "highli": 7, "recommend": 7, "inform": [5, 6, 7, 8, 9, 13, 18], "testrun": [7, 10, 11, 16, 17, 18], "top": [7, 10], "number": [7, 13, 17], "id": [1, 7, 8, 14, 16], "bracket": 7, "A": [5, 7, 8, 9, 13], "valid": [3, 6, 7, 11, 13], "each": [7, 8, 13], "provid": [3, 5, 6, 7, 8, 13, 18], "base": [7, 8], "known": [7, 18], "project": [6, 7, 9, 11, 18], "subject": [7, 18], "anyth": [7, 9], "uniqu": [7, 9], "enough": 7, "verbos": [7, 16, 17], "motiv": 7, "alik": 7, "some": [5, 6, 7, 8, 13, 16, 17, 18], "regist": [7, 9, 10, 11], "softwar": [7, 13, 18], "assign": [7, 9], "collect": [1, 7], "plan": [7, 18], "remark": [7, 18], "possibl": [3, 7, 13, 18], "ad": [0, 7, 8, 12, 18], "comment": [7, 9], "later": [1, 7, 13, 18], "discuss": [7, 8, 9], "ex": [7, 14, 17], "mron": 7, "rrec": 7, "rec": 7, "etc": [7, 8, 9], "onli": [3, 6, 7, 8, 10, 16, 17], "consid": [7, 8, 11], "allow": [5, 6, 7, 10], "u": 7, "perform": [6, 7], "repeat": 7, "same": [7, 16], "also": [7, 10], "should": [5, 6, 7, 13, 14, 18], "By": 7, "click": [5, 7, 10], "direct": [7, 10], "new": [1, 7, 9, 18], "where": [7, 8, 9, 16, 18], "have": [5, 7, 8, 9, 11, 13, 16, 18], "super": [7, 13], "filter": 7, "record": [1, 6, 7, 8, 17, 18], "respect": [5, 7, 8], "individu": 7, "statu": 7, "thei": 7, "had": 7, "For": [6, 7, 9, 13, 14], "here": [7, 8, 9, 16, 17, 18], "eba": [7, 9, 11, 13], "team": 7, "chose": 7, "eba_endur": 7, "releas": 7, "sw_043": 7, "003": 7, "001": [7, 18], "request": [6, 7, 8, 10, 18], "It": [7, 8, 18], "good": 7, "practic": [7, 9], "consist": 7, "convent": [6, 7], "order": [7, 8, 10, 13], "easili": [7, 9], "differenti": 7, "variou": [7, 18], "version": [7, 9, 14, 16, 17, 18], "tabl": [7, 10, 15], "row": 7, "attach": 7, "sub": [7, 8, 9], "child": [7, 18], "column": [7, 13], "spec": [7, 16, 17, 18], "tag": [7, 18], "alpha": 7, "charact": [7, 9], "identifi": [0, 7, 12], "manag": [7, 18], "door": 7, "well": [7, 8], "compar": 7, "rate": [7, 9], "per": [7, 8, 16], "x": [7, 13, 17], "kilomet": 7, "relev": [7, 8, 13], "measur": 7, "framework": [7, 13], "got": 7, "evalu": [7, 13], "comput": [6, 7, 9, 13, 16], "depend": [7, 8, 13], "pass": [1, 7, 9], "hyperlink": 7, "six": 7, "meet": 7, "fail": [7, 13], "doe": [7, 8], "n": 7, "data": [7, 8, 13, 16, 18], "nok": 7, "sensor": 7, "errat": 7, "erron": 7, "ground": [7, 9], "truth": 7, "broken": 7, "similar": [7, 18], "shall": [7, 8, 10], "affect": [7, 9], "over": [7, 9], "group": 7, "categor": 7, "them": [7, 15], "five": 7, "categori": 7, "out": [7, 9, 16], "other": [5, 7, 10, 13, 14], "help": [1, 7, 9, 18], "themselv": 7, "drop": [5, 7, 10], "down": [5, 7, 10, 13], "three": [6, 7, 8], "option": [1, 3, 7, 12, 16, 17, 19, 20], "current": [1, 7, 8, 9, 15], "api": 7, "kei": [7, 18], "server": 7, "auto": [7, 10], "scroll": 7, "usernam": 7, "rest": 7, "mandatori": [6, 7, 16, 17], "onlin": [7, 16, 18], "assess": [0, 7, 10, 12, 16, 18], "itinerari": [7, 8], "intermedi": 7, "befor": [7, 14, 16], "locat": [7, 8, 14, 16, 17, 18], "job": [6, 7, 16, 17, 18], "when": [3, 5, 6, 7, 8, 9, 14], "premis": 7, "lastli": 7, "gener": [0, 5, 7, 8, 9, 10, 11, 12, 18, 19, 20], "about": [5, 7, 9], "executor": 7, "alwai": 7, "footer": 7, "typic": [5, 7], "attribut": 7, "addit": [5, 6, 7, 8, 15, 17, 18], "web": [7, 9, 10], "custom": [5, 7, 8, 12, 16, 17, 18, 19, 20], "could": [7, 8], "fetch": [1, 7], "sever": 7, "analysi": 7, "total": 7, "distanc": 7, "time": [6, 7, 9, 13, 16], "visual": 7, "purpos": [7, 13, 16], "plot": [7, 8], "bar": 7, "histogram": [7, 8], "scatter": [7, 8], "definit": [7, 13, 16, 17], "relat": [5, 7], "while": 7, "up": [3, 5, 6, 7, 12], "verifi": [7, 9, 10], "script": [5, 8, 11, 12, 14, 16, 17, 18], "foundat": [5, 8, 11, 14, 18], "statisfi": 8, "store": [8, 16], "support": [5, 8, 13], "storag": 8, "imag": [8, 18], "graphic": 8, "signal": [8, 9, 13], "product": 8, "might": [8, 9, 18], "vari": [8, 13], "now": [5, 8, 9], "address": [8, 10], "recip": [8, 17], "map": [8, 13], "therefor": [8, 9], "basi": 8, "associ": [1, 8], "its": [8, 13], "video": [8, 16, 17, 18], "pictur": 8, "deliv": 8, "itself": 8, "hyphen": 8, "testcase_spec_tag": 8, "teststep_numb": 8, "hold": 8, "save": [8, 16], "seri": 8, "recipes_overview": 8, "csv": 8, "mea": 8, "sqlite": [1, 8, 15, 16, 17], "instanc": 8, "db": [1, 8, 10, 18], "run_spec": [0, 8, 12, 16, 17, 19, 20], "processing_graph": 8, "gv": 8, "represent": 8, "intern": [8, 9, 14], "take": [5, 8], "place": [8, 9, 14, 15, 18], "brief": 8, "target": [8, 13], "problem": 8, "fragment": [8, 16], "code": [8, 9, 12, 13, 14], "further": 8, "birdey": [8, 18], "meta": 8, "collection_overview": 8, "ref": 8, "front": 8, "left": [8, 10], "right": 8, "refer": [5, 8, 9, 16, 18], "camera": 8, "static": [0, 8, 12], "element": 8, "index": [8, 12], "homepag": 8, "welcom": 8, "emphasis": 8, "abl": [10, 13], "label": [9, 10], "matchbox": [10, 16, 17, 18], "pleas": [10, 14, 15], "login": [10, 15], "sign": 10, "window": [10, 17], "credenti": [6, 10], "ui": 10, "land": 10, "onc": 10, "self": [5, 9, 10, 13], "servic": [10, 15], "corner": 10, "home": 10, "email": 10, "fill": 10, "global": 10, "activ": [9, 10, 13, 14], "directori": [10, 16, 17, 18], "cannot": 10, "colleagu": 10, "alreadi": [10, 15, 17, 18], "see": [6, 10], "messag": 10, "pipelin": [0, 9, 11, 12], "ars540bw11": 11, "syshadha22": 11, "kindli": 11, "rais": [11, 16, 17], "jira": 11, "ticket": 11, "templat": [6, 11, 16, 18], "quickstart": 12, "prerequisit": [0, 12], "learner": 12, "profil": 12, "learn": 12, "object": [5, 9, 12], "testscript": [], "precondit": 12, "virtual": 12, "environ": 12, "tutori": 12, "understand": [12, 20], "line": [6, 12, 19, 20], "argument": [6, 12, 19, 20], "runner": [6, 12, 13, 15, 16, 18, 19, 20], "connect": [12, 16, 17, 19, 20], "paramet": [5, 6, 9, 12, 13, 15, 16, 17, 19, 20], "basic": [12, 19, 20], "advanc": [12, 15, 16, 17, 19, 20], "modul": [12, 17], "search": 12, "ll": 13, "know": [9, 13], "bit": [9, 13], "work": [1, 6, 13, 16, 17], "venv": [13, 14, 17], "quick": 13, "librari": 13, "familiar": 13, "panda": [13, 14], "datafram": 13, "read": [1, 5, 13], "what": [13, 16], "kpi": [9, 13, 16], "hil": 13, "sil": 13, "vsp": 13, "certain": [9, 13, 18], "behavior": 13, "thousand": 13, "without": [9, 13, 16, 17], "With": [9, 13], "singl": [9, 13], "shown": 13, "let": [9, 13], "assum": 13, "ccr": [13, 18], "approach": [9, 13], "ego": 13, "veloc": 13, "50": [9, 13], "km": [9, 13], "h": 13, "overlap": 13, "100": 13, "rotat": 13, "0": [9, 13, 14], "scope": 13, "assert": 13, "brake": 13, "deceler": 13, "reaction": 13, "earli": 13, "1": [5, 6, 9, 13, 16, 18], "ttc": 13, "look": [9, 13, 18], "interact": 13, "first": [9, 13], "open": [5, 13], "addition": 13, "mai": [9, 13], "start": [0, 3, 12, 13, 16, 18], "entir": 13, "mark": 13, "testcase_definit": 13, "ex_eba_000_001": 13, "usecas": 13, "carmak": 13, "erg": 13, "within": 13, "register_generic_collect": 13, "disciplin": [13, 18], "class": [5, 9, 13, 16], "properti": [9, 13], "test_step": [9, 13], "return": [5, 9, 13], "exampleaebteststep": [], "teststep_definit": [9, 13], "2": [7, 9, 13, 14, 17], "aeb": [], "expectedresult": 9, "unit": [9, 13], "greater_or_equ": 13, "aggregate_funct": 9, "aggregatefunct": 9, "register_sign": [9, 13], "ebasign": [], "kwarg": 13, "fall": [], "flank": [], "get": [], "frame": [], "reader": [5, 13], "rel": [], "tgt_x": [], "ego_x": [], "ego_velo": 13, "unreason": [], "replac": [], "40": [], "hardli": [], "move": [], "lim": [], "loc": 13, "pre_brake_decel": [], "diff": [], "slice": [], "empti": [], "timestamp": 13, "measured_result": 13, "els": [], "nan": [], "alia": 13, "signaldefinit": 13, "initi": 13, "_properti": 13, "ars540": [], "algosencycl": [], "medic_prebrakemea": [], "fprebrakedecel": [], "osi": [], "processor": [], "osi_data": [], "sensor_view": [], "global_ground_truth": [], "moving_object": [], "posit": 9, "phase": 13, "complex": 13, "accomplish": 13, "abov": [6, 13], "none": 3, "sample_input": [], "__file__": [], "parent": [], "v_vut": [], "z_rotat": [], "view": [13, 18], "download": [13, 14], "sourc": 13, "repositori": [6, 13, 18], "guid": 14, "interpret": 14, "6": 14, "pypi": 14, "mirror": 14, "appdata": 14, "config": [14, 17], "cd": 14, "path_to_example_repositori": 14, "my_venv": 14, "bat": [14, 16], "r": [14, 17], "numpi": 14, "plotli": 14, "commandlin": 14, "cmd": 14, "powershel": 14, "git": [14, 18], "bash": 14, "sure": 14, "pycharm": 14, "visualstudio": 14, "overrid": [15, 16, 17], "default": [15, 16, 17], "str": [5, 15, 16, 17, 18], "dialect": 15, "password": 15, "host": 15, "port": 15, "dsn": 15, "token": 15, "term": 15, "don": 15, "much": 15, "sens": 15, "wrong": 15, "continu": 15, "out_directori": 16, "testrun_id": [16, 18], "int": [16, 17, 18], "runspec": 16, "headnod": [16, 17], "runspec_headnod": 16, "lu00160vma": 16, "lu00156vma": 16, "lsas003a": 16, "ozas012a": 16, "head": [16, 17], "node": [16, 17], "jobid": 16, "d": [16, 18], "development_detail": 16, "flag": [16, 18], "input_directori": 16, "matchbox_directori": [16, 18], "video_directori": [16, 18], "suffix": [16, 18], "video_suffix": 16, "prefix": [5, 16, 18], "video_prefix": 16, "plugin": 16, "overview_plugin": 16, "statistic_plugin": 16, "resourc": [0, 6, 7, 12, 16, 18], "dir": [16, 17, 18], "custom_resource_dir": [16, 18], "custom_template_dir": [16, 18], "made": 16, "jinja2": 16, "clean": [16, 17, 18], "delet": [16, 17], "preprocess": 16, "from_hpc_preprocess": 16, "redo": 16, "redo_al": 16, "re": 16, "slow": 16, "copy_loc": 16, "robocopi": 16, "regress": [16, 18], "action": [], "store_tru": [], "done": [3, 5, 16, 17], "submit": [0, 12, 16, 17, 18], "processing_headnod": 16, "choos": [16, 17], "dedic": [16, 17], "zip": [5, 16], "pack": 16, "final": 16, "enabl": [16, 17], "browser": 16, "v": [16, 17], "count": [9, 16, 17], "log": [16, 17], "level": [16, 17], "stdout": [16, 17], "warn": [16, 17], "vv": [16, 17], "quiet": [16, 17], "q": [16, 17], "been": 16, "deprec": [7, 16, 17, 18], "opt": 16, "standard": [9, 16], "Then": [1, 5, 16, 17], "multiprocess": 17, "beta": [], "birdsey": 17, "export": 17, "append": 17, "updat": 17, "exist": 17, "caution": 17, "lookup": [], "xil": [], "configur": 17, "skip": 17, "max": 17, "socket": 17, "200": 17, "simultan": 17, "manual": 17, "temp": [16, 17, 18], "backhaul": [0, 12, 16, 17], "IF": [], "checkout": 17, "upcom": [], "find": [9, 18], "subject_under_test": 18, "test_disciplin": 18, "git_repo_url": 18, "git_hash": 18, "sw_creation_date_tim": 18, "hash": 18, "date": 18, "processing_input": 18, "recording_collect": 18, "generic_input_collect": 18, "versioned_input_collect": 18, "root": 18, "custom_overview": 18, "own": 18, "path_spec": 18, "mount_point": 18, "dict": [9, 18], "temporari": 18, "wipe": 18, "hpc_jobnam": [6, 18], "hpc_project": [6, 18], "hpc_templat": [6, 18], "extract": 18, "snippet": 18, "regression_path_spec": 18, "regression_input": 18, "sync_assess": 18, "sync": [0, 12, 18], "table_overview_additonal_info": 18, "pair": 18, "with_online_assess": 18, "method": [9, 18], "dev_report": [3, 18], "kpi_report": [3, 18], "kind": 18, "just": [5, 6, 18], "featur": [5, 18], "realli": 18, "util": [1, 14, 17, 18], "ars5xx": 18, "002": 18, "345": 18, "algo": 18, "frankfurt_merge_report": 18, "quarantin": 18, "legaci": 18, "minimal_exampl": 18, "ccrb": 18, "fals": [3, 9, 18], "past": 18, "larg": 18, "amount": 18, "geo": [14, 18], "s768sd": 18, "merge_report": 18, "20": 18, "02": 18, "2100": 18, "22": 18, "2101": 18, "ccrm": 18, "dataccrb": 18, "dataccr": 18, "dataccrm": 18, "project_v": [6, 18], "mandaori": [], "repeat_count": [16, 17], "specif": [5, 6, 12, 18, 19, 20], "usual": [17, 18], "consum": 18, "show": [5, 18], "taken": 18, "specifi": 18, "uniform": [0, 7, 12], "uri": [0, 7, 12], "uuid": [0, 12], "19": 7, "4": [7, 9], "9": [7, 9], "563": 9, "logic": 9, "physic": 9, "technologi": 9, "includ": [6, 9, 13], "real": 9, "world": 9, "peopl": 9, "concept": 9, "book": 9, "engin": 9, "refactor": 9, "worri": 9, "deploy": [6, 9], "scenario": 9, "classpath": 9, "unforeseen": 9, "issu": 9, "interest": 9, "wiki": 9, "univers": 9, "128": 9, "system": [6, 9], "accord": [6, 9], "block": 9, "uuid4": 9, "import": [5, 6, 9], "3042137c": 9, "284f": 9, "431a": 9, "9ab8": 9, "8dae293b5b77": 9, "briefli": 9, "decor": 9, "object_typ": 9, "acc": 9, "cvf": 9, "rdi": 9, "our": 9, "e4d2a32b": 9, "76ed": 9, "4371": 9, "b00d": 9, "162f823cadc9": 9, "register_input": 9, "examplekpitestcas": 9, "exampleteststep1": 9, "exampleteststep2": 9, "wherea": 9, "parameter": 9, "exampleparameterizedtestcaseuri": 9, "parameterizedtestcas": 9, "classmethod": 9, "compute_paramet": 9, "cl": 9, "parameterset": 9, "parameters_1": 9, "111": 9, "222": 9, "333": 9, "parameters_2": 9, "999": 9, "888": 9, "777": 9, "parameter_set": 9, "455f53af": 9, "7a34": 9, "4e70": 9, "9add": 9, "81afb265c3da": 9, "urlencod": 9, "parameter_1": 9, "parameter_2": 9, "second": [9, 13], "ctype": 9, "processinginputset": 9, "requirement_testcas": 9, "doors_url": 9, "ts_requirement_testcas": 9, "teststep_paramet": 9, "teststepparamet": 9, "exampleteststep": [9, 13], "dbc28e93": 9, "335f": 9, "43a0": 9, "b7ce": 9, "cd0b43ba9c16": 9, "correct": 9, "expected_result": [9, 13], "greater": 9, "en_parameter_2": 9, "enumer": 9, "en_parameter_1": 9, "091eccf7": 9, "c472": 9, "4bcd": 9, "8462": 9, "536151e80bb8": 9, "numerator_is_ev": 9, "less_or_equ": 9, "example_1": 9, "examplesignals1": 9, "dummi": 9, "confus": 9, "matrix": 9, "7c782c1e": 9, "a268": 9, "43c9": 9, "8a67": 9, "c9a3300e29e4": 9, "myconfusionmatrixteststep2": 9, "confusionmatrixteststep": 9, "ad2b8d16": 9, "abf": 9, "4bb0": 9, "83eb": 9, "2f4c9f49551e": 9, "exampleev": 9, "assessment_typ": 9, "exampleassess": 9, "prop_1": 9, "eventattribut": 9, "prop": 9, "attributetyp": 9, "float": 9, "prop_2": 9, "integ": 9, "prop_3": 9, "fcda7c46": 9, "863d": 9, "40ed": 9, "8a9c": 9, "0e7c029950b0": 9, "explicitassess": 9, "state": 9, "tp": 9, "asf": 9, "irrelev": 9, "fp": 9, "aaf": 9, "string_attribut": 9, "step_numb": 13, "examplesign": 13, "_log": [3, 13], "example_sign": 13, "activation_a": 13, "len": 13, "some_activation_a": 13, "activation_b": 13, "some_activation_b": 13, "activation_d": [], "some_activation_d": [], "binary_activation_a": 13, "binary_activation_b": 13, "sig_a": 13, "sig_b": 13, "sig_d": [], "aggregation_al": 13, "90": [], "tempfil": 13, "mkdtemp": 13, "o": [3, 13], "join": 13, "makedir": [3, 13], "exist_ok": [3, 13], "blob": 14, "14": 17, "testbench": [1, 17], "update_definit": 17, "instead": [17, 18], "Or": 17, "cli": [12, 19, 20], "00000": 16, "quickli": 16, "separ": 16, "thu": 16, "lot": 16, "stage": 17, "tc": 17, "automat": 17, "upload": 17, "hpc_two": [], "core": 5, "td": [], "validate_nam": [], "describ": 6, "document": 6, "high": 6, "runnar": [], "cluster": 6, "At": 6, "write": 6, "ars_srr": 6, "hcp": [0, 12], "permiss": 6, "aquir": 6, "conform": 6, "especi": 6, "properli": 6, "rule": 6, "__init__pi": 6, "reduc": 6, "exemplari": 6, "abc": [], "cde": [], "mix": [0, 12], "tipp": [0, 12], "troubleshoot": [0, 12], "special": [0, 12], "consider": [0, 12], "via": [0, 5, 12], "autom": [0, 12], "magic": 6, "extern": [0, 12], "complet": [], "outsid": 5, "redirect": 5, "externallink": 5, "external_link_report": 5, "customreportexternallink": 5, "externallinkpageclass": 5, "externallinkreportclass": 5, "displai": 5, "dropdown": 5, "rout": 5, "actual": 5, "next": 5, "achiev": 5, "customreportstaticreportcont": 5, "togeth": 5, "staticpagereportclass": 5, "avoid": 5, "ambigu": 5, "gnerat": [], "screenshot": 5, "deriv": 5, "menu": 5, "assement": 1, "wrt": 1, "assessment_sync_tool": 1, "proc": 1, "proc_input": 1, "collection_id": 1, "param": 1, "dev": 1, "path_to_sqlite_db": 1, "simplest": 3, "meant": 3, "jump": 3, "exampleminimaltestcas": 3, "repres": 13, "micro": 13, "activation_tim": 13, "iloc": 13, "90_a": 13, "cast": 13, "90_b": 13, "as_typ": 13, "np": 13, "int8": 13, "float32": 13}, "objects": {}, "objtypes": {}, "objnames": {}, "titleterms": {"how": [0, 4], "To": 0, "content": [0, 12, 19, 20], "build": 2, "wheel": 2, "debug": [3, 6, 13, 16, 17], "test": [3, 13], "case": 3, "implement": [3, 13], "process": [3, 6, 8], "two": 3, "bsig": 3, "parallel": 3, "expect": 4, "result": 4, "interv": 4, "us": [4, 6, 9], "confid": 4, "overview": 7, "page": [5, 7], "report": [5, 6, 7, 8, 16], "info": 7, "section": 7, "testcas": [7, 9, 13], "verdict": 7, "tool": [1, 7, 19], "statist": [5, 7], "event": [7, 9], "teststep": [9, 13], "tsf": [1, 5, 8, 10, 11, 12, 13, 19], "output": 8, "folder": 8, "structur": 8, "html": 8, "user": [10, 11], "registr": [10, 11], "webui": 11, "ada": 12, "exampl": [12, 16, 17], "indic": 12, "tabl": 12, "quickstart": 13, "prerequisit": [6, 13], "learner": 13, "profil": 13, "learn": 13, "object": 13, "testscript": [], "set": [6, 13], "up": 13, "setup": 14, "python": 14, "precondit": 14, "virtual": 14, "environ": 14, "usag": [14, 19], "custom": 15, "databas": 15, "connect": 15, "command": [15, 16, 17], "line": [15, 16, 17], "argument": [15, 16, 17], "understand": [18, 19], "py": [16, 17], "runner": 17, "run_spec": [6, 18], "json": [6, 18], "paramet": 18, "basic": 18, "advanc": 18, "tutori": 20, "option": 15, "uniform": 9, "resourc": 9, "identifi": 9, "uri": 9, "uuid": 9, "assess": [1, 9], "script": 13, "hpc": [6, 16, 17], "specif": [16, 17], "gener": [6, 16, 17], "develop": [16, 17], "cli": [16, 17], "submit": 6, "run": [], "hcp": 6, "backhaul": 6, "mix": 6, "local": 6, "tipp": 6, "troubleshoot": 6, "special": 6, "consider": 6, "via": 6, "autom": 6, "pipelin": 6, "start": 6, "extern": 5, "link": 5, "ad": 5, "url": 5, "through": 5, "static": 5, "sync": 1}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 8, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.todo": 2, "sphinx.ext.viewcode": 1, "sphinx": 57}, "alltitles": {"How To": [[0, "how-to"]], "Contents:": [[0, null], [12, null], [19, null], [20, null]], "TSF Assessment sync tool": [[1, "tsf-assessment-sync-tool"]], "Build a Wheel": [[2, "build-a-wheel"]], "Debugging": [[3, "debugging"]], "Debug a test case implementation": [[3, "debug-a-test-case-implementation"]], "Process two BSIGs in parallel": [[3, "process-two-bsigs-in-parallel"]], "Expected Result Interval": [[4, "expected-result-interval"]], "How to use": [[4, "how-to-use"]], "Confidence": [[4, "confidence"]], "TSF Report - External Links": [[5, "tsf-report-external-links"]], "Adding External URLs to the report": [[5, "adding-external-urls-to-the-report"]], "Adding External URLs through Statistics and Static page": [[5, "adding-external-urls-through-statistics-and-static-page"]], "Submit to HPC": [[6, "submit-to-hpc"]], "Prerequisites (HPC submit)": [[6, "prerequisites-hpc-submit"]], "Settings in run_spec.json": [[6, "settings-in-run-spec-json"]], "Start processing and report generation locally with submit to HCP": [[6, "start-processing-and-report-generation-locally-with-submit-to-hcp"]], "\u201cBackhaul\u201d for mixing HPC processing and local report generation": [[6, "backhaul-for-mixing-hpc-processing-and-local-report-generation"]], "Tipps for troubleshooting and debugging": [[6, "tipps-for-troubleshooting-and-debugging"]], "Special consideration for using HPC via automation pipeline": [[6, "special-consideration-for-using-hpc-via-automation-pipeline"]], "Overview Page": [[7, "overview-page"]], "Report Info section": [[7, "report-info-section"]], "Testcases section": [[7, "testcases-section"]], "Verdicts": [[7, "verdicts"]], "Overview section": [[7, "overview-section"]], "Tools section": [[7, "tools-section"]], "Statistics and Events section": [[7, "statistics-and-events-section"]], "Testcase Page": [[7, "testcase-page"]], "TSF Report": [[8, "tsf-report"]], "Output Folder structure": [[8, "output-folder-structure"]], "TSF Processing output": [[8, "tsf-processing-output"]], "TSF Reporting output": [[8, "tsf-reporting-output"]], "html report": [[8, "html-report"]], "Uniform Resource Identifier (URI)": [[9, "uniform-resource-identifier-uri"]], "UUID": [[9, "uuid"]], "Using URI": [[9, "using-uri"]], "Testcase": [[9, "testcase"]], "Teststep": [[9, "teststep"]], "Event": [[9, "event"]], "Assessment": [[9, "assessment"]], "TSF User registration": [[10, "tsf-user-registration"]], "TSF User WebUI registration": [[11, "tsf-user-webui-registration"]], "ADAS TSF Examples": [[12, "adas-tsf-examples"]], "Indices and tables": [[12, "indices-and-tables"]], "Quickstart": [[13, "quickstart"]], "Prerequisites": [[13, "prerequisites"]], "Learner profile": [[13, "learner-profile"]], "Learning Objectives": [[13, "learning-objectives"]], "Test scripting with TSF": [[13, "test-scripting-with-tsf"]], "Setting up Testcases and Teststeps": [[13, "setting-up-testcases-and-teststeps"]], "Debugging the test implementation": [[13, "debugging-the-test-implementation"]], "Setup Python": [[14, "setup-python"]], "Preconditions": [[14, "preconditions"]], "Virtual Environment": [[14, "virtual-environment"]], "Usage": [[14, "usage"]], "Command line arguments for custom database connection (Optional)": [[15, "command-line-arguments-for-custom-database-connection-optional"]], "Command line arguments for custom database connection": [[15, "id1"]], "Command line arguments for report.py": [[16, "command-line-arguments-for-report-py"]], "General arguments (report)": [[16, "general-arguments-report"]], "HPC specific arguments (report)": [[16, "hpc-specific-arguments-report"]], "Development/Debugging arguments (report)": [[16, "development-debugging-arguments-report"]], "Examples of report.py CLI commands": [[16, "examples-of-report-py-cli-commands"]], "Command line arguments for runner.py": [[17, "command-line-arguments-for-runner-py"]], "General arguments (runner)": [[17, "general-arguments-runner"]], "HPC specific arguments (runner)": [[17, "hpc-specific-arguments-runner"]], "Development/Debugging arguments (runner)": [[17, "development-debugging-arguments-runner"]], "Examples of runner.py CLI commands": [[17, "examples-of-runner-py-cli-commands"]], "Understanding run_spec.json": [[18, "understanding-run-spec-json"]], "run_spec parameters": [[18, "run-spec-parameters"]], "run_spec.json parameters": [[18, "id1"]], "Basic run_spec": [[18, "basic-run-spec"]], "Advanced run_spec": [[18, "advanced-run-spec"]], "Understanding usage of TSF tooling": [[19, "understanding-usage-of-tsf-tooling"]], "Tutorials": [[20, "tutorials"]]}, "indexentries": {}})