import os
import subprocess


def main():
    base_path = os.path.abspath('.')
    resources_path = os.path.join(base_path, "resources")
    images = os.listdir(os.path.join(resources_path, 'images'))
    qml_path = os.path.join(base_path, "qml")
    qmls = os.listdir(qml_path)

    f = open('resources.qrc', 'w+')
    f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource prefix="/">\n')

    for item in qmls:
        f.write(u'<file alias="qml/' + item + '">qml/' + item + '</file>\n')

    for item in images:
        f.write(u'<file alias="image/' + item + '">resources/images/' + item + '</file>\n')

    f.write(u'</qresource>\n</RCC>')
    f.close()

    pyrcc_path = 'D:/ProgramData/anaconda3/Scripts/pyside6-rcc.exe'
    cmd = '{} resources.qrc -o resources_rc.py'.format(pyrcc_path)
    invoke_cmd(cmd)


def invoke_cmd(cmd, debug=True):
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    while True:
        line = pipe.stdout.read()
        if debug:
            print(line)
        if not line:
            break

    code = pipe.wait()
    print(code)
    if code != 0:
        print(type(code))
        raise Exception("cmd failed: %d" % code)


if __name__ == "__main__":
    main()
