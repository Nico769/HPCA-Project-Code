import re

text_to_parse = """
Start
Process 8 finished in 7.1139s.

Process 2 finished in 7.1888s.

Process 5 finished in 7.1996s.

Process 6 finished in 8.9562s.

Process 3 finished in 8.9944s.

Process 9 finished in 9.0358s.

Process 7 finished in 10.3570s.

Process 4 finished in 10.4160s.

Process 1 finished in 10.4978s.

End
Start
Process 9 finished in 7.0031s.

Process 3 finished in 7.0874s.

Process 6 finished in 7.0876s.

Process 5 finished in 8.3848s.

Process 8 finished in 8.4303s.

Process 2 finished in 8.4481s.

Process 4 finished in 10.5088s.

Process 1 finished in 10.5558s.

Process 7 finished in 10.5998s.

End
Start
Process 3 finished in 6.5676s.

Process 9 finished in 6.6205s.

Process 6 finished in 6.6859s.

Process 8 finished in 10.0332s.

Process 5 finished in 10.0759s.

Process 2 finished in 10.0980s.

Process 4 finished in 10.3889s.

Process 1 finished in 10.5298s.

Process 7 finished in 10.5578s.

End
"""

def has_mo_match(matched_object):
    if matched_object is not None:
        return True
    else:
        return False
        
def parse_start(line):
    matched = re.compile(r'Start').search(line)
    if has_mo_match(matched):
        return matched.group()
    else:
        return ''
        
def parse_pid_time(line):
    matched = re.compile(r'\s(\d+).*?(\d{1,6}\.\d{1,6})').search(line)
    if has_mo_match(matched):
        return matched.group(1), matched.group(2)
    else:
        return ''
        
def parse_end(line):
    matched = re.compile(r'End').search(line)
    if has_mo_match(matched):
        return matched.group()
    else:
        return ''

tokenized_text = text_to_parse.splitlines()
for line in tokenized_text:
    pass
    # TODO Logica per pandas