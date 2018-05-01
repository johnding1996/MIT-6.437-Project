import sys
import os

def run(student_MIT_email):
    datasource = ['ciphertext']

    # Open logging file
    f = open('log/evaluation_run_submitted_code.py.log','a')
    path = './test/' + student_MIT_email
    sys.path.append(path)
    print 'Running: ' + student_MIT_email

    for source in datasource:
        # Create filenames
        output_fname = 'output_' + student_MIT_email + '_' + source + '.txt';
        input_fname = 'ciphers_and_messages/' + source + '.txt'

        # Get ciphertext
        ciphertext = get_text(input_fname)

        # Write to log
        f.write(source + ': Started...\n')

        # Actually run the file
        f.write('trying\n')
        os.chdir(path)
        sys.path.append(os.getcwd())
        try:
            import decode
            decode.decode(ciphertext, output_fname)
            f.write('Done!\n')
            print 'done'
        except Exception as e:
            f.write('Exception!\n')
            print 'exception:', e
        os.chdir('../../')
            

def get_text(fname):
    g = open(fname, 'r')
    s = g.readlines()
    y = s[0].strip()
    g.close()
    return y


if __name__=="__main__":
    if len(sys.argv) != 2:
        print "student mit email not provided"
    else:
        run(sys.argv[1])

